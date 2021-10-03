import yarl
import re
from disnake.ext import commands
import disnake
import asyncio
import base64
import binascii
import os

TOKEN_REGEX = re.compile(r'[a-zA-Z0-9_-]{23,28}\.[a-zA-Z0-9_-]{6,7}\.[a-zA-Z0-9_-]{27}')


def validate_token(token):
    try:
        # Just check if the first part validates as a user ID
        (user_id, _, _) = token.split('.')
        user_id = int(base64.b64decode(user_id, validate=True))
    except (ValueError, binascii.Error):
        return False
    else:
        return True


class GithubError(commands.CommandError):
    pass


class GistContent:
    def __init__(self, argument: str):
        try:
            block, code = argument.split('\n', 1)
        except ValueError:
            self.source = argument
            self.language = None
        else:
            if not block.startswith('```') and not code.endswith('```'):
                self.source = argument
                self.language = None
            else:
                self.language = block[3:]
                self.source = code.rstrip('`').replace('```', '')


class TokenInvalidation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock(loop=bot.loop)

    async def github_request(self, method, url, *, params=None, data=None, headers=None):
        hdrs = {
            'Accept': 'application/vnd.github.inertia-preview+json',
            'User-Agent': 'ViHillCorner\'s token invalidation',
            'Authorization': f'token {os.getenv("GITHUB_TOKEN")}'
        }

        req_url = yarl.URL('https://api.github.com') / url

        if headers is not None and isinstance(headers, dict):
            hdrs.update(headers)

        await self.lock.acquire()
        try:
            async with self.bot.session.request(method, req_url, params=params, json=data, headers=hdrs) as r:
                remaining = r.headers.get('X-Ratelimit-Remaining')
                js = await r.json()
                if r.status == 429 or remaining == '0':
                    # wait before we release the lock
                    delta = disnake.utils._parse_ratelimit_header(r)
                    await asyncio.sleep(delta)
                    self.lock.release()
                    return await self.github_request(method, url, params=params, data=data, headers=headers)
                elif 300 > r.status >= 200:
                    return js
                else:
                    raise GithubError(js['message'])
        finally:
            if self.lock.locked():
                self.lock.release()

    async def create_gist(self, content, *, description=None, filename=None, public=True):
        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }

        filename = filename or 'output.txt'
        data = {
            'public': public,
            'files': {
                filename: {
                    'content': content
                }
            }
        }

        if description:
            data['description'] = description

        js = await self.github_request('POST', 'gists', data=data, headers=headers)
        return js['html_url']

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        tokens = [token for token in TOKEN_REGEX.findall(message.content) if validate_token(token)]
        if tokens and message.author.id != self.bot.user.id:
            url = await self.create_gist('\n'.join(tokens), description='Discord tokens detected')
            msg = f'{message.author.mention}, I have found tokens and sent them to <{url}> to be invalidated for you.'
            return await message.channel.send(msg)


def setup(bot):
    bot.add_cog(TokenInvalidation(bot))

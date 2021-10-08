from typing import Optional, Union, Dict

from bot import database3


class DocCache:
    def __init__(self) -> None:
        self._cache = database3['DocsCache']
        self.cache = {}

    def _add_to_local_cache(self, item, value: str) -> None:
        """Adds to the local cache `self.cache`."""
        k = self.cache.get(item.package)
        if k is None:
            self.cache[item.package] = {}
        self.cache[item.package][item.symbol_id] = value

    async def set(self, item, value: str) -> None:
        """
        Set the Markdown `value` for the symbol `item`.
        All keys from a single page are stored together.
        """
        self._add_to_local_cache(item, value)

        k: Union[Dict, None] = await self._cache.find_one({'_id': item.package})
        if k is None:
            await self._cache.insert_one({'_id': item.package, 'data': {item.symbol_id: value}})
            return
        k['data'][item.symbol_id] = value
        await self._cache.update_one({'_id': item.package}, {'$set': {'data': k}})

    async def get(self, item) -> Optional[str]:
        """Return the Markdown content of the symbol `item` if it exists."""

        key: Union[Dict, None] = self.cache.get(item.package)
        if key is not None:
            result = key.get(item.symbol_id)
            if result is not None:
                return result
        k: Union[Dict, None] = await self._cache.find_one({'_id': item.package})
        if k is not None:
            res = k['data'].get(item.symbol_id)
            if res is not None:
                v = res
                self._add_to_local_cache(item, v)
                return res
        return None

    async def delete(self, package: str) -> bool:
        """Remove all values for `package`; return True if at least one key was deleted, False otherwise."""
        v = await self._cache.find_one({'_id': package})
        if v is None:
            return None
        await self._cache.delete_one({'_id': package})
        try:
            self.cache.pop(package)
        except KeyError:
            pass
        return True

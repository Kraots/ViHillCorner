from aiohttp import ClientSession
import os

authorization_token = os.getenv('HARPER_DB_KEY')
url = os.getenv('HARPER_DB_URL')

class Database:
    url = url
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {authorization_token}'
    }

    def __init__(self, session: ClientSession):
        self.session = session

    async def create_schema(self, name: str):
        """|coro|

        Creates the schema.
        
        Parameters
        ----------
            name: :class:`str`
                The name of the schema.
        """
        payload = '{"operation": "create_schema", "schema": "%s"}' % (name)
        async with self.session.post(url=self.url, headers=self.headers, data=payload) as r:
            return await r.text('utf8')

    async def drop_schema(self, name: str):
        """|coro|

        Drops the schema.
        
        Parameters
        ----------
            name: :class:`str`
                The name of the schema.
        """
        payload = '{"operation": "drop_schema", "schema": "%s"}' % (name)
        async with self.session.post(url=self.url, headers=self.headers, data=payload) as r:
            return await r.text('utf8')

    async def create_table(self, schema: str, name: str, hash_attr: str):
        """|coro|
        
        Creates the table for the given schema with the coresponding hash attribute.

        Parameters
        ----------
            schema: :class:`str`
                The name of the schema the table is created for.
            name: :class:`str`
                The name of the table.
            hash_attr: :class:`str`
                The hash attribute of the table.
        """
        payload = '{"operation": "create_table", "schema": "%s", "table": "%s", "hash_attribute": "%s"}' % (schema, name, hash_attr)
        async with self.session.post(url=self.url, headers=self.headers, data=payload) as r:
            return await r.text('utf8')

    async def drop_table(self, schema: str, name: str):
        """|coro|
        
        Drops the table for the given schema.

        Parameters
        ----------
            schema: :class:`str`
                The name of the schema the table is created for.
            name: :class:`str`
                The name of the table.
        """
        payload = '{"operation": "drop_table", "schema": "%s", "table": "%s"}' % (schema, name)
        async with self.session.post(url=self.url, headers=self.headers, data=payload) as r:
            return await r.text('utf8')
    
    async def do_sql(self, sql_code: str):
        """|coro|

        Performs SQL code.
        
        Parameters
        ----------
            sql_code: :class:`str`
                The SQL code which performs an SQL operation.
        """
        payload = '{"operation": "sql", "sql": "%s"}' % (sql_code)
        async with self.session.post(url=self.url, headers=self.headers, data=payload) as r:
            return await r.text('utf8')
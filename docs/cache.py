from __future__ import annotations

from typing import Optional, Union, Dict, TYPE_CHECKING

from utils.databases import DocsCache

if TYPE_CHECKING:
    from .cog import DocItem


class DocCache:
    def __init__(self) -> None:
        self._cache = DocsCache
        self.cache = {}

    def _add_to_local_cache(self, item: DocItem, value: str) -> None:
        """Adds to the local cache `self.cache`."""
        k = self.cache.get(item.package)
        if k is None:
            self.cache[item.package] = {}
        self.cache[item.package][item.symbol_id] = value

    async def set(self, item: DocItem, value: str) -> None:
        """
        Set the Markdown `value` for the symbol `item`.
        All keys from a single page are stored together.
        """
        self._add_to_local_cache(item, value)

        k: Union[DocsCache, None] = await self._cache.find_one({'_id': item.package})
        if k is None:
            doc = DocsCache(
                id=item.package,
                data={item.symbol_id: value}
            )
            await doc.commit()
            return
        k.data[item.symbol_id] = value
        await k.commit()

    async def get(self, item: DocItem) -> Optional[str]:
        """Return the Markdown content of the symbol `item` if it exists."""

        key: Union[Dict, None] = self.cache.get(item.package)
        if key is not None:
            result = key.get(item.symbol_id)
            if result is not None:
                return result
        k: Union[DocsCache, None] = await self._cache.find_one({'_id': item.package})
        if k is not None:
            res = k.data.get(item.symbol_id)
            if res is not None:
                v = res
                self._add_to_local_cache(item, v)
                return res
        return None

    async def delete(self, package: str) -> bool:
        """Remove all values for `package`; return True if at least one key was deleted, False otherwise."""
        v: DocsCache = await self._cache.find_one({'_id': package})
        if v is None:
            return None
        await v.delete()
        try:
            self.cache.pop(package)
        except KeyError:
            pass
        return True

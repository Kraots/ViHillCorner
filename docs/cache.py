from typing import Optional, Union, Dict
import os

from deta import Deta


class DocCache:
    def __init__(self) -> None:
        self._db = Deta(os.getenv('DETA_KEY'))
        self._cache = self._db.Base('DocsCache')
        self.cache = {}

    def _add_to_local_cache(self, item, value: str) -> None:
        """Adds to the local cache `self.cache`."""
        k = self.cache.get(item.package)
        if k is None:
            self.cache[item.package] = {}
        self.cache[item.package][item.symbol_id] = value

    def set(self, item, value: str) -> None:
        """
        Set the Markdown `value` for the symbol `item`.
        All keys from a single page are stored together.
        """
        self._add_to_local_cache(item, value)

        k: Union[Dict, None] = self._cache.get(item.package)
        if k is None:
            self._cache.insert({'data': {item.symbol_id: value}}, item.package)
            return
        k['data'][item.symbol_id] = value
        self._cache.put(k, item.package)

    def get(self, item) -> Optional[str]:
        """Return the Markdown content of the symbol `item` if it exists."""

        key: Union[Dict, None] = self.cache.get(item.package)
        if key is not None:
            result = key.get(item.symbol_id)
            if result is not None:
                print('took from local cache')
                return result

        k: Union[Dict, None] = self._cache.get(item.package)
        if k is not None:
            res = k['data'].get(item.symbol_id)
            if res is not None:
                v = res
                self._add_to_local_cache(item, v)
                print('local cache didn\'t work')
            return res
        return None

    def delete(self, package: str) -> bool:
        """Remove all values for `package`; return True if at least one key was deleted, False otherwise."""
        v = self._cache.get(package)
        if v is None:
            return None
        self._cache.delete(package)
        try:
            self.cache.pop(package)
        except KeyError:
            pass
        return True

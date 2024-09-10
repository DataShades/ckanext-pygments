from __future__ import annotations

import logging

import ckan.plugins.toolkit as tk
from ckan.lib.redis import connect_to_redis

from ckanext.pygments import const

log = logging.getLogger(__name__)


class RedisCache:
    """Cache data to Redis"""

    def __init__(self):
        self.client = connect_to_redis()

    def get_data(self, resource_id: str) -> str:
        """Return data from cache if exists"""
        raw_data = self.client.get(self.make_key(resource_id))

        if not raw_data:
            return ""

        log.debug("Pygments: cache hit for resource: %s", resource_id)

        return str(raw_data, "utf-8")  # type: ignore

    def set_data(self, resource_id: str, data: str):
        """Serialize data and save to redis"""
        cache_ttl = 7200  # TODO: make it configurable

        try:
            self.client.setex(self.make_key(resource_id), cache_ttl, data)
        except Exception as e:
            log.exception("Failed to save data to Redis: %s", e)

    def invalidate(self, resource_id: str):
        """Invalidate cache by key"""
        log.debug("Pygments: invalidating cache for resource: %s", resource_id)
        self.client.delete(self.make_key(resource_id))

    @classmethod
    def drop_cache(cls) -> None:
        """Drop all cache keys"""
        conn = connect_to_redis()

        log.debug("Pygments: dropping all cache keys")

        for key in conn.scan_iter(f"{const.REDIS_PREFIX}*"):
            conn.delete(key)

    def calculate_cache_size(self) -> int:
        """Return the size of the Redis cache"""
        total_size = 0

        for key in self.client.scan_iter(f"{const.REDIS_PREFIX}*"):
            size = self.client.memory_usage(key)

            if not size or not isinstance(size, int):
                continue

            total_size += size

        return total_size

    def calculate_resource_cache_size(self, resource_id: str) -> int:
        size = self.client.memory_usage(self.make_key(resource_id))

        if not size or not isinstance(size, int):
            return 0

        return size

    def make_key(self, resource_id: str) -> str:
        return f"{const.REDIS_PREFIX}{resource_id}"

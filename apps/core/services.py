from django.core.cache import cache
from django.conf import settings
from typing import Any, Optional
import hashlib
import json

class CacheService:
    @staticmethod
    def generate_key(prefix: str, *args: Any) -> str:
        """Generate a cache key based on prefix and arguments"""
        if args:
            # Hash only the arguments to keep prefix readable for pattern matching
            args_string = ':'.join(str(arg) for arg in args)
            args_hash = hashlib.md5(args_string.encode()).hexdigest()
            return f"{prefix}:{args_hash}"
        else:
            # If no args, just return the prefix
            return prefix
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        return cache.get(key)
    
    @staticmethod
    def set(
        key: str,
        value: Any,
        timeout: Optional[int] = None
    ) -> None:
        """Set value in cache with optional timeout"""
        if timeout is None:
            timeout = settings.CACHE_TIMEOUT
        cache.set(key, value, timeout)
    
    @staticmethod
    def delete(key: str) -> None:
        """Delete value from cache"""
        cache.delete(key)
    
    @staticmethod
    def get_or_set(
        key: str,
        default_func: callable,
        timeout: Optional[int] = None
    ) -> Any:
        """Get value from cache or set it if not exists"""
        value = cache.get(key)
        if value is None:
            value = default_func()
            CacheService.set(key, value, timeout)
        return value
    
    @staticmethod
    def invalidate_pattern(pattern: str) -> int:
        """
        Invalidate all keys matching pattern
        Returns number of keys deleted
        """
        deleted_count = 0
        
        try:
            # Try django-redis specific method first (most common production setup)
            if hasattr(cache, 'delete_pattern'):
                deleted_count = cache.delete_pattern(pattern)
                return deleted_count
            
            # Try backend with keys() method (some Redis backends)
            if hasattr(cache, 'keys'):
                try:
                    matching_keys = cache.keys(pattern)
                    if matching_keys:
                        cache.delete_many(matching_keys)
                        deleted_count = len(matching_keys)
                    return deleted_count
                except (AttributeError, TypeError):
                    pass
            
            # Fallback for LocMemCache - access internal cache dict
            if hasattr(cache, '_cache'):
                try:
                    import fnmatch
                    cache_keys = list(cache._cache.keys())
                    matching_keys = []
                    
                    for key in cache_keys:
                        # Extract actual key from Django's versioned format for pattern matching
                        # LocMemCache stores keys as ":version:actual_key"
                        stored_key = str(key)
                        actual_key = stored_key
                        
                        if stored_key.startswith(':'):
                            # Remove version prefix to get the original key
                            # Format is typically ":1:prefix:hash" -> "prefix:hash"
                            parts = stored_key.split(':', 2)
                            if len(parts) >= 3:
                                actual_key = parts[2]  # Get everything after ":version:"
                        
                        # Now match the pattern against the actual key (without version prefix)
                        if fnmatch.fnmatch(actual_key, pattern):
                            matching_keys.append(actual_key)
                    
                    # Delete the matching keys using their original format
                    for actual_key in matching_keys:
                        cache.delete(actual_key)
                        deleted_count += 1
                        
                    return deleted_count
                except Exception:
                    pass
            
            # If no method works, log warning and return 0
            # In production, this should be logged properly
            return 0
            
        except Exception:
            # Graceful fallback - don't break the application
            return 0
"""
Caching functionality for dictionary lookups.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Optional


class Cache:
    """File-based cache for dictionary lookups."""
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl_days: int = 30):
        if cache_dir is None:
            xdg_cache = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
            cache_dir = xdg_cache / "define"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_days * 86400
    
    def _hash(self, word: str, lang: str) -> str:
        """Generate cache key hash."""
        key = f"{lang}:{word}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def _cache_path(self, word: str, lang: str) -> Path:
        """Get cache file path for a word."""
        return self.cache_dir / f"{self._hash(word, lang)}.json"
    
    def get(self, word: str, lang: str) -> Optional[dict]:
        """
        Get cached definition if available and not expired.
        
        Args:
            word: The word to look up
            lang: Language code
            
        Returns:
            Cached result or None
        """
        cache_file = self._cache_path(word, lang)
        
        if not cache_file.exists():
            return None
        
        # Check if expired
        file_age = time.time() - cache_file.stat().st_mtime
        if file_age > self.ttl_seconds:
            cache_file.unlink()
            return None
        
        try:
            return json.loads(cache_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return None
    
    def set(self, word: str, lang: str, data: dict) -> None:
        """
        Cache a definition.
        
        Args:
            word: The word
            lang: Language code
            data: Definition data to cache
        """
        cache_file = self._cache_path(word, lang)
        try:
            cache_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except IOError:
            pass  # Silently fail on cache write errors
    
    def clear(self) -> int:
        """
        Clear all cached definitions.
        
        Returns:
            Number of files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except IOError:
                pass
        return count


# Need this import at the top level
import os

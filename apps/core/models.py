from django.db import models
from django.core.cache import cache

class Setting(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_public:
            cache.set(f'setting_{self.key}', self.value, timeout=3600)
    
    @classmethod
    def get_value(cls, key):
        cached_value = cache.get(f'setting_{key}')
        if cached_value is not None:
            return cached_value
            
        try:
            setting = cls.objects.get(key=key)
            if setting.is_public:
                cache.set(f'setting_{key}', setting.value, timeout=3600)
            return setting.value
        except cls.DoesNotExist:
            return None
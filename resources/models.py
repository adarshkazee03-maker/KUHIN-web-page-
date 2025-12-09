from django.db import models
from ckeditor.fields import RichTextField

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-file')
    
    class Meta:
        verbose_name_plural = 'Resource Categories'
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('link', 'External Link'),
        ('video', 'Video'),
        ('tool', 'Tool/Software'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='resources/files/', blank=True)
    external_link = models.URLField(blank=True)
    thumbnail = models.ImageField(upload_to='resources/thumbnails/', blank=True)
    uploaded_by = models.CharField(max_length=100)
    download_count = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title

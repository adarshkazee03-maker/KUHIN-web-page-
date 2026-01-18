from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import timedelta


class SearchQuery(models.Model):
    """Track search queries for analytics and trending"""
    query = models.CharField(max_length=255, db_index=True)
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    last_searched = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Search Query'
        verbose_name_plural = 'Search Queries'
        ordering = ['-count', '-last_searched']
    
    def __str__(self):
        return f"{self.query} ({self.count})"


class ContentView(models.Model):
    """Track views for content to show trending items"""
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('blog', 'Blog Post'),
            ('news', 'News Update'),
            ('event', 'Event'),
            ('resource', 'Resource'),
            ('member', 'Member'),
            ('gallery', 'Gallery Image'),
        ]
    )
    object_id = models.IntegerField()
    view_count = models.IntegerField(default=0)
    weekly_views = models.IntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)
    weekly_reset_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Content View'
        verbose_name_plural = 'Content Views'
        unique_together = ('content_type', 'object_id')
        indexes = [
            models.Index(fields=['-weekly_views']),
            models.Index(fields=['-view_count']),
        ]
    
    def __str__(self):
        return f"{self.content_type} #{self.object_id} - {self.view_count} views"
    
    @classmethod
    def record_view(cls, content_type, object_id):
        """Record a view for content"""
        view, created = cls.objects.get_or_create(
            content_type=content_type,
            object_id=object_id
        )
        view.view_count += 1
        view.weekly_views += 1
        view.save()
        return view
    
    @classmethod
    def get_trending_content(cls, model_class, limit=5):
        """Get trending content based on weekly views"""
        content_type_map = {
            'BlogPost': 'blog',
            'NewsUpdate': 'news',
            'Event': 'event',
            'Resource': 'resource',
            'Member': 'member',
            'GalleryImage': 'gallery',
        }
        
        content_type_str = content_type_map.get(model_class.__name__, model_class.__name__.lower())
        
        # Reset weekly views if needed
        now = timezone.now().date()
        cls.objects.filter(
            content_type=content_type_str,
            weekly_reset_date__lt=now - timedelta(days=7)
        ).update(weekly_views=0, weekly_reset_date=now)
        
        return cls.objects.filter(
            content_type=content_type_str
        ).order_by('-weekly_views')[:limit]
    
    @classmethod
    def reset_weekly_views(cls):
        """Reset weekly view counts"""
        now = timezone.now().date()
        cls.objects.filter(
            weekly_reset_date__lt=now - timedelta(days=7)
        ).update(weekly_views=0, weekly_reset_date=now)


class UserRecommendation(models.Model):
    """Track user interactions for personalized recommendations"""
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('read', 'Read'),
        ('search', 'Search'),
    ]
    
    session_key = models.CharField(max_length=40, db_index=True)
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('blog', 'Blog Post'),
            ('news', 'News Update'),
            ('event', 'Event'),
            ('resource', 'Resource'),
            ('member', 'Member'),
        ]
    )
    object_id = models.IntegerField()
    interaction_type = models.CharField(max_length=10, choices=INTERACTION_TYPES, default='view')
    score = models.FloatField(default=1.0)  # Weight score for recommendation
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Recommendation'
        verbose_name_plural = 'User Recommendations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_key', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.session_key} - {self.content_type} #{self.object_id}"
    
    @classmethod
    def record_interaction(cls, session_key, content_type, object_id, interaction_type='view'):
        """Record user interaction for recommendations"""
        # Score weights for different interactions
        weights = {
            'view': 1.0,
            'click': 1.5,
            'read': 2.0,
            'search': 0.5,
        }
        
        return cls.objects.create(
            session_key=session_key,
            content_type=content_type,
            object_id=object_id,
            interaction_type=interaction_type,
            score=weights.get(interaction_type, 1.0)
        )

from django.contrib import admin
from .models import SearchQuery, ContentView, UserRecommendation


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'count', 'last_searched', 'created_at']
    list_filter = ['last_searched', 'created_at']
    search_fields = ['query']
    ordering = ['-count', '-last_searched']
    readonly_fields = ['created_at', 'last_searched']
    
    def has_add_permission(self, request):
        return False


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_id', 'view_count', 'weekly_views', 'last_viewed']
    list_filter = ['content_type', 'last_viewed']
    search_fields = ['object_id']
    ordering = ['-weekly_views', '-view_count']
    readonly_fields = ['content_type', 'object_id', 'view_count', 'weekly_views', 'last_viewed', 'weekly_reset_date']
    
    def has_add_permission(self, request):
        return False


@admin.register(UserRecommendation)
class UserRecommendationAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'content_type', 'object_id', 'interaction_type', 'score', 'created_at']
    list_filter = ['interaction_type', 'content_type', 'created_at']
    search_fields = ['session_key']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False

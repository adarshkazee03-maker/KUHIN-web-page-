from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'team', 'batch', 'role_in_project', 'is_active', 'display_order']
    list_filter = ['position', 'team', 'batch', 'is_active']
    search_fields = ['name', 'email', 'role_in_project', 'specialization']
    list_editable = ['display_order', 'is_active', 'team']
    ordering = ['team', 'display_order', 'name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'team', 'role_in_project', 'batch', 'specialization')
        }),
        ('Biography', {
            'fields': ('bio', 'achievements')
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'linkedin', 'github', 'twitter', 'website')
        }),
        ('Display Settings', {
            'fields': ('photo', 'display_order', 'is_active', 'join_date')
        }),
    )

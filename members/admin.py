from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'batch', 'role_in_project', 'is_active', 'display_order']
    list_filter = ['position', 'batch', 'is_active']
    search_fields = ['name', 'email', 'role_in_project', 'specialization']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order', 'name']

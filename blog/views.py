from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import BlogPost, Category

def blog_list(request):
    """Display list of published blog posts with optional category and search filtering"""
    blogs = BlogPost.objects.filter(status='published').order_by('-published_date', '-created_at')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    context = {
        'blogs': blogs,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'blogs/blog_list.html', context)

def blog_detail(request, slug):
    """Display detailed view of a single blog post"""
    blog = get_object_or_404(BlogPost, slug=slug, status='published')
    
    # Increment view count
    blog.views += 1
    blog.save(update_fields=['views'])
    
    # Get related blog posts from same category
    related_blogs = BlogPost.objects.filter(
        status='published',
        category=blog.category
    ).exclude(slug=slug).order_by('-published_date')[:3]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
    }
    return render(request, 'blogs/blog_detail.html', context)


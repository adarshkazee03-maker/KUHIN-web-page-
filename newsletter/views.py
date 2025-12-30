from django.shortcuts import render, get_object_or_404
from .models import NewsUpdate

def news_list(request):
    """Display list of active news updates"""
    news_updates = NewsUpdate.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'news_updates': news_updates,
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, slug):
    """Display detailed view of a single news update"""
    news = get_object_or_404(NewsUpdate, slug=slug, is_active=True)
    
    # Get related news updates
    related_news = NewsUpdate.objects.filter(
        is_active=True
    ).exclude(slug=slug).order_by('-created_at')[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/news_detail.html', context)


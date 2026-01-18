from django.shortcuts import render, get_object_or_404
from .models import NewsUpdate

def news_list(request):
    """
    Display list of all active news updates.
    
    Features:
    - Shows only active news items
    - Orders chronologically (newest first)
    - Displays news summaries and dates
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered news_list template with context
        
    Context:
        - news_updates: All active NewsUpdate objects ordered by created date
    """
    # Order by created_at descending to show newest first
    news_updates = NewsUpdate.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'news_updates': news_updates,
    }
    return render(request, 'news/news_list.html', context)

def news_detail(request, slug):
    """
    Display detailed view of a single news update with SEO optimization and sidebar.
    
    Features:
    - Shows full news content with rich formatting
    - Displays related news items for engagement
    - Includes sidebar with latest news
    - Adds breadcrumb navigation for SEO
    - Shows only active news items
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the news update
        
    Returns:
        HttpResponse: Rendered news_detail template with context
        HttpResponse: 404 if news update not found or inactive
        
    Context:
        - news: The requested NewsUpdate object
        - related_news: Up to 3 other recent news items
        - latest_news: Up to 5 newest news items for sidebar
        - breadcrumb_items: Navigation breadcrumbs for SEO
        
    Note:
        Only displays active news items (is_active=True).
        Related news helps users discover more content.
        Latest news in sidebar improves engagement and time on site.
    """
    news = get_object_or_404(NewsUpdate, slug=slug, is_active=True)
    
    # Get related news updates
    related_news = NewsUpdate.objects.filter(
        is_active=True
    ).exclude(slug=slug).order_by('-created_at')[:3]
    
    # Get all latest news for sidebar
    latest_news = NewsUpdate.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Prepare breadcrumb data with plain string URLs
    breadcrumb_items = [
        {'label': 'News & Updates', 'url': '/news/'},
        {'label': news.title, 'url': None}
    ]
    
    context = {
        'news': news,
        'related_news': related_news,
        'latest_news': latest_news,
        'breadcrumb_items': breadcrumb_items,
    }
    return render(request, 'news/news_detail.html', context)


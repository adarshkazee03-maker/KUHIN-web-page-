from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from datetime import datetime

from blog.models import BlogPost
from newsletter.models import NewsUpdate
from events.models import Event
from resources.models import Resource
from members.models import Member

from .models import SearchQuery, ContentView, UserRecommendation


def global_search(request):
    """Global search across all content types"""
    query = request.GET.get('q', '').strip()
    content_filter = request.GET.get('type', 'all')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    page = request.GET.get('page', 1)
    
    results = {
        'blogs': [],
        'news': [],
        'events': [],
        'resources': [],
        'members': [],
    }
    
    total_results = 0
    trending_searches = SearchQuery.objects.order_by('-count')[:10]
    
    if query:
        # Record search query
        search_obj, created = SearchQuery.objects.get_or_create(query=query)
        if not created:
            search_obj.count += 1
            search_obj.save()
        
        # Record user interaction
        if request.session.session_key:
            UserRecommendation.record_interaction(
                request.session.session_key,
                'search',
                0,
                'search'
            )
        
        # Build date filter
        date_filter_kwargs = {}
        if date_from:
            try:
                date_filter_kwargs['created_at__gte'] = datetime.strptime(date_from, '%Y-%m-%d').date()
            except ValueError:
                pass
        if date_to:
            try:
                date_filter_kwargs['created_at__lte'] = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Search blogs
        if content_filter in ['all', 'blog']:
            blog_results = BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(category__name__icontains=query),
                status='published',
                **date_filter_kwargs
            ).select_related('category', 'author').distinct()
            results['blogs'] = blog_results[:10]
            total_results += len(results['blogs'])
        
        # Search news
        if content_filter in ['all', 'news']:
            news_results = NewsUpdate.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query),
                is_active=True,
                **date_filter_kwargs
            ).distinct()
            results['news'] = news_results[:10]
            total_results += len(results['news'])
        
        # Search events
        if content_filter in ['all', 'event']:
            event_results = Event.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query),
                **date_filter_kwargs
            ).distinct()
            results['events'] = event_results[:10]
            total_results += len(results['events'])
        
        # Search resources
        if content_filter in ['all', 'resource']:
            resource_results = Resource.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query),
                **date_filter_kwargs
            ).select_related('category').distinct()
            results['resources'] = resource_results[:10]
            total_results += len(results['resources'])
        
        # Search members
        if content_filter in ['all', 'member']:
            member_results = Member.objects.filter(
                Q(name__icontains=query) |
                Q(position__icontains=query) |
                Q(bio__icontains=query) |
                Q(email__icontains=query),
                is_active=True
            ).distinct()
            results['members'] = member_results[:10]
            total_results += len(results['members'])
    
    context = {
        'query': query,
        'results': results,
        'total_results': total_results,
        'content_filter': content_filter,
        'date_from': date_from,
        'date_to': date_to,
        'trending_searches': trending_searches,
    }
    
    return render(request, 'search/search_results.html', context)


@require_http_methods(['GET'])
def autocomplete(request):
    """Autocomplete suggestions for search"""
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    # Get unique titles from recent searches
    recent_searches = SearchQuery.objects.filter(
        query__istartswith=query
    ).values_list('query', flat=True).order_by('-last_searched')[:5]
    suggestions.extend(recent_searches)
    
    # Get blog titles
    blog_titles = BlogPost.objects.filter(
        Q(title__icontains=query),
        status='published'
    ).values_list('title', flat=True)[:3]
    suggestions.extend(blog_titles)
    
    # Get event titles
    event_titles = Event.objects.filter(
        title__icontains=query
    ).values_list('title', flat=True)[:3]
    suggestions.extend(event_titles)
    
    # Get member names
    member_names = Member.objects.filter(
        Q(name__icontains=query),
        is_active=True
    ).values_list('name', flat=True)[:3]
    suggestions.extend(member_names)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for s in suggestions:
        if s not in seen:
            seen.add(s)
            unique_suggestions.append(s)
    
    return JsonResponse({'suggestions': unique_suggestions[:10]})


def trending_content(request):
    """Get trending content across all types"""
    trending = {
        'blogs': ContentView.get_trending_content(BlogPost, limit=5),
        'news': ContentView.get_trending_content(NewsUpdate, limit=5),
        'events': ContentView.get_trending_content(Event, limit=5),
        'resources': ContentView.get_trending_content(Resource, limit=5),
    }
    
    context = {
        'trending': trending,
        'page_title': 'Trending Content',
    }
    
    return render(request, 'search/trending.html', context)


def recommendations(request, content_type_str, object_id):
    """Get personalized recommendations based on similar content"""
    # Map content type strings to model classes
    content_type_map = {
        'blog': (BlogPost, 'category'),
        'news': (NewsUpdate, None),
        'event': (Event, None),
        'resource': (Resource, 'category'),
        'member': (Member, None),
    }
    
    if content_type_str not in content_type_map:
        return JsonResponse({'error': 'Invalid content type'}, status=400)
    
    model_class, category_field = content_type_map[content_type_str]
    
    try:
        obj = model_class.objects.get(pk=object_id)
    except model_class.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status=404)
    
    # Record view
    if request.session.session_key:
        ContentView.record_view(content_type_str, object_id)
        UserRecommendation.record_interaction(
            request.session.session_key,
            content_type_str,
            object_id,
            'view'
        )
    
    # Get similar content
    recommendations_list = []
    
    if category_field and hasattr(obj, category_field):
        category = getattr(obj, category_field)
        similar = model_class.objects.filter(
            **{f'{category_field}': category}
        ).exclude(pk=object_id)[:5]
        recommendations_list = list(similar)
    
    # If not enough recommendations from category, get trending
    if len(recommendations_list) < 5:
        trending = ContentView.get_trending_content(model_class, limit=5)
        trending_ids = [cv.object_id for cv in trending]
        remaining = model_class.objects.filter(
            pk__in=trending_ids
        ).exclude(pk=object_id)
        recommendations_list.extend(remaining)
    
    context = {
        'recommendations': recommendations_list[:5],
        'content_type': content_type_str,
        'original_content': obj,
    }
    
    return render(request, 'search/recommendations.html', context)


@require_http_methods(['GET'])
def quick_stats(request):
    """API endpoint for quick stats"""
    stats = {
        'total_blogs': BlogPost.objects.filter(status='published').count(),
        'total_news': NewsUpdate.objects.filter(is_active=True).count(),
        'total_events': Event.objects.count(),
        'total_resources': Resource.objects.count(),
        'total_members': Member.objects.filter(is_active=True).count(),
        'trending_searches': list(
            SearchQuery.objects.order_by('-count')[:5].values('query', 'count')
        ),
    }
    
    return JsonResponse(stats)

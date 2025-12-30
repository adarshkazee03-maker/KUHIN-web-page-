from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from events.models import Event
from members.models import Member
from resources.models import Resource
from blog.models import BlogPost
from newsletter.models import NewsUpdate
from .models import ContactMessage
from .forms import ContactForm
from .email_utils import (
    get_client_ip,
    check_rate_limit,
    increment_rate_limit,
    send_contact_email,
    send_confirmation_email
)

def home(request):
    # Get upcoming events
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date')[:3]
    
    # Get latest published blog posts
    latest_blogs = BlogPost.objects.filter(status='published').order_by('-published_date', '-created_at')[:3]
    
    # Get latest active news updates
    latest_news = NewsUpdate.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Get counts for stats
    member_count = Member.objects.count()
    event_count = Event.objects.count()
    resource_count = Resource.objects.count()
    blog_count = BlogPost.objects.filter(status='published').count()
    news_count = NewsUpdate.objects.filter(is_active=True).count()
    
    context = {
        'upcoming_events': upcoming_events,
        'latest_blogs': latest_blogs,
        'latest_news': latest_news,
        'member_count': member_count,
        'event_count': event_count,
        'resource_count': resource_count,
        'blog_count': blog_count,
        'news_count': news_count,
    }
    return render(request, 'home/index.html', context)

def about(request):
    return render(request, 'about.html')

def team(request):
    executive_committee = Member.objects.filter(team='Executive Committee').order_by('display_order', 'name')
    advisory_board = Member.objects.filter(team='Advisory Board').order_by('display_order', 'name')
    all_members = Member.objects.all()
    return render(request, 'team.html', {
        'executive_committee': executive_committee,
        'advisory_board': advisory_board,
        'members': all_members
    })

def events(request):
    upcoming = Event.objects.filter(status='upcoming').order_by('date')
    past = Event.objects.filter(status='completed').order_by('-date')
    return render(request, 'events.html', {
        'upcoming_events': upcoming,
        'past_events': past
    })

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    # Get related upcoming events
    related_events = Event.objects.filter(status='upcoming').exclude(slug=slug).order_by('date')[:3]
    return render(request, 'event_detail.html', {
        'event': event,
        'related_events': related_events
    })

def gallery(request):
    from gallery.models import GalleryImage
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

def resources(request):
    from resources.models import Resource
    resources_list = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources_list})

def resource_detail(request, slug):
    from resources.models import Resource
    resource = get_object_or_404(Resource, slug=slug)
    # Get related resources from same category
    related_resources = Resource.objects.filter(category=resource.category).exclude(slug=slug)[:4]
    return render(request, 'resource_detail.html', {
        'resource': resource,
        'related_resources': related_resources
    })

def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'member_detail.html', {'member': member})

def contact(request):
    """
    Handle contact form submissions with email sending and rate limiting
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Get client IP for rate limiting
            client_ip = get_client_ip(request)
            
            # Check rate limit
            is_allowed, remaining_messages, current_count = check_rate_limit(client_ip)
            
            if not is_allowed:
                messages.error(
                    request,
                    f'You have reached the message limit (5 messages per hour). Please try again later.'
                )
                return redirect('contact')
            
            # Extract validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']
            
            # Try to send the email
            email_result = send_contact_email(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
                request=request
            )
            
            if email_result['success']:
                # Increment rate limit counter
                increment_rate_limit(client_ip)
                
                # Send confirmation email to user
                confirmation_result = send_confirmation_email(email, name)
                
                # Show success message
                messages.success(
                    request,
                    email_result['message']
                )
                
                # Clear form by redirecting
                return redirect('contact')
            else:
                # Email sending failed
                messages.error(request, email_result['error'])
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        # GET request - display empty form
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)

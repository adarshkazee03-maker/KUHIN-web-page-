from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
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
from homepage_features.views import enhanced_home

def home(request):
    """
    Display enhanced homepage with interactive features.
    
    Uses the enhanced_home view from homepage_features app which includes:
    - Active announcements carousel
    - Event countdown timer
    - Member spotlights
    - Achievements section
    - Testimonials
    - Activity feed
    - Trending content
    - Statistics counters
    """
    return enhanced_home(request)

def about(request):
    """
    Display the about page with organization information.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered about template
    """
    return render(request, 'about.html')

def team(request):
    """
    Display team members organized by role.
    
    Features:
    - Separates executive committee from advisory board
    - Maintains display order
    - Shows all members on the page
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered team template with context
        
    Context:
        - executive_committee: Members in executive roles
        - advisory_board: Members in advisory roles
        - members: All members (for full listing)
    """
    executive_committee = Member.objects.filter(team='Executive Committee').order_by('display_order', 'name')
    advisory_board = Member.objects.filter(team='Advisory Board').order_by('display_order', 'name')
    all_members = Member.objects.all()
    return render(request, 'team.html', {
        'executive_committee': executive_committee,
        'advisory_board': advisory_board,
        'members': all_members
    })

def events(request):
    """
    Display upcoming and past events.
    
    Features:
    - Separates upcoming events from completed/past events
    - Sorts chronologically (upcoming: ascending, past: descending)
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered events template with context
        
    Context:
        - upcoming_events: Events scheduled for the future
        - past_events: Completed events (sorted newest first)
    """
    upcoming = Event.objects.filter(status='upcoming').order_by('date')
    past = Event.objects.filter(status='completed').order_by('-date')
    return render(request, 'events.html', {
        'upcoming_events': upcoming,
        'past_events': past
    })

def event_detail(request, slug):
    """
    Display detailed view of a single event with SEO optimization.
    
    Features:
    - Shows event details including date, location, description
    - Displays related upcoming events
    - Includes breadcrumb navigation
    - Simple and efficient query execution
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the event
        
    Returns:
        HttpResponse: Rendered event_detail template with context
        HttpResponse: 404 if event not found
        
    Context:
        - event: The requested Event object
        - related_events: Up to 3 upcoming events
        - breadcrumb_items: Navigation breadcrumbs for SEO
        
    Note:
        Location is stored as a CharField, not a foreign key.
        Related events help with engagement and time-on-site metrics.
    """
    # Get event by slug
    # location is a CharField, not a relational field
    event = get_object_or_404(Event, slug=slug)
    
    # Get related upcoming events
    related_events = Event.objects.filter(
        status='upcoming'
    ).exclude(slug=slug).order_by('date')[:3]
    
    # Prepare breadcrumb data
    breadcrumb_items = [
        {'label': 'Events', 'url': '/events/'},
        {'label': event.title, 'url': None}
    ]
    
    return render(request, 'event_detail.html', {
        'event': event,
        'related_events': related_events,
        'breadcrumb_items': breadcrumb_items,
    })

def gallery(request):
    """
    Display gallery with all uploaded images.
    
    Features:
    - Shows all gallery images
    - Maintains display order
    - Displays image metadata (title, description)
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered gallery template with context
        
    Context:
        - images: All gallery images ordered by date
    """
    from gallery.models import GalleryImage
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

def resources(request):
    """
    Display all available resources for the community.
    
    Features:
    - Lists all published resources
    - Maintains display order
    - Shows resource metadata
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered resources template with context
        
    Context:
        - resources: All available resources
    """
    from resources.models import Resource
    resources_list = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources_list})

def resource_detail(request, slug):
    """
    Display detailed view of a single resource with SEO optimization.
    
    Features:
    - Shows resource content with rich formatting
    - Displays related resources from same category
    - Includes breadcrumb navigation
    - Optimizes database queries with select_related
    
    Args:
        request (HttpRequest): The HTTP request object
        slug (str): URL slug of the resource
        
    Returns:
        HttpResponse: Rendered resource_detail template with context
        HttpResponse: 404 if resource not found
        
    Context:
        - resource: The requested Resource object
        - related_resources: Up to 4 resources from same category
        - breadcrumb_items: Navigation breadcrumbs for SEO
        
    Note:
        Uses select_related('category') to optimize N+1 query problem.
        Breadcrumbs help users navigate and improve SEO ranking.
    """
    from resources.models import Resource
    
    resource = get_object_or_404(Resource, slug=slug)
    
    # Get related resources from same category with select_related
    related_resources = Resource.objects.select_related('category').filter(
        category=resource.category
    ).exclude(slug=slug).order_by('-uploaded_at')[:4]
    
    # Prepare breadcrumb data
    breadcrumb_items = [
        {'label': 'Resources', 'url': '/resources/'},
        {'label': resource.title, 'url': None}
    ]
    
    return render(request, 'resource_detail.html', {
        'resource': resource,
        'related_resources': related_resources,
        'breadcrumb_items': breadcrumb_items,
    })

def member_detail(request, pk):
    """
    Display detailed profile of a team member with SEO optimization.
    
    Features:
    - Shows team member profile information
    - Displays member role and biography
    - Includes breadcrumb navigation
    - Links back to team listing page
    
    Args:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key ID of the Member object
        
    Returns:
        HttpResponse: Rendered member_detail template with context
        HttpResponse: 404 if member not found
        
    Context:
        - member: The requested Member object with all profile data
        - breadcrumb_items: Navigation breadcrumbs for SEO
        
    Note:
        Breadcrumbs improve SEO and user navigation experience.
        Member object includes name, role, bio, image, and contact info.
    """
    member = get_object_or_404(Member, pk=pk)
    
    # Prepare breadcrumb data
    breadcrumb_items = [
        {'label': 'Team', 'url': '/team/'},
        {'label': member.name, 'url': None}
    ]
    
    return render(request, 'member_detail.html', {
        'member': member,
        'breadcrumb_items': breadcrumb_items,
    })

def contact(request):
    """
    Display and process contact form submissions with email sending and rate limiting.
    
    Features:
    - Validates form data before submission
    - Implements rate limiting (5 messages per hour per IP)
    - Sends email notifications to organization
    - Sends confirmation email to user
    - Provides user feedback via messages framework
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered contact template with context on GET/error
        HttpResponseRedirect: Redirects to contact on successful submission
        
    Context:
        - form: Contact form instance for template rendering
        
    Form Fields:
        - name: Contact person's name (required)
        - email: Contact person's email (required)
        - subject: Message subject (required)
        - message: Message body (required)
        
    Note:
        Rate limiting is tracked by client IP address.
        Confirmation emails are sent from DEFAULT_FROM_EMAIL.
        Email sending failures display friendly error messages to user.
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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from events.models import Event
from members.models import Member
from resources.models import Resource
from .models import ContactMessage

def home(request):
    # Get upcoming events
    upcoming_events = Event.objects.filter(status='upcoming').order_by('date')[:3]
    
    # Get counts for stats
    member_count = Member.objects.count()
    event_count = Event.objects.count()
    resource_count = Resource.objects.count()
    
    context = {
        'upcoming_events': upcoming_events,
        'member_count': member_count,
        'event_count': event_count,
        'resource_count': resource_count,
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
    # Increment download count
    resource.download_count += 1
    resource.save(update_fields=['download_count'])
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'contact.html')

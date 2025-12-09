from django.shortcuts import render
from events.models import Event
from members.models import Member
from resources.models import Resource

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

def gallery(request):
    from gallery.models import GalleryImage
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})

def resources(request):
    from resources.models import Resource
    resources_list = Resource.objects.all()
    return render(request, 'resources.html', {'resources': resources_list})

def contact(request):
    return render(request, 'contact.html')

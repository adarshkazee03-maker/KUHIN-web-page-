# KUHIN Website Project

## Kathmandu University Health Informatics Club

A comprehensive Django-based website for KUHIN with features for team management, event tracking, gallery, and resources.

### Project Setup

#### Development Setup
1. Clone the repository
2. Create virtual environment: `python3 -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run development server: `python manage.py runserver`

#### Project Structure
```
├── home/                    # Main app with core views
├── members/                 # Team member management
├── events/                  # Event management
├── gallery/                 # Image gallery
├── resources/               # Health informatics resources
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── media/
│   ├── members/
│   └── events/
├── templates/
│   ├── home/
│   ├── base.html
│   ├── about.html
│   ├── team.html
│   ├── events.html
│   ├── gallery.html
│   ├── resources.html
│   ├── contact.html
│   └── ...
├── kuhin_project/           # Main Django project
├── manage.py
└── requirements.txt
```

### Features
- ✅ Club information pages
- ✅ Team member profiles with photos
- ✅ Event management (upcoming & past)
- ✅ Resource library
- ✅ Image gallery
- ✅ Contact system
- ✅ Mobile responsive design
- ✅ Admin panel for content management

### Database Models

#### Member
- Name, Position, Role, Batch
- Bio, Photo, Email
- LinkedIn & GitHub links
- Display order

#### Event
- Title, Description, Type
- Date, Time, Location
- Image, Registration link
- Is upcoming status

#### GalleryImage
- Title, Image, Category
- Description, Upload date

#### Resource
- Title, Description, Category
- Link, Uploaded by, Date

### Access Points
- **Development server:** http://127.0.0.1:8000
- **Admin panel:** http://127.0.0.1:8000/admin
- **Default admin:** admin / kuhin2024

### Main Routes
- `/` - Home page
- `/about/` - About KUHIN
- `/team/` - Team members
- `/events/` - Events & activities
- `/gallery/` - Image gallery
- `/resources/` - Resource library
- `/contact/` - Contact form
- `/admin/` - Admin panel

### Technology Stack
- **Backend:** Django 6.0
- **Frontend:** Bootstrap 5, HTML5, CSS3, JavaScript
- **Database:** SQLite (dev), PostgreSQL (production)
- **Image Processing:** Pillow
- **Server:** Gunicorn (production)

### Customization

#### Adding Team Members
1. Go to admin panel: `/admin/`
2. Click on "Members"
3. Click "Add Member"
4. Fill in the details and upload photo
5. Save

#### Creating Events
1. Go to admin panel: `/admin/`
2. Click on "Events"
3. Click "Add Event"
4. Fill event details, set date & time
5. Toggle "Is upcoming" status
6. Save

#### Adding Resources
1. Go to admin panel: `/admin/`
2. Click on "Resources"
3. Click "Add Resource"
4. Fill title, description, category
5. Add external link
6. Save

### Deployment

#### PythonAnywhere
1. Create account at pythonanywhere.com
2. Clone repository to your account
3. Create virtual environment
4. Configure web app
5. Set up static files
6. Deploy and test

#### Environment Variables (Production)
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
```

### Team Structure
- **Senior 1** - Project Lead
- **Senior 2** - Backend Development
- **Senior 3** - Frontend Development
- **Junior A** - Design & Media
- **Junior B** - Content & Research
- **Junior C** - Documentation & Testing

### Development Notes
- Use Bootstrap 5 for responsive design
- Follow Django best practices
- Update migrations when models change
- Test on multiple browsers
- Keep documentation updated

### Contributing
1. Create a new branch for features
2. Test thoroughly before pushing
3. Update documentation
4. Submit pull request

### License
This project is developed by KUHIN for Kathmandu University.

### Support
For issues or suggestions, contact: contact@kuhin.edu.np

---
**Built with Django by KUHIN Tech Team 2024**
# KUHIN Professional Website

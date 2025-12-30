# KUHIN Website Project - Complete Architecture

## 📋 Project Overview

**Project Name**: KUHIN Website  
**Organization**: Kathmandu University Health Informatics Club  
**Framework**: Django 4.2.27  
**Language**: Python 3.13  
**Database**: SQLite (Development)  
**Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript  
**Status**: Production Ready ✅

---

## 🏗️ Project Structure

```
KUHIN-web-page/
├── kuhin_project/              # Project configuration
│   ├── settings.py            # Django settings (DB, apps, middleware, email, cache, logging)
│   ├── urls.py                # Main URL router
│   ├── asgi.py                # ASGI config (production)
│   └── wsgi.py                # WSGI config (production)
│
├── home/                       # Main/Home app
│   ├── views.py               # Core views (home, contact, resources, gallery)
│   ├── urls.py                # Home app routing
│   ├── forms.py               # Contact form with validation
│   ├── email_utils.py         # Email sending + rate limiting
│   ├── models.py              # ContactMessage model (legacy)
│   ├── admin.py               # Admin interface
│   └── migrations/            # Database migrations
│
├── members/                    # Team/Member management
│   ├── models.py              # Member model
│   ├── views.py               # Member views
│   ├── admin.py               # Member admin
│   └── migrations/
│
├── events/                     # Event management
│   ├── models.py              # Event, EventRegistration models
│   ├── views.py               # Event views
│   ├── admin.py               # Event admin
│   └── migrations/
│
├── blog/                       # Blog system
│   ├── models.py              # BlogPost, Category models
│   ├── views.py               # Blog views with search/filter
│   ├── urls.py                # Blog routing
│   ├── admin.py               # Blog admin
│   └── migrations/
│
├── newsletter/                 # News Updates system
│   ├── models.py              # Subscriber, NewsUpdate models
│   ├── views.py               # News views
│   ├── urls.py                # News routing
│   ├── admin.py               # News admin
│   └── migrations/
│
├── gallery/                    # Image Gallery
│   ├── models.py              # GalleryCategory, GalleryImage models
│   ├── views.py               # Gallery views
│   ├── admin.py               # Gallery admin
│   └── migrations/
│
├── resources/                  # External Resources/Links
│   ├── models.py              # ResourceCategory, Resource models
│   ├── views.py               # Resource views
│   ├── admin.py               # Resource admin (file & download removed)
│   └── migrations/
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template (nav, footer)
│   ├── home/
│   │   └── index.html         # Homepage
│   ├── about.html             # About page
│   ├── contact.html           # Contact form page
│   ├── team.html              # Team/Members page
│   ├── blogs/
│   │   ├── blog_list.html     # Blog listing
│   │   └── blog_detail.html   # Individual blog post
│   ├── news/
│   │   ├── news_list.html     # News listing
│   │   └── news_detail.html   # Individual news article
│   ├── events.html            # Events page
│   ├── event_detail.html      # Individual event
│   ├── gallery.html           # Gallery page
│   ├── resources.html         # Resources page
│   ├── resource_detail.html   # Individual resource
│   └── member_detail.html     # Individual member profile
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet (1371 lines)
│   └── js/
│       └── script.js          # Frontend JavaScript
│
├── logs/                       # Application logs
│   └── kuhin.log              # Email & system logs
│
├── .env.example               # Environment variables template
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
├── db.sqlite3                 # Development database
├── start.sh                   # Startup script
├── README.md                  # Project documentation
├── SETUP.md                   # Setup instructions
└── PROJECT_STATUS.txt         # Project status

```

---

## 🎯 Core Features

### 1. **Homepage** (`home/views.py`)
- **URL**: `/`
- **Features**:
  - Latest 3 blog posts
  - Latest 5 news updates
  - Team statistics (members, events, resources)
  - Upcoming 3 events
  - Quick access to all sections
  - Professional hero section
- **Template**: `home/index.html`

### 2. **Team Management** (`members/`)
- **URL**: `/team/`, `/member/<id>/`
- **Features**:
  - Team member profiles
  - Member photos
  - Member roles/positions
  - Member details page
  - Admin management
- **Model**: `Member`
- **Fields**: name, email, phone, position, bio, photo, joined_date, is_active

### 3. **Event Management** (`events/`)
- **URL**: `/events/`, `/event/<id>/`
- **Features**:
  - Event listings
  - Event details with registration tracking
  - Event status (upcoming, ongoing, completed)
  - Event registration management
  - Admin interface with filtering
- **Models**: `Event`, `EventRegistration`
- **Event Fields**: title, slug, description, date, time, location, status, image

### 4. **Blog System** (`blog/`)
- **URL**: `/blog/`, `/blog/<slug>/`
- **Features**:
  - Blog post creation and management
  - Category-based organization
  - Full-text search functionality
  - Category filtering
  - Rich text editor (CKEditor)
  - Blog post view counter
  - Related posts (same category)
  - Featured posts display
  - Featured images
- **Models**: `BlogPost`, `Category`
- **BlogPost Fields**: title, slug, content, author, category, featured_image, status, views, created_at, updated_at
- **Admin Features**: Search, filter by status/category, featured toggle

### 5. **News Updates** (`newsletter/`)
- **URL**: `/news/`, `/news/<slug>/`
- **Features**:
  - News article publishing
  - Rich text descriptions
  - Active/Inactive toggle
  - Slug-based URLs
  - Related news display (same category)
  - Timeline-style layout
  - Featured news section
  - Homepage integration
- **Models**: `NewsUpdate`, `Subscriber`
- **NewsUpdate Fields**: title, slug, description, is_active, created_at, updated_at
- **Admin Features**: Date hierarchy, list filtering, quick activate/deactivate

### 6. **Gallery** (`gallery/`)
- **URL**: `/gallery/`
- **Features**:
  - Image gallery with categories
  - Responsive grid layout
  - Gallery categories
  - Image management
  - Thumbnail generation
- **Models**: `GalleryCategory`, `GalleryImage`
- **Image Fields**: title, image, category, uploaded_at, description

### 7. **Resources** (`resources/`)
- **URL**: `/resources/`, `/resources/<slug>/`
- **Features** (UPDATED):
  - External link sharing (no file downloads)
  - Resource categorization
  - Resource types (Document, External Link, Video, Tool)
  - Thumbnail support
  - Tags for organization
  - Featured resources
  - ❌ File uploads removed
  - ❌ Download tracking removed
- **Models**: `ResourceCategory`, `Resource`
- **Resource Fields**: title, slug, description, category, resource_type, external_link, thumbnail, uploaded_by, is_featured, tags

### 8. **Contact Us** (`home/forms.py`, `home/email_utils.py`)
- **URL**: `/contact/`
- **Features**:
  - Contact form with comprehensive validation
  - Email sending to admin (kuhin@ku.edu.np)
  - Automatic confirmation emails to users
  - Rate limiting (5 messages/hour per IP)
  - Spam detection and prevention
  - Full-text and regex validation
  - Temporary email blocking
  - Error logging
  - Console and SMTP email backends
  - Form error display
- **Form Fields**: name, email, subject, message
- **Validations**:
  - Name: 2-100 chars, letters only, requires full name
  - Email: Valid RFC 5322 format, blocks disposable domains
  - Subject: 3-200 chars, min 2 words
  - Message: 10-5000 chars, 5+ words, spam detection
- **Security**: CSRF token, rate limiting, input validation, spam patterns

---

## 🗄️ Database Models

### Member Model
```python
- id (Primary Key)
- name (CharField, 100)
- email (EmailField)
- phone (CharField, 20)
- position (CharField, 100)
- bio (TextField)
- photo (ImageField)
- joined_date (DateField)
- is_active (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Event Model
```python
- id (Primary Key)
- title (CharField, 200)
- slug (SlugField)
- description (RichTextField)
- date (DateField)
- time (TimeField)
- location (CharField, 200)
- status (CharField: upcoming/ongoing/completed)
- image (ImageField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### BlogPost Model
```python
- id (Primary Key)
- title (CharField, 200)
- slug (SlugField, unique)
- content (RichTextField via CKEditor)
- author (CharField, 100)
- category (ForeignKey to Category)
- featured_image (ImageField)
- status (CharField: draft/published)
- views (IntegerField, default=0)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Category Model (Blog)
```python
- id (Primary Key)
- name (CharField, 100)
- slug (SlugField, unique)
- description (TextField)
- icon (CharField, 50)
```

### NewsUpdate Model
```python
- id (Primary Key)
- title (CharField, 200)
- slug (SlugField, unique)
- description (RichTextField)
- is_active (BooleanField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

### Subscriber Model
```python
- id (Primary Key)
- email (EmailField, unique)
- name (CharField, 100, blank=True)
- subscribed_at (DateTimeField)
- is_active (BooleanField)
```

### GalleryImage Model
```python
- id (Primary Key)
- title (CharField, 200)
- image (ImageField)
- category (ForeignKey to GalleryCategory)
- description (TextField, blank=True)
- uploaded_at (DateTimeField)
```

### GalleryCategory Model
```python
- id (Primary Key)
- name (CharField, 100)
- slug (SlugField, unique)
- icon (CharField, 50)
```

### Resource Model
```python
- id (Primary Key)
- title (CharField, 200)
- slug (SlugField, unique)
- description (RichTextField)
- category (ForeignKey to ResourceCategory)
- resource_type (CharField: document/link/video/tool)
- external_link (URLField, blank=True)
- thumbnail (ImageField, blank=True)
- uploaded_by (CharField, 100)
- is_featured (BooleanField)
- tags (CharField, 200, blank=True)
- uploaded_at (DateTimeField)
- updated_at (DateTimeField)
```

### ResourceCategory Model
```python
- id (Primary Key)
- name (CharField, 100)
- slug (SlugField, unique)
- description (TextField)
- icon (CharField, 50)
```

### ContactMessage Model (Legacy)
```python
- id (Primary Key)
- name (CharField, 100)
- email (EmailField)
- subject (CharField, 200)
- message (TextField)
- created_at (DateTimeField)
```

---

## 🎨 Frontend Components

### Navigation & Footer
- **File**: `templates/base.html`
- **Navigation Menu**: Home → Team → Events → News → Gallery → Resources → Blog → Contact → About
- **Footer**: 4 columns (KUHIN Info, Quick Links, Connect, Get in Touch)
- **Social Links**: Facebook, Instagram, Twitter, LinkedIn
- **Contact**: Email, Phone, Address

### Homepage
- **Hero Section**: Main banner with KUHIN branding
- **Latest Blogs**: 3-post grid with thumbnails
- **Latest News**: 5-update timeline
- **Statistics**: Member count, events, resources, galleries
- **CTA Buttons**: Quick navigation to all sections

### Styling
- **Framework**: Bootstrap 5
- **Custom CSS**: 1371 lines of custom styling
- **Responsive**: Mobile-first, works on all devices
- **Colors**: Professional color scheme (purple, blue gradients)
- **Icons**: Font Awesome 6
- **Animations**: Smooth transitions, hover effects
- **Card Layouts**: Professional card-based design

---

## 🔐 Security Features

### Form Validation
- **Contact Form**:
  - CSRF token protection
  - Email format validation
  - Temporary email blocking
  - Spam keyword detection
  - Character limit enforcement
  - Repeated character detection
  - HTML/JavaScript injection prevention

### Rate Limiting
- **IP-based**: Blocks >5 messages/hour per IP
- **Cache-backed**: Django LocMemCache
- **No DB overhead**: In-memory tracking
- **Automatic reset**: 1-hour window

### Email Security
- **SMTP**: Configurable via environment variables
- **No hardcoded credentials**: All from .env file
- **Reply-to field**: Sender can respond directly
- **Logging**: All email operations logged
- **Error handling**: Graceful failures with user messages

### Admin Security
- **Django Admin**: Restricted to superusers
- **Read-only fields**: Auto-protected
- **List filters**: Safe filtering
- **Search fields**: Indexed searching
- **Custom permissions**: Per-model access control

---

## 📧 Email System

### Components
- **EmailMessage**: Django's email class
- **Backends**: Console (dev) + SMTP (production)
- **Rate Limiting**: 5 messages per IP per hour
- **Logging**: File + console logging
- **Queue**: No async (synchronous sending)

### Email Types
1. **Contact Email** (to admin)
   - User details + message
   - Reply-to set to user email
   - IP address and timestamp logged

2. **Confirmation Email** (to user)
   - Receipt acknowledgment
   - Professional template
   - Auto-reply from noreply@kuhin.ku.edu.np

### Configuration
- **Settings**: Email config in `settings.py`
- **Env Variables**: SMTP details from `.env`
- **Logging**: `logs/kuhin.log`
- **Cache**: LocMemCache for rate limiting

---

## 📦 Technology Stack

### Backend
- **Framework**: Django 4.2.27
- **Language**: Python 3.13
- **Database**: SQLite (dev) / PostgreSQL (production-ready)
- **ORM**: Django ORM
- **Server**: Gunicorn (production)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Responsive design, animations
- **Bootstrap 5**: UI framework
- **Font Awesome 6**: Icons
- **JavaScript**: Vanilla JS, no jQuery
- **CKEditor**: Rich text editing for blog/news

### Dependencies
```
Django==4.2.27
Pillow==11.3.0 (Image handling)
django-ckeditor==6.7.3 (Rich text editor)
django-crispy-forms==2.5 (Form styling)
crispy-bootstrap5==0.7 (Bootstrap integration)
django-widget-tweaks==1.5.0 (Form widgets)
python-decouple==3.8 (Environment variables)
gunicorn==20.1.0 (WSGI server)
psycopg2-binary==2.9.6 (PostgreSQL driver)
```

---

## 🔄 URL Routing

### Main Routes
| URL | Handler | Purpose |
|-----|---------|---------|
| `/` | `home()` | Homepage |
| `/team/` | `team()` | Team listing |
| `/member/<id>/` | `member_detail()` | Member profile |
| `/events/` | `events()` | Events listing |
| `/event/<id>/` | `event_detail()` | Event details |
| `/blog/` | `blog_list()` | Blog listing |
| `/blog/<slug>/` | `blog_detail()` | Blog post |
| `/news/` | `news_list()` | News listing |
| `/news/<slug>/` | `news_detail()` | News article |
| `/gallery/` | `gallery()` | Image gallery |
| `/resources/` | `resources()` | Resources listing |
| `/resources/<slug>/` | `resource_detail()` | Resource details |
| `/contact/` | `contact()` | Contact form |
| `/about/` | (static template) | About page |
| `/admin/` | Django Admin | Admin panel |

---

## 📊 Admin Panel Features

### Available Models
1. **Members**: Create, edit, delete team members
2. **Events**: Manage events and registrations
3. **Event Registrations**: View, filter registrations
4. **Blog Posts**: Write, edit, publish, feature blogs
5. **Blog Categories**: Organize blog content
6. **News Updates**: Publish news articles
7. **Subscribers**: Manage newsletter subscribers
8. **Gallery Images**: Upload and manage gallery
9. **Gallery Categories**: Organize gallery
10. **Resources**: Manage external resources
11. **Resource Categories**: Organize resources
12. **Contact Messages**: View contact submissions

### Admin Features
- **Search**: Full-text search on key fields
- **Filtering**: Filter by date, status, category
- **Sorting**: Click column headers to sort
- **Bulk Actions**: Edit multiple items
- **Read-only fields**: Auto, timestamps protected
- **Date hierarchy**: Navigate by date
- **Quick edit**: Edit directly in list view
- **Admin actions**: Custom actions per model

---

## 📝 Configuration

### Settings (`kuhin_project/settings.py`)
- **Debug Mode**: Toggle dev/prod
- **Allowed Hosts**: Domain configuration
- **Database**: SQLite/PostgreSQL support
- **Email Backend**: Console/SMTP
- **Cache**: LocMemCache (in-memory)
- **Logging**: File + console handlers
- **Static Files**: CSS, JS, images
- **Media Files**: Uploads directory
- **Security**: CSRF, XFrame options

### Environment Variables (`.env.example`)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

DEFAULT_FROM_EMAIL=noreply@kuhin.ku.edu.np
CONTACT_EMAIL_RECIPIENT=kuhin@ku.edu.np
```

---

## 🚀 Deployment Ready

### Production Checklist
- ✅ Static files configuration
- ✅ Media files handling
- ✅ Database migrations
- ✅ Email configuration
- ✅ Logging setup
- ✅ Security settings
- ✅ Environment variables
- ✅ Error handling
- ✅ Rate limiting
- ✅ CSRF protection

### Deployment Options
- **Heroku**: With Procfile
- **AWS**: EC2 with RDS
- **DigitalOcean**: App Platform
- **PythonAnywhere**: Easy Django hosting
- **VPS**: Any Linux with Gunicorn + Nginx

---

## 📚 Documentation Files

1. **README.md** - Project overview and setup
2. **SETUP.md** - Detailed setup instructions
3. **PROJECT_STATUS.txt** - Current project status
4. **CONTACT_FEATURE_GUIDE.md** - Email system guide (1000+ lines)
5. **CONTACT_IMPLEMENTATION_SUMMARY.md** - Contact feature details
6. **.env.example** - Environment variables template
7. **PROJECT_ARCHITECTURE.md** - This file

---

## 🎯 Recent Updates (Current Session)

1. ✅ **Blog & News System** - Complete with models, views, URLs, templates, styling
2. ✅ **Navigation & Footer** - Reordered menu, added Blog/News links, professional footer
3. ✅ **Contact Email Feature** - Form validation, rate limiting, SMTP support
4. ✅ **Enhanced Validations** - Stronger email validation, spam detection, disposable email blocking
5. ✅ **Resource Management** - Removed file uploads and download tracking
6. ✅ **Newsletter Cleanup** - Removed Newsletter model, kept NewsUpdate only

---

## 📈 Project Statistics

| Metric | Count |
|--------|-------|
| Python Files | 50+ |
| Templates | 15+ |
| Models | 11 |
| Admin Classes | 13 |
| CSS Lines | 1371 |
| Documentation Files | 7 |
| Total Routes | 20+ |
| Installed Apps | 11 |
| Middleware | 6 |
| Static Files | Multiple |
| Media Folders | Multiple |

---

## 🎓 Architecture Highlights

### Separation of Concerns
- **Apps**: Each feature has its own app (blog, events, members, etc.)
- **Models**: Data layer separated from business logic
- **Views**: Request handlers for each feature
- **Templates**: HTML separated from Python
- **Static Files**: CSS/JS in separate folders

### Scalability
- **Modular Design**: Add new apps without modifying core
- **Database**: Easy to migrate to PostgreSQL
- **Caching**: Built-in caching for rate limiting
- **Email**: Queue-ready for async jobs
- **Static Files**: CDN-ready configuration

### Maintainability
- **Clear Structure**: Organized by feature
- **Documentation**: Comprehensive guides
- **Admin Interface**: Easy content management
- **Logging**: Track errors and email operations
- **Security**: Built-in protections

---

**Last Updated**: December 30, 2025  
**Status**: Production Ready ✅  
**Maintained By**: KUHIN Development Team

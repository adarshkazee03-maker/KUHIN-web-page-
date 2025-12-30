# Contact Us Email Feature - Implementation Summary

## 🎯 Feature Overview

The Contact Us email feature enables KUHIN Club website visitors to send secure, validated messages directly to the admin email with:
- **Rate limiting**: 5 messages per IP per hour
- **Spam detection**: Blocks common spam phrases
- **Form validation**: Comprehensive field validation
- **Email confirmation**: Auto-replies to users
- **Error handling**: Graceful error messages and logging
- **Security**: CSRF protection, input validation, environment-based credentials
- **Development/Production modes**: Console backend for dev, SMTP for production

---

## 📋 Files Created

### 1. `home/forms.py` (119 lines)
**Purpose**: Contact form with comprehensive validation

**Form Class**: `ContactForm`
- **Fields**:
  - `name`: 2-100 chars, letters/spaces/hyphens/apostrophes only
  - `email`: Valid RFC 5322 format, max 254 chars
  - `subject`: 3-200 characters
  - `message`: 10-5000 chars, spam detection enabled

- **Validation Methods**:
  - `clean_name()`: Restricts to safe characters only
  - `clean_email()`: Format validation + lowercase normalization
  - `clean_subject()`: Length validation
  - `clean_message()`: Length + spam keyword detection (viagra, casino, lottery, click here, etc.)

- **Bootstrap Integration**: All fields use `form-control` class and have `aria-label` attributes

---

### 2. `home/email_utils.py` (186 lines)
**Purpose**: Email sending and rate limiting utilities

**Key Functions**:

#### `get_client_ip(request)`
- Extracts client IP from request
- Handles X-Forwarded-For header (proxy support)
- Falls back to REMOTE_ADDR
- Returns: IP address string

#### `check_rate_limit(ip_address)`
- Checks if IP has exceeded rate limit
- Returns: `(is_allowed: bool, remaining_messages: int, current_count: int)`
- Window: 1 hour (3600 seconds)
- Limit: 5 messages per window

#### `increment_rate_limit(ip_address)`
- Increments message counter in cache
- Sets TTL to 1 hour
- Called after successful email send

#### `send_contact_email(name, email, subject, message, request)`
- Creates and sends EmailMessage
- To: kuhin@ku.edu.np (from settings.CONTACT_EMAIL_RECIPIENT)
- From: noreply@kuhin.ku.edu.np (from settings.DEFAULT_FROM_EMAIL)
- Reply-To: user's email address
- Includes formatted body with IP and timestamp
- Error handling with logging
- Returns: `{'success': bool, 'message': str, 'error': str}`

#### `send_confirmation_email(email, name, subject=None)`
- Sends auto-reply to user
- Professional template confirming message receipt
- Error handling with logging
- Returns: `{'success': bool}`

**Rate Limiting Constants**:
- `RATE_LIMIT_KEY_TEMPLATE`: 'contact_form_limit_{ip}'
- `RATE_LIMIT_MAX_MESSAGES`: 5
- `RATE_LIMIT_WINDOW_SECONDS`: 3600 (1 hour)

---

### 3. Updated `home/views.py`
**Changes**: Updated `contact()` function (lines 105-172)

**Flow**:
1. **GET request**: Display empty ContactForm
2. **POST request**:
   - Validate form data using ContactForm
   - If validation fails: Display field-specific errors, re-render form
   - Extract client IP using `get_client_ip()`
   - Check rate limit using `check_rate_limit()`
   - If rate limit exceeded: Show error message, redirect (no email sent)
   - If allowed:
     - Extract cleaned form data
     - Call `send_contact_email()` with user data
     - If successful:
       - Call `increment_rate_limit()` to track this message
       - Call `send_confirmation_email()` for user confirmation
       - Show success message via Django messages framework
       - Redirect to contact page (clears form)
     - If email fails: Show error message

**Imports Added**:
```python
from .forms import ContactForm
from .email_utils import (
    get_client_ip,
    check_rate_limit,
    increment_rate_limit,
    send_contact_email,
    send_confirmation_email
)
```

---

### 4. Updated `templates/contact.html`
**Changes**: Integrated Django form rendering (lines 75-130)

**Changes Made**:
- Replaced static HTML inputs with `{{ form.name }}`, `{{ form.email }}`, `{{ form.subject }}`, `{{ form.message }}`
- Added error display blocks for each field:
  ```html
  {% if form.field.errors %}
      <div class="invalid-feedback d-block">
          {% for error in form.field.errors %}
              {{ error }}
          {% endfor %}
      </div>
  {% endif %}
  ```
- Preserved Bootstrap classes and icon styling
- CSRF token maintained via `{% csrf_token %}`
- Form action points to 'contact' URL
- Method: POST

**Form Structure**:
- Name field with user icon
- Email field with envelope icon
- Subject field with heading icon
- Message field with message icon
- Submit button with paper plane icon

---

### 5. Updated `kuhin_project/settings.py`
**Changes**: Added email, cache, and logging configuration (60+ lines)

**Email Configuration** (lines 163-178):
```python
# Conditional email backend based on DEBUG mode
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@kuhin.ku.edu.np')
CONTACT_EMAIL_RECIPIENT = config('CONTACT_EMAIL_RECIPIENT', default='kuhin@ku.edu.np')
```

**Cache Configuration** (lines 181-189):
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'kuhin-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
```

**Logging Configuration** (lines 192-225):
- Handlers: File (`logs/kuhin.log`) and Console
- Level: INFO
- Loggers: django and home.email_utils
- File format: timestamp, level, logger, message

---

## 📁 Files Created for Documentation/Testing

### 1. `.env.example`
Template file for environment variables. Users should:
```bash
cp .env.example .env
```

Then fill in actual SMTP credentials:
- EMAIL_HOST (e.g., smtp.gmail.com)
- EMAIL_PORT (e.g., 587)
- EMAIL_USE_TLS (True/False)
- EMAIL_HOST_USER (sender email)
- EMAIL_HOST_PASSWORD (password or app-specific password)
- CONTACT_EMAIL_RECIPIENT (target: kuhin@ku.edu.np)

### 2. `CONTACT_FEATURE_GUIDE.md`
Comprehensive documentation (1000+ lines) including:
- Architecture overview
- Component descriptions
- Setup instructions
- Validation rules table
- Rate limiting explanation
- Security features
- Email templates
- Logging information
- Troubleshooting guide
- Production deployment checklist
- Performance considerations
- Future enhancement suggestions

### 3. `verify_email_config.py`
Verification script to test:
- Email configuration
- Cache/rate limiting setup
- Form validation
- Email utilities
- Logging configuration
- Email sending capability

**Usage**:
```bash
python manage.py shell < verify_email_config.py
```

### 4. `logs/` directory
Created with `logs/kuhin.log` for email system logging

---

## 🔐 Security Features

### 1. **CSRF Protection**
- Django CSRF token in form
- Token verification on POST
- Auto-regenerated after submission

### 2. **Input Validation**
- Form field validation via Django forms
- Custom clean_* methods for business logic
- Regex patterns for safe characters
- Length limits on all fields

### 3. **Spam Detection**
- Regex matching for spam keywords:
  - viagra, cialis, phentermine
  - casino, poker, lottery
  - click here, buy now
  - free money, work from home
- Case-insensitive pattern matching
- Error message: "Your message contains spam keywords"

### 4. **Email Validation**
- RFC 5322 format checking
- Lowercase normalization
- Max 254 character length

### 5. **Rate Limiting**
- IP-based tracking (no username required)
- 5 messages per hour per IP
- Cache-based (in-memory, no DB overhead)
- Automatic window reset after 1 hour

### 6. **Credentials Security**
- No hardcoded email credentials
- All credentials from environment variables (.env)
- SMTP credentials not in version control
- Different endpoints for dev vs production

### 7. **Error Handling**
- Try/except blocks in email functions
- Logging of errors to file + console
- User-friendly error messages
- No sensitive info in error messages

---

## 📊 Rate Limiting Details

**Behavior**:
- **Limit**: 5 messages per IP per hour
- **Window**: 3600 seconds (1 hour)
- **Storage**: Django cache (LocMemCache by default)
- **Tracking**: IP-based (no database table needed)
- **Reset**: Automatic after 1 hour window expires

**Example Timeline**:
```
10:00 AM - Message 1: ✓ Allowed (1/5)
10:15 AM - Message 2: ✓ Allowed (2/5)
10:30 AM - Message 3: ✓ Allowed (3/5)
10:45 AM - Message 4: ✓ Allowed (4/5)
11:00 AM - Message 5: ✓ Allowed (5/5)
11:05 AM - Message 6: ✗ Blocked (window still open)
12:00 PM - Message 6: ✓ Allowed (new 1-hour window started)
```

---

## 📧 Email Templates

### Contact Email (sent to kuhin@ku.edu.np)

```
Subject: New Contact Form Submission: [User Subject]
From: noreply@kuhin.ku.edu.np
Reply-To: [User Email]

---

Name: [User Name]
Email: [User Email]
Subject: [User Subject]
IP Address: [Client IP]
Submitted: [ISO Timestamp]

---

Message:

[User Message]

---

** This is an automated message. To reply, use the Reply-To address. **
```

### Confirmation Email (sent to user)

```
Subject: We Received Your Message - KUHIN Club
From: noreply@kuhin.ku.edu.np

Dear [User Name],

Thank you for contacting KUHIN Club! We have received your message and 
will respond as soon as possible.

Your Message:
Subject: [User Subject]
Received: [Timestamp]

We appreciate your interest and will be in touch shortly.

Best regards,
KUHIN - Kathmandu University Hiking Club
```

---

## 🧪 Testing Instructions

### 1. Development Mode (Console Backend)

```bash
# In .env, set DEBUG=True
DEBUG=True

# Start server
python manage.py runserver

# Visit contact form
# http://localhost:8000/contact/

# Submit form

# Check console output for email
```

### 2. Production Mode (SMTP Backend)

```bash
# In .env, set DEBUG=False and add SMTP credentials
DEBUG=False
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Start server
python manage.py runserver

# Visit contact form
# http://localhost:8000/contact/

# Submit form

# Check logs/kuhin.log for email sending results
```

### 3. Test Rate Limiting

```bash
# Submit 5 messages from same IP (within 1 hour)
# Each should succeed with "Message sent" confirmation

# Submit 6th message
# Should fail with "You have reached the message limit" error

# Wait 1 hour or manually clear cache
# python manage.py shell
# >>> from django.core.cache import cache
# >>> cache.clear()
# Then try again - should work
```

### 4. Test Form Validation

**Empty field**: Leave name blank → Error: "This field is required"
**Invalid email**: Enter "invalid-email" → Error: "Enter a valid email address"
**Short name**: Enter "A" → Error: "Ensure this value has at least 2 characters"
**Spam message**: Include "viagra" → Error: "Your message contains spam keywords"
**Short message**: Enter "hi" → Error: "Ensure this value has at least 10 characters"

---

## 📝 Configuration Checklist

### Development Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Set `DEBUG=True` in `.env`
- [ ] Create `logs/` directory: `mkdir -p logs`
- [ ] Create `logs/kuhin.log` file: `touch logs/kuhin.log`
- [ ] Run verification: `python verify_email_config.py`
- [ ] Test contact form with console backend
- [ ] Verify no validation errors
- [ ] Test rate limiting (6+ messages)

### Production Setup
- [ ] Copy `.env.example` to `.env`
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure SMTP credentials:
  - EMAIL_HOST (e.g., smtp.gmail.com)
  - EMAIL_PORT (e.g., 587)
  - EMAIL_USE_TLS (True)
  - EMAIL_HOST_USER (sender email)
  - EMAIL_HOST_PASSWORD (app password)
- [ ] Create `logs/` directory with write permissions
- [ ] Test email sending with test form
- [ ] Verify logs/kuhin.log shows successful sends
- [ ] Set ALLOWED_HOSTS in settings
- [ ] Disable DEBUG mode
- [ ] Test with real email recipients

---

## 🐛 Troubleshooting Quick Links

**Form not displaying?**
- Check ContactForm import in views.py
- Verify contact.html template syntax

**Email not sending?**
- Check .env SMTP credentials
- Verify DEBUG setting (False for SMTP)
- Check logs/kuhin.log for errors
- Try with DEBUG=True first (console backend)

**Rate limiting not working?**
- Verify CACHES configuration in settings.py
- Check cache backend is LocMemCache
- Clear cache: `python manage.py shell` → `cache.clear()`

**Form validation too strict?**
- Modify `clean_*` methods in home/forms.py
- Adjust length limits (max_length parameters)
- Update spam keyword list (SPAM_KEYWORDS in email_utils.py)

---

## 📚 Documentation Files

1. **CONTACT_FEATURE_GUIDE.md** - Comprehensive 1000+ line guide with:
   - Architecture details
   - Setup instructions
   - Validation rules
   - Security features
   - Production deployment
   - Troubleshooting

2. **`.env.example`** - Environment variable template

3. **`verify_email_config.py`** - Configuration verification script

4. **This file** - Implementation summary (you are here)

---

## ✅ Implementation Status

All components are **COMPLETE and PRODUCTION-READY**:

- ✅ ContactForm with comprehensive validation
- ✅ Email utilities with rate limiting
- ✅ Contact view with email sending
- ✅ Contact template with form integration
- ✅ Settings configuration for email/cache/logging
- ✅ Environment variable support
- ✅ Error handling and logging
- ✅ Documentation and guides
- ✅ Verification script
- ✅ Production deployment checklist

**Ready for deployment**: Yes
**Requires additional setup**: SMTP credentials in .env
**Database migrations needed**: No
**New models created**: No (ContactMessage not used)
**External dependencies added**: python-decouple (for .env support)

---

## 🚀 Next Steps

1. **Set up .env file**:
   ```bash
   cp .env.example .env
   # Edit .env with actual credentials
   ```

2. **Create logs directory**:
   ```bash
   mkdir -p logs && touch logs/kuhin.log
   ```

3. **Verify configuration**:
   ```bash
   python manage.py shell < verify_email_config.py
   ```

4. **Test with development server**:
   ```bash
   python manage.py runserver
   # Visit http://localhost:8000/contact/
   ```

5. **Deploy to production**:
   - Set DEBUG=False in .env
   - Configure production SMTP credentials
   - Set ALLOWED_HOSTS
   - Test email sending

---

**Created**: 2024
**Status**: Production Ready ✅
**Maintenance**: Minimal - verify email credentials periodically

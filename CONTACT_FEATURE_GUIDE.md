# Django Contact Us Email Feature - Documentation

## Overview
The Contact Us feature allows website visitors to send messages directly to kuhin@ku.edu.np with built-in:
- Email validation and spam detection
- Rate limiting (5 messages per IP per hour)
- Automatic confirmation emails to users
- Comprehensive error handling and logging
- Support for both development and production environments

---

## Architecture

### Core Components

#### 1. **Contact Form** (`home/forms.py`)
Validates user input with multiple layers of security:

**Form Fields:**
- `name`: 2-100 characters, letters/spaces/hyphens/apostrophes only
- `email`: Valid email format (RFC 5322), max 254 characters
- `subject`: 3-200 characters
- `message`: 10-5000 characters, spam detection enabled

**Validation Methods:**
- `clean_name()`: Allows only letters, spaces, hyphens, and apostrophes
- `clean_email()`: Validates RFC 5322 format and converts to lowercase
- `clean_subject()`: Enforces length limits
- `clean_message()`: Detects spam patterns (viagra, casino, lottery, click here, etc.)

---

#### 2. **Email Utilities** (`home/email_utils.py`)
Handles all email-related operations:

**Key Functions:**

```python
get_client_ip(request)
```
- Extracts client IP address from request
- Handles X-Forwarded-For header (proxy support)
- Falls back to REMOTE_ADDR

```python
check_rate_limit(ip_address)
```
- Returns: `(is_allowed, remaining_messages, current_count)`
- Window: 1 hour per IP address
- Limit: 5 messages per window
- Uses Django cache (no database overhead)

```python
increment_rate_limit(ip_address)
```
- Increments message counter in cache
- Sets TTL to 1 hour

```python
send_contact_email(name, email, subject, message, request)
```
- Creates EmailMessage with:
  - To: kuhin@ku.edu.np (CONTACT_EMAIL_RECIPIENT)
  - From: noreply@kuhin.ku.edu.np (DEFAULT_FROM_EMAIL)
  - Reply-To: user's email address
  - Formatted body with metadata (IP, timestamp)
- Error handling with logging
- Supports console and SMTP backends

```python
send_confirmation_email(email, name, subject)
```
- Auto-reply to user confirming message receipt
- Professional template
- Error handling with logging

---

#### 3. **Contact View** (`home/views.py`)
Main handler for contact form:

**Request Flow:**
1. **GET**: Display empty ContactForm
2. **POST - Validation**:
   - Form validation (fields + custom validators)
   - If errors: Display field-specific messages, re-render form
3. **POST - Rate Limit Check**:
   - Extract client IP
   - Check if IP has exceeded 5 messages/hour
   - If exceeded: Show error message, redirect (no email sent)
4. **POST - Email Sending**:
   - Extract form data
   - Send main email to kuhin@ku.edu.np
   - Increment rate limit counter
   - Send confirmation email to user
   - Show success message
   - Redirect to contact page

**Error Handling:**
- Form validation errors: Display field-specific messages
- Rate limit exceeded: User-friendly message
- Email sending failure: Graceful error message + logging

---

#### 4. **Email Configuration** (`kuhin_project/settings.py`)

**Email Backend Selection:**
```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

**SMTP Configuration** (Production):
- `EMAIL_HOST`: Read from environment
- `EMAIL_PORT`: Read from environment (default: 587)
- `EMAIL_USE_TLS`: Read from environment (default: True)
- `EMAIL_HOST_USER`: Read from environment
- `EMAIL_HOST_PASSWORD`: Read from environment

**Cache Configuration** (Rate Limiting):
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

**Logging Configuration:**
- Handler: File (`logs/kuhin.log`) + Console
- Level: INFO
- Loggers: django, home.email_utils

---

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

**For Gmail SMTP:**
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

**Note for Gmail Users:**
- Enable 2-Step Verification
- Generate App Password: https://myaccount.google.com/apppasswords
- Use the 16-character App Password as EMAIL_HOST_PASSWORD

**For Office 365:**
```
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-password
```

### 2. Create Logs Directory

```bash
mkdir -p logs
touch logs/kuhin.log
```

### 3. Install Requirements

Ensure python-decouple is installed:
```bash
pip install python-decouple
```

Check your `requirements.txt` includes:
```
Django==4.2.27
python-decouple==3.8
```

### 4. Test Configuration

**Development Mode (Console Backend):**
```bash
python manage.py runserver
```

Visit http://localhost:8000/contact/ and submit a test form.

**Check Django Console:**
- You should see the email content printed to terminal
- Verify no validation errors appear
- Confirm rate limit works (submit 6+ messages from same IP)

**Production Mode (SMTP Backend):**
Set `DEBUG=False` in `.env`:
```
DEBUG=False
```

Run server and test form submission. Emails should be sent to actual recipients.

---

## Form Validation Rules

| Field | Rules | Error Message |
|-------|-------|---------------|
| **Name** | 2-100 chars, letters/spaces/hyphens/apostrophes | "Please enter a valid name (2-100 characters, letters only)" |
| **Email** | Valid format (RFC 5322), max 254 chars | "Please enter a valid email address" |
| **Subject** | 3-200 characters | "Subject must be between 3 and 200 characters" |
| **Message** | 10-5000 chars, no spam patterns | "Message must be between 10 and 5000 characters / Contains spam keywords" |

---

## Rate Limiting

**Behavior:**
- Limit: **5 messages per IP per hour**
- Window: 1 hour (3600 seconds)
- Storage: Django cache (in-memory, no database)
- Reset: Automatic after 1 hour

**Example:**
```
Message 1: ✓ Allowed (1/5)
Message 2: ✓ Allowed (2/5)
Message 3: ✓ Allowed (3/5)
Message 4: ✓ Allowed (4/5)
Message 5: ✓ Allowed (5/5)
Message 6: ✗ Blocked (0/5 in new window after 1 hour)
```

**Error Message:**
"You have reached the message limit for this hour (5 per hour per IP). Please try again later."

---

## Security Features

### 1. CSRF Protection
- All forms protected by Django CSRF token
- Token verified on POST submission
- Token auto-regenerated after successful submission

### 2. Email Validation
- RFC 5322 compliant format checking
- Lowercase normalization
- Length limit (254 chars)

### 3. Spam Detection
- Regex patterns for common spam phrases:
  - viagra, cialis, phentermine
  - casino, poker, lottery
  - click here, buy now
  - free money, work from home
- Case-insensitive matching
- Error message: "Your message contains spam keywords"

### 4. Input Validation
- Name: Only safe characters allowed
- Subject: Length validation
- Message: Length + content validation
- All inputs HTML-escaped in templates

### 5. Rate Limiting
- IP-based tracking
- Prevents brute-force attacks
- DoS mitigation

### 6. Environment Variables
- No hardcoded credentials
- SMTP credentials from .env
- Recipient email configurable
- From email configurable

---

## Email Templates

### Contact Email (to kuhin@ku.edu.np)

```
Subject: New Contact Form Submission: [User Subject]

From: [User Name] <[User Email]>
Reply-To: [User Email]

---

Name: [User Name]
Email: [User Email]
Subject: [User Subject]
IP Address: [Client IP]
Submitted: [Timestamp]

---

Message:

[User Message]

---

** This is an automated message. To reply, use the Reply-To address. **
```

### Confirmation Email (to user)

```
Subject: We Received Your Message - KUHIN Club

Dear [User Name],

Thank you for contacting KUHIN Club! We have received your message and will 
respond as soon as possible.

Your Message:
Subject: [User Subject]
Received: [Timestamp]

We appreciate your interest and will be in touch shortly.

Best regards,
KUHIN - Kathmandu University Hiking Club
```

---

## Logging

Log file location: `logs/kuhin.log`

**Logged Events:**
```
[2024-01-15 10:30:45] INFO: Contact email sent successfully (from: user@example.com)
[2024-01-15 10:31:20] ERROR: Failed to send contact email: SMTP error (from: user@example.com)
[2024-01-15 10:32:00] INFO: Confirmation email sent to user@example.com
[2024-01-15 10:32:15] WARNING: Rate limit exceeded for IP 192.168.1.1
```

**Log Levels:**
- **INFO**: Successful email sends, normal operations
- **WARNING**: Rate limit exceeded, validation issues
- **ERROR**: Email sending failures, SMTP errors

---

## Troubleshooting

### Issue: Form not displaying
**Solution:** Check that ContactForm is imported in views.py
```python
from .forms import ContactForm
```

### Issue: "Email not sent" message
**Solution:** 
1. Check SMTP credentials in .env
2. Verify logs/kuhin.log for error details
3. Enable DEBUG=True to see full error in console
4. Check Gmail App Password is used (not regular password)

### Issue: Rate limiting not working
**Solution:**
1. Verify cache is configured in settings.py
2. Check that django.core.cache middleware is included
3. Clear cache: `python manage.py shell` → `cache.clear()`

### Issue: Confirmation emails not sent
**Solution:**
1. Check user email is valid (form validation)
2. Same SMTP troubleshooting as above
3. Check logs for error messages

### Issue: Form validation too strict
**Solution:** Modify validation rules in `home/forms.py`:
- Change length limits in `clean_*` methods
- Modify spam keywords in `clean_message()`
- Update regex patterns

---

## Production Deployment

### Pre-Deployment Checklist
- [ ] Set `DEBUG=False` in .env
- [ ] Set `ALLOWED_HOSTS` in .env
- [ ] Configure production SMTP credentials
- [ ] Create `logs/` directory with write permissions
- [ ] Test form with DEBUG=False
- [ ] Verify email sending works
- [ ] Check logs are being written
- [ ] Review security settings

### Nginx Configuration (Optional)
Contact form endpoint: `/contact/`
Allow all methods: GET (display), POST (submit)

### Database Migrations
Contact messages are **not stored in database**. No migrations needed beyond existing ones.

---

## Performance Considerations

### Rate Limiting Impact
- Minimal: Uses in-memory cache only
- No database queries for rate limiting
- Cache eviction: Automatic after 1 hour

### Email Sending
- Async: Can be improved with Celery (optional future enhancement)
- Blocking: Currently synchronous (acceptable for small volume)
- Timeout: SMTP timeout set by server (typically 30 seconds)

### Scalability
- Current: Single server with LocMemCache
- Future: Switch to Redis cache for distributed systems
  ```python
  CACHES = {
      'default': {
          'BACKEND': 'django_redis.cache.RedisCache',
          'LOCATION': 'redis://127.0.0.1:6379/1',
      }
  }
  ```

---

## Future Enhancements

1. **Async Email Sending**
   - Integrate Celery + Redis
   - Queue email tasks
   - Non-blocking form submission

2. **Email Categories**
   - Allow users to select reason (Membership, Events, Bug Report, etc.)
   - Route to different recipients

3. **File Attachments**
   - Allow file uploads (PDFs, images)
   - Virus scanning
   - Size limits

4. **Captcha Integration**
   - reCAPTCHA v3 for bot protection
   - Complements rate limiting

5. **Analytics**
   - Track submission volume
   - Monitor spam patterns
   - Rate limit statistics

6. **Email Templates with HTML**
   - Rich HTML emails
   - Branded templates
   - Django template rendering

---

## File References

- **Form**: [home/forms.py](home/forms.py)
- **Email Utilities**: [home/email_utils.py](home/email_utils.py)
- **Views**: [home/views.py](home/views.py#L105-L165)
- **Template**: [templates/contact.html](templates/contact.html)
- **Settings**: [kuhin_project/settings.py](kuhin_project/settings.py)
- **URLs**: [home/urls.py](home/urls.py)
- **Environment Template**: [.env.example](.env.example)

---

## Support & Questions

For issues with the contact feature:
1. Check this documentation
2. Review logs/kuhin.log for errors
3. Test with DEBUG=True to see detailed errors
4. Verify .env configuration
5. Check email provider's security settings (Gmail, Office 365, etc.)

---

**Last Updated:** 2024-01-15
**Status:** Production Ready

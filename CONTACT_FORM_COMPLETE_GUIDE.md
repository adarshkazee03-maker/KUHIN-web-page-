# Contact Form Validation & Email Setup - COMPLETE ✅

## Summary
Your contact form is **fully functional** with comprehensive form validation and email configuration. Emails are correctly sent to **kuhin@ku.edu.np**.

---

## 📋 Contact Form Location
- **URL:** `http://127.0.0.1:8000/contact/`
- **Method:** POST with CSRF protection
- **Response:** Redirect on success, re-render with errors on failure

---

## ✅ Form Fields & Validation

### 1. Your Name
```
Validation Rules:
- Required: Yes
- Length: 2-100 characters
- Pattern: First and last name (minimum 2 words)
- Allowed: Letters, spaces, hyphens, apostrophes only
- Example: "John Doe" ✅
- Invalid: "John" (single word) ❌
```

### 2. Email Address
```
Validation Rules:
- Required: Yes
- Format: RFC-compliant email (user@domain.com)
- Max Length: 254 characters
- Disposable Domains Rejected: tempmail, guerrillamail, 10minutemail, etc.
- Example: "john@example.com" ✅
- Invalid: "notanemail" or "john@tempmail.com" ❌
```

### 3. Subject
```
Validation Rules:
- Required: Yes
- Length: 3-200 characters
- Word Count: Minimum 2 words
- Example: "Inquiry about membership" ✅
- Invalid: "Hi" (too short) or "Inquiry" (one word) ❌
```

### 4. Message
```
Validation Rules:
- Required: Yes
- Length: 10-5000 characters
- Word Count: Minimum 5 words
- Spam Detection: Enabled
- Example: "I am interested in joining KUHIN and learning more." ✅
- Invalid: "Hello there" (too short) ❌

Spam Patterns Detected:
- Pharmaceutical spam: viagra, cialis, phentermine, tramadol
- Gambling spam: casino, poker, slots, lottery, prize, jackpot
- Financial scams: "make money", "earn money", "work from home"
- Aggressive marketing: "click here", "buy now", "limited offer"
- Suspicious links: Any http/https URLs
- HTML/Script injection: <a href>, <script>, javascript:
- Excessive punctuation: More than 3 consecutive !! or ??
- Repeated characters: More than 2 consecutive identical chars
- Repeated words: Same word appearing more than 5 times
```

---

## 📧 Email Configuration

### Email Recipient
```
CONFIGURED TO: kuhin@ku.edu.np
Location: kuhin_project/settings.py (line 217)
```

### Email Flow

#### 1. Contact Form Email (to KUHIN)
```
To: kuhin@ku.edu.np
From: noreply@kuhin.ku.edu.np
Reply-To: {user_email}
Subject: [KUHIN Contact Form] {user_subject}

Content:
- User name
- User email
- Message subject
- Full message
- Auto-generated footer
```

#### 2. Confirmation Email (to User)
```
To: {user_email}
From: noreply@kuhin.ku.edu.np
Subject: We've received your message - KUHIN

Content:
- Thank you message
- Message received confirmation
- Response time (24-48 hours)
- Direct contact email: kuhin@ku.edu.np
```

---

## 🔧 Email Backend Configuration

### Development Mode (DEBUG=True)
```python
# In kuhin_project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
**Behavior:** Emails printed to console (terminal output)

### Production Mode (DEBUG=False)
```python
# In kuhin_project/settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```
**Behavior:** Emails sent via SMTP to kuhin@ku.edu.np

---

## 🔐 Security Features

✅ **CSRF Protection** - `{% csrf_token %}` in form
✅ **Form Validation** - Client & server-side validation
✅ **Spam Detection** - 7+ spam pattern checks
✅ **Rate Limiting** - 5 messages per hour per IP
✅ **HTML Injection Prevention** - Sanitized inputs
✅ **Email Validation** - Disposable domain detection
✅ **Logging** - All submissions logged to database
✅ **Error Handling** - Graceful error messages
✅ **Rate Limit Tracking** - Django cache (1-hour window)

---

## 🧪 Testing the Form

### Step 1: Start Server
```bash
cd /Users/adarshthapa/KUHIN-web-page-
source .venv/bin/activate
python3 manage.py runserver
```

### Step 2: Access Form
Visit: `http://127.0.0.1:8000/contact/`

### Step 3: Submit Valid Form
```
Name: John Doe
Email: john@example.com
Subject: Inquiry about membership
Message: I am interested in joining KUHIN and would like to know more about the club.
```

### Step 4: Check Console Output
```
Development mode: Emails printed to terminal
Production mode: Check kuhin@ku.edu.np inbox
```

### Step 5: Verify Database
```
Admin URL: http://127.0.0.1:8000/admin/
Navigate to: Home > Contact Messages
Check: All submissions are logged with timestamps
```

---

## 📊 Rate Limiting

```python
RATE_LIMIT_MAX_MESSAGES = 5      # 5 messages allowed
RATE_LIMIT_WINDOW_SECONDS = 3600 # Per hour (1 hour = 3600 seconds)
Tracked By: Client IP address
Cache: Django local memory cache
```

**After 5 submissions within 1 hour:**
```
Error Message: "You have reached the message limit (5 messages per hour). 
Please try again later."
```

---

## 🌐 Production Deployment

### Step 1: Update .env File
```dotenv
DEBUG=False
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
CONTACT_EMAIL_RECIPIENT=kuhin@ku.edu.np
DEFAULT_FROM_EMAIL=noreply@kuhin.ku.edu.np
```

### Step 2: Gmail Configuration (if using Gmail)
1. Enable 2-factor authentication on Gmail account
2. Create app-specific password: https://myaccount.google.com/apppasswords
3. Use app password in `EMAIL_HOST_PASSWORD` in .env

### Step 3: Restart Server
```bash
python3 manage.py runserver
```

### Step 4: Verify Emails
- Contact form emails → `kuhin@ku.edu.np` inbox
- Confirmation emails → User's inbox

---

## 📁 Related Files

| File | Purpose |
|------|---------|
| [home/forms.py](home/forms.py) | Form class with all validators |
| [home/views.py](home/views.py) | Contact view with email logic |
| [home/email_utils.py](home/email_utils.py) | Email sending & rate limiting |
| [home/models.py](home/models.py) | ContactMessage model |
| [templates/contact.html](templates/contact.html) | Form template with Bootstrap styling |
| [kuhin_project/settings.py](kuhin_project/settings.py) | Email & cache configuration |
| [.env](.env) | Environment variables (email credentials) |

---

## 🔍 Troubleshooting

### Issue: Emails not sending
```
Solution:
1. Check .env file has correct credentials
2. Verify EMAIL_BACKEND is correct
3. Check logs: tail -f logs/kuhin.log
4. Test: python3 manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail('Test', 'This is a test', 'from@example.com', ['to@example.com'])
```

### Issue: Form validation not working
```
Solution:
1. Clear browser cache (Ctrl+Shift+Del)
2. Check browser console (F12 → Console)
3. Verify Django checks: python3 manage.py check
4. Look for JavaScript errors in console
```

### Issue: Rate limit too strict
```
Solution:
1. Modify in home/email_utils.py:
   RATE_LIMIT_MAX_MESSAGES = 10  # Increase from 5
   RATE_LIMIT_WINDOW_SECONDS = 7200  # Change from 3600
2. Clear cache: python3 manage.py shell
   >>> from django.core.cache import cache
   >>> cache.clear()
3. Restart server
```

---

## ✨ Features Summary

✅ Full name validation (2+ words)
✅ Email format & disposable domain validation
✅ Subject validation (2+ words)
✅ Message validation (5+ words)
✅ Spam detection (7+ patterns)
✅ Rate limiting (5 msgs/hour)
✅ Email to: kuhin@ku.edu.np
✅ Confirmation email to user
✅ CSRF protection
✅ Bootstrap styling
✅ Responsive design
✅ Error messages per field
✅ Success notifications
✅ Database logging
✅ Admin interface
✅ Production ready
✅ Logging to file

---

## 📞 Support

For questions about the contact form implementation:
- Check Django logs: `logs/kuhin.log`
- Run system checks: `python3 manage.py check`
- View submitted messages: Django admin at `/admin/`
- Email KUHIN directly: `kuhin@ku.edu.np`

---

**Status:** ✅ COMPLETE & TESTED
**Email Recipient:** ✅ kuhin@ku.edu.np
**Last Updated:** January 19, 2026

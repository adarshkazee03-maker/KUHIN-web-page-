# Contact Form Implementation - Complete Guide

## Overview
The contact form at `http://127.0.0.1:8000/contact/` is fully implemented with comprehensive form validation and email sending functionality.

## Form Fields
The contact form includes the following fields:

1. **Your Name** - Required
   - Min 2 characters, Max 100 characters
   - Must contain first and last name (2+ parts)
   - Only letters, spaces, hyphens, and apostrophes allowed

2. **Email Address** - Required
   - Valid email format (e.g., john@example.com)
   - Max 254 characters
   - Disposable email detection (tempmail, guerrillamail, etc. rejected)
   - No consecutive dots or invalid patterns

3. **Subject** - Required
   - Min 3 characters, Max 200 characters
   - Must be at least 2 words

4. **Message** - Required
   - Min 10 characters, Max 5000 characters
   - Must contain at least 5 words
   - Spam detection enabled

## Form Validations

### Client-Side Validations
- Bootstrap form validation with visual feedback
- Real-time error messages displayed below each field
- Red text for error states

### Server-Side Validations (Python/Django)

#### Name Validation
```python
- Length: 2-100 characters
- Must have at least 2 name parts (first and last name)
- Only alphanumeric, spaces, hyphens, and apostrophes
- Error: "Name can only contain letters, spaces, hyphens, and apostrophes."
```

#### Email Validation
```python
- Valid email format (RFC compliant)
- No disposable email domains (tempmail, guerrillamail, etc.)
- No consecutive dots or invalid patterns
- Error messages for each validation rule
```

#### Subject Validation
```python
- Length: 3-200 characters
- Minimum 2 words
- Error: "Subject should be at least 2 words."
```

#### Message Validation
```python
- Length: 10-5000 characters
- Minimum 5 words
- Spam detection:
  * Pharmaceutical spam (viagra, cialis, etc.)
  * Gambling spam (casino, poker, lottery, etc.)
  * Aggressive marketing phrases
  * Financial scams
  * Suspicious links
  * HTML/script injection attempts
  * Excessive punctuation (max 3 !! or ??)
  * Repeated characters
  * Too many repeated words (max 5 times)
```

## Email Configuration

### Email Recipient
**To:** `kuhin@ku.edu.np` (configured in settings.py)

### Email Templates

#### 1. Contact Form Email (to KUHIN)
- **Subject:** `[KUHIN Contact Form] {user_subject}`
- **Content:**
  - Sender name
  - Sender email
  - Original subject
  - Full message
  - Reply-to: User's email address

#### 2. Confirmation Email (to User)
- **Subject:** `We've received your message - KUHIN`
- **Content:**
  - Thank you message
  - Acknowledgment of message receipt
  - Expected response time (24-48 hours)
  - Direct contact email: kuhin@ku.edu.np

## Email Sending Setup

### Development Mode (DEBUG=True)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails are printed to console (not actually sent)

### Production Mode (DEBUG=False)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Configuration File: `.env`
```dotenv
# Email Settings
DEFAULT_FROM_EMAIL=noreply@kuhin.ku.edu.np
CONTACT_EMAIL_RECIPIENT=kuhin@ku.edu.np

# For production SMTP
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

## Rate Limiting

The contact form has built-in rate limiting to prevent spam:

- **Limit:** 5 messages per hour per IP address
- **Cache:** Django local memory cache
- **Window:** 3600 seconds (1 hour)
- **Error Message:** "You have reached the message limit (5 messages per hour). Please try again later."

## Form Processing Flow

1. User fills out the form
2. Form is submitted via POST
3. Server validates all fields
4. If validation fails:
   - Error messages displayed below each field
   - Form is re-rendered with user data preserved
5. If validation passes:
   - Rate limit checked by IP address
   - If rate limited: error shown, no email sent
   - If allowed:
     - Email sent to `kuhin@ku.edu.np`
     - Confirmation email sent to user
     - Rate limit counter incremented
     - Success message shown
     - Form cleared (redirect)

## Messages Framework

The form uses Django's messages framework for user feedback:

- **Success:** Green alert with check icon
- **Error:** Red alert with exclamation icon
- **Auto-dismiss:** Available with Bootstrap dismiss button

## Testing the Form

### Development Testing
1. Go to `http://127.0.0.1:8000/contact/`
2. Fill in all fields with valid data
3. Submit form
4. Check console for email output (console backend)
5. Verify success message appears

### Gmail SMTP Setup (Production)
1. Enable 2-factor authentication on Gmail account
2. Generate app-specific password
3. Update `.env` file with:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-specific-password
   ```
4. Restart Django server

### Email Verification
- Check that emails arrive at `kuhin@ku.edu.np`
- Verify "Reply-to" header points to user's email
- Check user receives confirmation email
- Verify email formatting and content

## Files Involved

1. **[home/forms.py](home/forms.py)** - Contact form with validators
2. **[home/views.py](home/views.py)** - Contact view with email logic
3. **[home/email_utils.py](home/email_utils.py)** - Email sending and rate limiting
4. **[templates/contact.html](templates/contact.html)** - Form template
5. **[kuhin_project/settings.py](kuhin_project/settings.py)** - Email configuration
6. **.env** - Environment variables (email credentials)

## Troubleshooting

### Emails not sending
- Check `.env` file has correct email credentials
- Verify `EMAIL_BACKEND` is correct for your environment
- Check Django logs in `logs/kuhin.log`
- Ensure "Less secure apps" is enabled for Gmail (if using)

### Form validation not working
- Clear browser cache
- Check browser console for JavaScript errors
- Verify Django system checks: `python manage.py check`

### Rate limiting issues
- Check cache configuration in settings.py
- Clear cache if needed: `python manage.py shell` then `cache.clear()`

## Security Features

✅ CSRF protection via `{% csrf_token %}`
✅ Form validation on client and server
✅ Spam detection with multiple patterns
✅ Rate limiting by IP address
✅ HTML/script injection prevention
✅ Email validation with disposable domain detection
✅ Logging of all email sends for audit trail
✅ Error messages that don't expose system details

## Success Indicators

When the form works correctly, you should see:

1. **Form Renders:** All fields display properly with placeholders
2. **Validation Errors:** Invalid input shows red error messages
3. **Email Sent:** Console backend shows formatted email output
4. **Success Message:** Green alert appears after submission
5. **Confirmation Email:** User receives confirmation message
6. **Message Saved:** Contact message stored in database

# Contact Email Feature - Quick Start Guide

## 🚀 5-Minute Setup

### Step 1: Create Environment File
```bash
cp .env.example .env
```

Edit `.env` and add your email credentials:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEBUG=True
```

**For Gmail Users**:
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password as EMAIL_HOST_PASSWORD

### Step 2: Create Logs Directory
```bash
mkdir -p logs && touch logs/kuhin.log
```

### Step 3: Verify Installation
```bash
python manage.py shell < verify_email_config.py
```

Expected output:
```
✓ EMAIL_BACKEND: django.core.mail.backends.console.EmailBackend
✓ Cache Backend: django.core.cache.backends.locmem.LocMemCache
✓ form fields: ['name', 'email', 'subject', 'message']
✓ All utilities working correctly
```

### Step 4: Test in Development
```bash
python manage.py runserver
```

Open browser:
```
http://localhost:8000/contact/
```

Submit test form and check console output for email content.

---

## 📧 Form Fields

| Field | Rules | Example |
|-------|-------|---------|
| Name | 2-100 chars, letters only | John Doe |
| Email | Valid format, 254 chars max | john@example.com |
| Subject | 3-200 chars | Event Inquiry |
| Message | 10-5000 chars, no spam | I'm interested in joining... |

---

## ⏱️ Rate Limiting

**Limit**: 5 messages per IP per hour

After 5 messages, get error:
```
"You have reached the message limit (5 per hour). Try again later."
```

---

## 🔍 Testing Checklist

- [ ] Form displays with all fields
- [ ] Valid data submits successfully
- [ ] Success message shows
- [ ] Email printed to console (DEBUG=True)
- [ ] Form clears after submit
- [ ] 6th message shows rate limit error
- [ ] Empty field shows validation error
- [ ] Invalid email shows validation error

---

## 📋 Common Tasks

### Change Recipient Email
Edit `.env`:
```
CONTACT_EMAIL_RECIPIENT=newemail@kuhin.ku.edu.np
```

### Change From Email
Edit `.env`:
```
DEFAULT_FROM_EMAIL=contact@kuhin.ku.edu.np
```

### Clear Rate Limit Cache
```bash
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> exit()
```

### View Email Logs
```bash
tail -f logs/kuhin.log
```

### Test with Different Email Provider
Edit `.env` (Office 365 example):
```
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-password
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Form not showing | Check ContactForm import in views.py |
| Email not sending | Set DEBUG=False, check SMTP credentials |
| Rate limit not working | Verify CACHES in settings.py, clear cache |
| Validation too strict | Edit clean_* methods in forms.py |
| No log file | Create: `touch logs/kuhin.log` |

---

## 📚 Full Documentation

For detailed information, see:
- **CONTACT_FEATURE_GUIDE.md** - Complete feature documentation
- **CONTACT_IMPLEMENTATION_SUMMARY.md** - Implementation details
- **verify_email_config.py** - Configuration verification script

---

## ✅ Production Deployment

When deploying to production:

1. Create `.env` with production settings
2. Set `DEBUG=False`
3. Configure real SMTP credentials
4. Create `logs/` directory with write permissions
5. Run verification: `python verify_email_config.py`
6. Test with test form
7. Monitor logs/kuhin.log for issues

---

**Status**: ✅ Ready to Use
**Last Updated**: 2024-01-15

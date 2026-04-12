# Contact Form - Complete Testing & Debugging Guide

## IMPORTANT: Restart Your Server!

Before testing, you MUST restart the Django server for changes to take effect:

```bash
# Stop the running server (Ctrl+C if it's running)

# Start fresh:
python3 manage.py runserver
```

---

## What Was Just Fixed

The form template was updated to properly display validation errors:

### Before (Not working):
- Used `{% render_field %}` tag to render error fields
- Widget_tweaks tag wasn't applying the red border correctly

### After (Fixed):
- Now renders `<input>` and `<textarea>` elements directly
- Applies red border `border-2 border-danger` immediately
- Shows error message below the field
- Preserves user input so they can fix it

---

## Test the Contact Form Now

### Step 1: Start Fresh Server
```bash
# Kill old server (Ctrl+C)
# Start new one:
python3 manage.py runserver
```

### Step 2: Go to Contact Page
```
http://127.0.0.1:8000/contact/
```

### Step 3: Test Invalid Data

**Copy and paste this:**

```
Name: hhhh
Email: hjuii
Subject: jnj
Message: jnj
```

**Then click "Send Message"**

### Step 4: What You Should See

✅ Page should **NOT** redirect
✅ Page should **STAY** on the same form
✅ All 4 fields should have **RED BORDERS** (2px)
✅ Below each field should show error messages:

```
Name field error:
🔴 Please enter your full name (first and last name).

Email field error:
🔴 Please enter a valid email address (e.g., user@example.com).

Subject field error:
🔴 Subject should be at least 2 words.

Message field error:
🔴 Message must be at least 10 characters long.
```

✅ Your entered data should still be in the fields

---

## If You DON'T See Errors

### Check #1: Server Restarted?
```bash
# Is the server showing the new code?
# Look for these messages when you submit:
# - If you see "[KUHIN Contact Form]" emails being logged
#   → Server IS running the new code ✅
# - If you see old behavior
#   → Restart server ❌
```

**Fix:** Kill the server (Ctrl+C) and restart:
```bash
python3 manage.py runserver
```

### Check #2: Browser Cache
```
Clear browser cache:
- Press: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
- Select "All time"
- Clear cache
- Refresh page
```

### Check #3: Hard Refresh
```
Refresh the page:
- Press: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- This forces a fresh load
```

### Check #4: Check Browser Console
```
Press: F12
→ Go to Console tab
→ Look for any JavaScript errors
→ Check if form is being submitted
```

---

## Step-by-Step Validation Testing

### Test 1: Invalid Email Only ❌

```
Name: John Doe
Email: hjuii                     ← INVALID (no @ symbol)
Subject: Inquiry about KUHIN
Message: I am interested in joining KUHIN and learning more
```

**Expected:**
- ✅ RED border on Email field ONLY
- ✅ Error: "Please enter a valid email address..."
- ✅ Other 3 fields normal (no red border)
- ✅ Data preserved in all fields

---

### Test 2: Invalid Subject Only ❌

```
Name: John Doe
Email: john@example.com
Subject: jnj                     ← INVALID (only 1 word)
Message: I am interested in joining KUHIN and learning more
```

**Expected:**
- ✅ RED border on Subject field ONLY
- ✅ Error: "Subject should be at least 2 words."
- ✅ Other 3 fields normal (no red border)
- ✅ Data preserved in all fields

---

### Test 3: Invalid Message Only ❌

```
Name: John Doe
Email: john@example.com
Subject: Inquiry about KUHIN
Message: jnj                     ← INVALID (too short, 1 word)
```

**Expected:**
- ✅ RED border on Message field ONLY
- ✅ Error: "Message must be at least 10 characters long."
- ✅ Other 3 fields normal (no red border)
- ✅ Data preserved in all fields

---

### Test 4: All Valid Data ✅

```
Name: John Doe
Email: john@example.com
Subject: Inquiry about KUHIN
Message: I am interested in joining KUHIN and would like to know more about the club and membership process
```

**Expected:**
- ✅ NO RED BORDERS
- ✅ NO ERROR MESSAGES
- ✅ GREEN success alert: "✅ Your message is sent successfully! We will get back to you soon."
- ✅ Form clears (ready for next message)
- ✅ Email sent to kuhin@ku.edu.np
- ✅ Confirmation email sent to john@example.com

---

### Test 5: Rate Limiting ⏰

```
1. Submit valid form 5 times
2. Try to submit 6th time
```

**Expected on 6th attempt:**
- ✅ RED alert appears: "⏰ Rate limit reached: You have sent 5 messages in the past hour. Please try again after 1 hour."
- ✅ No email sent
- ✅ Form NOT cleared
- ✅ Can try again after 1 hour passes

---

## Email Validation Rules

These will be rejected:

| Input | Reason | Error Message |
|-------|--------|---------------|
| hjuii | No @ symbol | "Please enter a valid email..." |
| test@tempmail.com | Disposable domain | "Please enter a valid email..." |
| test@test | No domain extension | "Please enter a valid email..." |
| test..email@test.com | Consecutive dots | "Please enter a valid email..." |
| notanemail | No @ or domain | "Please enter a valid email..." |

These will be accepted:

| Input | Reason |
|-------|--------|
| john@example.com | Valid format ✅ |
| user.name@company.co.uk | Valid format ✅ |
| test@university.edu | Valid format ✅ |

---

## Field Validation Summary

| Field | Min | Max | Rules |
|-------|-----|-----|-------|
| Name | 2 chars | 100 chars | Must have 2+ words (first + last name) |
| Email | - | 254 chars | Valid format, permanent domain only |
| Subject | 3 chars | 200 chars | Must have 2+ words |
| Message | 10 chars | 5000 chars | Must have 5+ words |

---

## Console Debugging (If Issues Persist)

### In Django Shell:
```bash
python3 manage.py shell
```

```python
from home.forms import ContactForm

# Test with your invalid data
form = ContactForm(data={
    'name': 'hhhh',
    'email': 'hjuii',
    'subject': 'jnj',
    'message': 'jnj'
})

# Check if form is invalid
print("Form is valid:", form.is_valid())

# See all errors
for field, errors in form.errors.items():
    print(f"{field}: {errors}")
```

---

## Files Modified

- [templates/contact.html](templates/contact.html) - Fixed error field rendering
- [home/forms.py](home/forms.py) - Enhanced validators
- [home/views.py](home/views.py) - Clear success messages

---

## Success Checklist

✅ Server restarted with new code
✅ Browser cache cleared
✅ Contact form page loaded fresh
✅ Invalid data shows RED borders
✅ Error messages appear below fields
✅ User data preserved in fields
✅ Valid data shows green success
✅ Rate limiting works (5 msgs/hour)
✅ Emails sent to kuhin@ku.edu.np
✅ Confirmation emails sent to users

---

## Still Not Working?

### Option 1: Check Git Status
```bash
cd /Users/adarshthapa/KUHIN-web-page-
git status
# Make sure changes are saved
```

### Option 2: Check Template Syntax
```bash
python3 manage.py check --deploy
```

### Option 3: View Page Source
In browser:
- Right-click → View Page Source
- Search for `form-control-lg bg-light border-2 border-danger`
- Should appear when field has error
- If NOT there, server didn't restart

### Option 4: Restart Everything
```bash
# Kill server (Ctrl+C)
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Restart server
python3 manage.py runserver
```

---

## Expected vs Actual

### Expected on Invalid Email Input:
```html
<input type="email" name="email" 
       class="form-control form-control-lg bg-light border-2 border-danger" 
       placeholder="e.g. john@example.com" 
       value="hjuii">
<div class="text-danger small mt-2 fw-bold">
    <i class="fas fa-exclamation-circle me-1"></i>
    Please enter a valid email address (e.g., user@example.com).
</div>
```

If you see this in page source → ✅ WORKING
If you don't see `border-danger` → ❌ Server not restarted

---

**TEST NOW AND LET ME KNOW WHAT YOU SEE!**

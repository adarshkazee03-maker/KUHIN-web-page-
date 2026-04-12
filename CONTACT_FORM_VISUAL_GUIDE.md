# 📞 Contact Form - Visual Reference

## The Contact Form (http://127.0.0.1:8000/contact/)

```
┌─────────────────────────────────────────────────────────────┐
│                    Contact KUHIN                            │
│              Get In Touch with our team                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────────────────┐
│  Contact Info        │  │  Send us a Message               │
├──────────────────────┤  ├──────────────────────────────────┤
│ Email:               │  │                                  │
│ kuhin@ku.edu.np      │  │ Your Name *                      │
│                      │  │ ┌──────────────────────────────┐ │
│ Location:            │  │ │ e.g. John Doe                │ │
│ Dhulikhel, Nepal     │  │ └──────────────────────────────┘ │
│                      │  │                                  │
│ [Google Map]         │  │ Email Address *                  │
│                      │  │ ┌──────────────────────────────┐ │
│ [Social Links]       │  │ │ e.g. john@example.com        │ │
│                      │  │ └──────────────────────────────┘ │
└──────────────────────┘  │                                  │
                          │ Subject *                        │
                          │ ┌──────────────────────────────┐ │
                          │ │ How can we help?             │ │
                          │ └──────────────────────────────┘ │
                          │                                  │
                          │ Message *                        │
                          │ ┌──────────────────────────────┐ │
                          │ │ Write your message here...   │ │
                          │ │                              │ │
                          │ │                              │ │
                          │ └──────────────────────────────┘ │
                          │                                  │
                          │ [Send Message Button]            │
                          └──────────────────────────────────┘
```

---

## ✅ Validation Rules Quick Reference

### Name Field
```
Input: "John"
Result: ❌ ERROR
Reason: "Please enter your full name (first and last name)."

Input: "John Doe"
Result: ✅ ACCEPTED
Reason: Valid full name (2 words, 2-100 chars)

Rules:
• Minimum 2 words (first and last name)
• 2-100 characters
• Only letters, spaces, hyphens, apostrophes
```

### Email Field
```
Input: "notanemail"
Result: ❌ ERROR
Reason: "Please enter a valid email address"

Input: "john@tempmail.com"
Result: ❌ ERROR
Reason: "Please use a valid, permanent email address"

Input: "john@example.com"
Result: ✅ ACCEPTED
Reason: Valid email format

Rules:
• Valid email format (user@domain.com)
• No disposable domains (tempmail, guerrillamail, etc.)
• Max 254 characters
```

### Subject Field
```
Input: "Hi"
Result: ❌ ERROR
Reason: "Subject must be at least 3 characters long"

Input: "Inquiry"
Result: ❌ ERROR
Reason: "Subject should be at least 2 words"

Input: "Inquiry about membership"
Result: ✅ ACCEPTED
Reason: Valid subject (2+ words, 3-200 chars)

Rules:
• 3-200 characters
• Minimum 2 words
```

### Message Field
```
Input: "Hello"
Result: ❌ ERROR
Reason: "Message should contain at least 5 words"

Input: "Click here to buy viagra now!!!"
Result: ❌ ERROR
Reason: "Message contains prohibited content (pharmaceutical spam)"

Input: "I am interested in joining KUHIN and learning more about the membership"
Result: ✅ ACCEPTED
Reason: Valid message (5+ words, 10-5000 chars, no spam)

Rules:
• 10-5000 characters
• Minimum 5 words
• Spam detection enabled
• Excessive punctuation detection
• Repeated word detection
```

---

## 📧 Email Sending Flow

```
User Submits Form
     ↓
     ├─ Client-side validation (Bootstrap)
     ↓
Django Server Receives POST
     ↓
     ├─ Name validation
     ├─ Email validation
     ├─ Subject validation
     ├─ Message validation
     ↓ All Valid?
     YES ↓
     ├─ Check rate limit (IP address)
     ↓ Limit OK?
     YES ↓
     ├─ Email #1: To kuhin@ku.edu.np
     │   Subject: [KUHIN Contact Form] {subject}
     │   Reply-To: {user_email}
     │
     ├─ Email #2: To {user_email}
     │   Subject: We've received your message - KUHIN
     │
     ├─ Save to database (ContactMessage)
     ├─ Increment rate limit counter
     ↓
Success Message: "Your message has been sent successfully!"
Form Clear & Redirect
```

---

## 🔒 Security Checks

```
Check 1: CSRF Token
Status: ✅ Active
Location: Form: {% csrf_token %}

Check 2: Name Validation
Status: ✅ Active
Patterns: [a-zA-Z\s\-']+, 2+ words

Check 3: Email Validation
Status: ✅ Active
Patterns: RFC email format, No disposable domains

Check 4: Subject Validation
Status: ✅ Active
Rules: 3-200 chars, 2+ words

Check 5: Message Spam Detection
Status: ✅ Active
Patterns:
  • Viagra, Cialis, etc. (pharmaceutical)
  • Casino, poker, lottery (gambling)
  • Click here, buy now (aggressive marketing)
  • Make money, work from home (financial scams)
  • HTTP links (suspicious)
  • <script>, HTML tags (injection)
  • Repeated characters (!!!!)
  • Excessive punctuation
  • Repeated words

Check 6: Rate Limiting
Status: ✅ Active
Limit: 5 messages per hour per IP address
Cache: Django local memory cache

Check 7: Database Logging
Status: ✅ Active
Saved: All submissions logged with timestamp
```

---

## 📧 Email Content Preview

### Email Sent TO kuhin@ku.edu.np

```
From: noreply@kuhin.ku.edu.np
To: kuhin@ku.edu.np
Reply-To: john@example.com
Date: 2026-01-19 09:30:00
Subject: [KUHIN Contact Form] Inquiry about membership

Hello KUHIN Team,

You have received a new message from the contact form:

============================================================
NAME: John Doe
EMAIL: john@example.com
SUBJECT: Inquiry about membership
============================================================

MESSAGE:
I am interested in joining KUHIN and would like to know 
more about the club and membership benefits.

============================================================

This is an automated email. Please reply to the sender's 
email address above.

Best regards,
KUHIN Website
```

### Email Sent TO john@example.com

```
From: noreply@kuhin.ku.edu.np
To: john@example.com
Date: 2026-01-19 09:30:00
Subject: We've received your message - KUHIN

Hi John,

Thank you for reaching out to KUHIN - Kathmandu University 
Health Informatics Club!

We have received your message and will review it shortly. 
Our team typically responds within 24-48 hours.

If your inquiry is urgent, please feel free to contact us 
directly at:
📧 kuhin@ku.edu.np

Best regards,
KUHIN Team
Kathmandu University
```

---

## ⚙️ Configuration Summary

```
Email Recipient:     ✅ kuhin@ku.edu.np
Sender Email:        ✅ noreply@kuhin.ku.edu.np
Backend (Dev):       ✅ Console output
Backend (Prod):      ✅ SMTP ready
Rate Limit:          ✅ 5 msgs/hour
Database Logging:    ✅ Enabled
CSRF Protection:     ✅ Enabled
Spam Detection:      ✅ Enabled
Error Messages:      ✅ Per-field feedback
Confirmation Email:  ✅ Sent to user
Status:              ✅ LIVE & READY
```

---

## 🎯 Success Indicators

When the form works correctly, you'll see:

✅ Form renders with all 4 fields
✅ Invalid input shows red error messages
✅ Valid input accepted without errors
✅ Email appears in console (development)
✅ Green success alert after submission
✅ Confirmation email received by user
✅ Message appears in Django admin
✅ Spam detected and rejected

---

## 📞 How to Use

1. **Access:** http://127.0.0.1:8000/contact/
2. **Fill in:** Name, Email, Subject, Message
3. **Submit:** Click "Send Message"
4. **Check:** Console output (development) or inbox (production)
5. **Verify:** Django admin → Home → Contact Messages

---

**Setup Status: ✅ COMPLETE & OPERATIONAL**

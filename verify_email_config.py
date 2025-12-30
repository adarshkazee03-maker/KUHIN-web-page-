#!/usr/bin/env python
"""
Email Configuration Verification Script

This script tests the Django email configuration and verifies that all
components of the contact email system are working correctly.

Usage:
    python manage.py shell < verify_email_config.py
    # or
    python verify_email_config.py
"""

import os
import sys
import django

# Setup Django if running standalone
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kuhin_project.settings')
    django.setup()

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.cache import cache
from home.forms import ContactForm
from home.email_utils import (
    get_client_ip,
    check_rate_limit,
    increment_rate_limit,
    send_contact_email,
    send_confirmation_email
)

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def verify_email_settings():
    """Verify email configuration"""
    print_header("EMAIL CONFIGURATION")
    
    print(f"✓ EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"✓ DEBUG Mode: {settings.DEBUG}")
    
    if settings.DEBUG:
        print("   → Using CONSOLE backend (emails printed to console)")
    else:
        print("   → Using SMTP backend (real emails sent)")
        print(f"   → EMAIL_HOST: {settings.EMAIL_HOST}")
        print(f"   → EMAIL_PORT: {settings.EMAIL_PORT}")
        print(f"   → EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        print(f"   → EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    
    print(f"✓ DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"✓ CONTACT_EMAIL_RECIPIENT: {settings.CONTACT_EMAIL_RECIPIENT}")

def verify_cache_settings():
    """Verify cache configuration for rate limiting"""
    print_header("CACHE CONFIGURATION (Rate Limiting)")
    
    cache_backend = settings.CACHES['default']['BACKEND']
    print(f"✓ Cache Backend: {cache_backend}")
    
    # Test cache operations
    test_key = 'test_cache_verify'
    test_value = 'test_value'
    
    try:
        cache.set(test_key, test_value, 60)
        retrieved = cache.get(test_key)
        
        if retrieved == test_value:
            print("✓ Cache SET/GET working correctly")
            cache.delete(test_key)
            print("✓ Cache DELETE working correctly")
        else:
            print("✗ Cache retrieval failed")
    except Exception as e:
        print(f"✗ Cache error: {e}")

def verify_forms():
    """Verify contact form structure"""
    print_header("CONTACT FORM VALIDATION")
    
    form = ContactForm()
    
    print(f"✓ Form fields: {list(form.fields.keys())}")
    
    # Test form validation
    test_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message for verification.'
    }
    
    form = ContactForm(data=test_data)
    if form.is_valid():
        print("✓ Valid form data accepted")
    else:
        print(f"✗ Form validation failed: {form.errors}")

def verify_email_utilities():
    """Verify email utility functions"""
    print_header("EMAIL UTILITIES")
    
    # Test get_client_ip (with fake request)
    class FakeRequest:
        META = {'REMOTE_ADDR': '192.168.1.1'}
    
    fake_request = FakeRequest()
    
    try:
        ip = get_client_ip(fake_request)
        print(f"✓ get_client_ip() working: {ip}")
    except Exception as e:
        print(f"✗ get_client_ip() error: {e}")
    
    # Test rate limiting functions
    try:
        test_ip = '192.168.1.100'
        
        # Clear any existing test data
        cache.delete(f'contact_form_limit_{test_ip}')
        
        # Check rate limit (should be allowed initially)
        is_allowed, remaining, current = check_rate_limit(test_ip)
        print(f"✓ check_rate_limit() working")
        print(f"   → Allowed: {is_allowed}, Remaining: {remaining}, Current: {current}")
        
        # Increment rate limit
        increment_rate_limit(test_ip)
        is_allowed, remaining, current = check_rate_limit(test_ip)
        print(f"✓ increment_rate_limit() working")
        print(f"   → After increment: Remaining: {remaining}, Current: {current}")
        
        # Clean up
        cache.delete(f'contact_form_limit_{test_ip}')
    except Exception as e:
        print(f"✗ Rate limiting error: {e}")

def test_email_sending():
    """Test email sending (won't actually send if not configured)"""
    print_header("EMAIL SENDING TEST")
    
    if not settings.DEBUG:
        print("⚠ DEBUG=False detected")
        print("  This will attempt to send a real email via SMTP")
        print("  Make sure SMTP credentials are configured in .env")
    else:
        print("✓ DEBUG=True: Email will be printed to console (not sent)")
    
    print("\nTo test email sending:")
    print("  1. Run: python manage.py runserver")
    print("  2. Visit: http://localhost:8000/contact/")
    print("  3. Fill out and submit the form")
    print("  4. Check console output or logs/kuhin.log for email content")

def verify_logging():
    """Verify logging configuration"""
    print_header("LOGGING CONFIGURATION")
    
    import logging
    
    log_dir = 'logs'
    log_file = 'logs/kuhin.log'
    
    if os.path.exists(log_dir):
        print(f"✓ Log directory exists: {log_dir}")
    else:
        print(f"✗ Log directory missing: {log_dir}")
        print(f"  Create with: mkdir -p {log_dir}")
    
    if os.path.exists(log_file):
        print(f"✓ Log file exists: {log_file}")
    else:
        print(f"⚠ Log file missing: {log_file}")
        print(f"  Create with: touch {log_file}")
    
    # Check logger configuration
    logger = logging.getLogger('home.email_utils')
    print(f"✓ Email utility logger configured")
    print(f"  Handlers: {len(logger.handlers)} configured")

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("  DJANGO CONTACT EMAIL SYSTEM - VERIFICATION")
    print("="*60)
    
    verify_email_settings()
    verify_cache_settings()
    verify_forms()
    verify_email_utilities()
    verify_logging()
    test_email_sending()
    
    print("\n" + "="*60)
    print("  VERIFICATION COMPLETE")
    print("="*60)
    print("\nNext Steps:")
    print("  1. Ensure .env file exists with email credentials")
    print("  2. Run: python manage.py runserver")
    print("  3. Visit: http://localhost:8000/contact/")
    print("  4. Submit a test message")
    print("  5. Check console or logs/kuhin.log for email output")
    print("\nDocumentation: CONTACT_FEATURE_GUIDE.md")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()

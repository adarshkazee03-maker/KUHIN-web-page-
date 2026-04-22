#!/usr/bin/env python3
import os
import re

# Template updates - file path and specific update details
updates = {
    'templates/events.html': {
        'tag': 'EVENTS & ACTIVITIES',
        'title': 'Events & Activities',
        'description': 'Join us for networking opportunities, technical workshops, seminars, and collaborative events throughout the year.',
        'cta': 'Browse Events'
    },
    'templates/gallery.html': {
        'tag': 'VISUAL ARCHIVES',
        'title': 'Gallery',
        'description': 'Explore the moments and memories captured from our programs, events, and community initiatives at KUHIN.',
        'cta': 'View Gallery'
    },
    'templates/resources.html': {
        'tag': 'LEARNING RESOURCES',
        'title': 'Health Informatics Resources',
        'description': 'Comprehensive collection of tools, guides, research papers, and educational materials for health informatics professionals.',
        'cta': 'Explore Resources'
    },
    'templates/event_detail.html': {
        'tag': 'EVENT DETAILS',
        'title': 'Event Details',
        'description': 'Discover the latest event information including date, time, location, agenda, and registration details.',
        'cta': 'Learn More'
    },
    'templates/blogs/blog_list.html': {
        'tag': 'INSIGHTS & STORIES',
        'title': 'KUHIN Blog',
        'description': 'Read articles, case studies, and insights from our community about health informatics, technology, and innovation.',
        'cta': 'Read Articles'
    },
    'templates/news/news_list.html': {
        'tag': 'ANNOUNCEMENTS',
        'title': 'News & Updates',
        'description': 'Stay updated with the latest news, announcements, and developments from the KUHIN community.',
        'cta': 'View News'
    },
    'templates/home.html': {
        'tag': 'WELCOME TO KUHIN',
        'title': 'Transforming Healthcare Through Data and Technology',
        'description': 'Kathmandu University Health Informatics Network empowers students and professionals to build innovative solutions at the intersection of healthcare, data science, and technology.',
        'cta': 'Join KUHIN'
    }
}

new_hero_template = '''<!-- Hero Section - Professional Design -->
<section style="background-image: linear-gradient(135deg, rgba(26,30,60,0.8) 0%, rgba(26,30,60,0.7) 100%), url('/static/images/backgroundtemp1.png'); background-size: cover; background-position: center; background-attachment: fixed; height: 600px; display: flex; align-items: center; color: white; position: relative; margin-top: 0;">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-8">
                <div style="animation: fadeInUp 0.8s ease-out;">
                    <p style="color: #D4A574; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 1rem;">{TAG}</p>
                    <h1 style="font-size: 3.5rem; font-weight: 900; line-height: 1.2; margin-bottom: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        {TITLE}
                    </h1>
                    <p style="font-size: 1.2rem; line-height: 1.8; margin-bottom: 2rem; max-width: 700px; font-weight: 300; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
                        {DESCRIPTION}
                    </p>
                    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                        <a href="#main-content" style="background: #D4A574; color: #1a1e3c; padding: 1rem 2.5rem; font-weight: 700; border-radius: 8px; text-decoration: none; transition: all 0.3s; box-shadow: 0 10px 30px rgba(212,165,116,0.3);" onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 15px 40px rgba(212,165,116,0.4)'" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(212,165,116,0.3)';">
                            {CTA}
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>'''

for file_path, details in updates.items():
    full_path = os.path.join('/Users/adarshthapa/KUHIN-web-page-', file_path)
    
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            content = f.read()
        
        # Find and replace the hero section
        # Pattern to match the old hero section
        pattern = r'<!-- Hero Section.*?-->\s*<section[^>]*style="[^"]*background-image: url\(\'\/static\/images\/backgroundtemp1\.png\'\)[^"]*"[^>]*>.*?</section>'
        
        # Create new hero content
        new_hero = new_hero_template.format(
            TAG=details['tag'],
            TITLE=details['title'],
            DESCRIPTION=details['description'],
            CTA=details['cta']
        )
        
        # Replace
        new_content = re.sub(pattern, new_hero, content, flags=re.DOTALL)
        
        if new_content != content:
            with open(full_path, 'w') as f:
                f.write(new_content)
            print(f"✓ Updated {file_path}")
        else:
            print(f"⚠ No match found in {file_path}")
    else:
        print(f"✗ File not found: {file_path}")

print("\nDone!")

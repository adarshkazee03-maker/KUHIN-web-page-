# KUHIN Website Design System & Component Standards

## 📐 Overview
This document defines the professional design standards and component specifications for all KUHIN website pages to ensure consistent UI/UX, branding, and visual hierarchy.

---

## 🎨 **Color Palette**

### Primary Colors
- **Primary Blue**: `#2c3e91` (Main brand color - buttons, links, headers)
- **Primary Light Blue**: `#3d5fff` (Hover states, gradients)
- **Dark Background**: `#1a1f35` (Hero sections, dark overlays)
- **Light Background**: `#f8f9fa` (Section backgrounds)
- **Card Background**: `#ffffff` (Card backgrounds)

### Hero Gradient
```
linear-gradient(135deg, #1a1f35 0%, #2c3e91 100%)
```

### CSS Variables (base.html)
```css
:root {
  --primary-color: #2c3e91;
  --primary-light: #3d5fff;
  --secondary-color: #6c757d;
  --dark-bg: #1a1f35;
  --light-bg: #f8f9fa;
  --card-bg: #ffffff;
  --hero-gradient: linear-gradient(135deg, #1a1f35 0%, #2c3e91 100%);
}
```

---

## 🏗️ **Component Classes & Usage**

### 1. Hero Sections
**Class**: `.kuhin-hero`
**Usage**: All landing/main sections
```html
<section class="kuhin-hero">
    <div class="container position-relative z-3 text-center py-5">
        <span class="kuhin-badge mb-3">...</span>
        <h1 class="display-4 fw-bold" style="color: white;">Title</h1>
        <p class="lead" style="color: rgba(255,255,255,0.9);">Subtitle</p>
    </div>
</section>
```

### 2. Content Sections
**Class**: `.kuhin-content`
**Usage**: Main content wrapper areas
- Padding: `3rem 0` (top/bottom), `0` (left/right)
- Background: `#f8f9fa`

### 3. Cards
**Class**: `.kuhin-card`
**Usage**: All card elements (blog, resources, events, etc.)
```html
<div class="kuhin-card h-100 p-4">
    <!-- Content -->
</div>
```

#### Card Features:
- Background: white with rounded corners (12px)
- Shadow: `0 2px 8px rgba(0,0,0,0.08)`
- Hover Effect: Lifts up (+4px), enhanced shadow
- Padding: Use `p-4` for consistent spacing
- Border: None (border: none;)

### 4. Badges
**Class**: `.kuhin-badge`
**Usage**: Labels, category badges, status indicators
- Background: Primary color (#2c3e91)
- Color: White
- Padding: `0.5rem 1rem`
- Border-radius: `20px`
- Font-size: `0.9rem`

### 5. Section Titles
**Class**: `.kuhin-section-title`
**Usage**: Main section headings

#### Features:
- Font-size: `2.5rem`
- Font-weight: `700`
- Color: `#1a1f35` (dark)
- Bottom border: 4px blue line (60px wide)
- Margin-bottom: `2rem`

**Responsive**: At 768px breakpoint → `2rem` font-size

### 6. Buttons
**Class**: `.btn-primary` or `.btn btn-outline-primary`

#### Primary Button:
- Background: `var(--primary-color)`
- Border: None
- Hover: Lighter blue (#3d5fff) with slight lift (-2px)
- Shadow on hover: `0 8px 16px rgba(44,62,145,0.3)`

#### Outline Button:
- Border: 1px solid `var(--primary-color)`
- Color: `var(--primary-color)`
- Background: Transparent
- Border-radius: `50px` (pill shape)

---

## 📑 **Template Structure Standards**

### Base Template Hierarchy
```
base.html (master template)
├── Navigation (fixed top, blue gradient)
├── {% block content %} (main content)
├── Footer (dark background)
└── Scripts
```

### Page Template Pattern
```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title - KUHIN{% endblock %}
{% block meta_description %}Page description...{% endblock %}

{% block content %}

<!-- Hero Section -->
<section class="kuhin-hero">
    <!-- Hero content -->
</section>

<!-- Main Content -->
<section class="kuhin-content">
    <div class="container">
        <h2 class="kuhin-section-title">Section Title</h2>
        <!-- Content with cards/components -->
    </div>
</section>

{% endblock %}
```

---

## 📱 **Responsive Design**

### Breakpoints (Bootstrap)
- **xs**: < 576px
- **sm**: ≥ 576px
- **md**: ≥ 768px  
- **lg**: ≥ 992px
- **xl**: ≥ 1200px

### Grid System
- Use Bootstrap 5 grid: `row g-4` for consistent gaps
- Column spacing: `g-4` (1.5rem gap)
- Mobile-first approach - define mobile layout, then use `col-md-6`, `col-lg-4`, etc.

---

## 🎭 **Typography Standards**

### Font Stacks (from base.html)
- **Headings**: `Plus Jakarta Sans` (weights: 400, 600, 700, 800)
- **Body**: `Inter` (weights: 300, 400, 500, 600)
- **Monospace**: System fonts for code blocks

### Heading Hierarchy
```
h1: display-4 or display-3 (page titles in heroes)
h2: kuhin-section-title class (section headings)
h3: fw-bold mb-3 (subsection headings)
h4, h5, h6: fw-bold (smaller headings)
```

### Text Classes
- **Large text**: `.fs-5` or `lead` class
- **Small text**: `.small` class
- **Muted text**: `.text-muted`
- **Bold**: `.fw-bold`
- **Light**: `.fw-light` (300)
- **SemiBold**: `.fw-semibold` (600)

---

## ✨ **Spacing & Layout**

### Padding Conventions
- **Card padding**: `p-4` (1.5rem)
- **Section padding**: Built into `.kuhin-content`
- **Container spacing**: `py-5` for vertical spacing (3rem)

### Margins
- **Section margin**: `mb-5` (3rem bottom)
- **Element spacing**: `mb-3` or `mb-4` depending on size
- **Heading margins**: Usually `mb-3` to `mb-5`

### Gap Classes
- **Grid gaps**: `g-4` (1.5rem) standard for all grid rows

---

## 🚀 **State/Hover Effects**

###  Hover Lift
**Class**: `.hover-lift`
- Transform: `translateY(-8px)`
- Enhanced shadow on hover
- Smooth transition: `all 0.3s ease`

### Card Hover Behavior
- Cards automatically lift on hover (built into `.kuhin-card`)
- Shadow increases from `0 2px 8px` to `0 8px 24px`
- Smooth transition: `0.3s cubic-bezier(0.4, 0, 0.2, 1)`

---

## 📋 **Checklist for New Pages/Components**

- [ ] Use `.kuhin-hero` for main sections
- [ ] Use `.kuhin-content` for content wrappers
- [ ] Replace inline color styles with CSS variables
- [ ] Use `.kuhin-card` for all card elements
- [ ] Use `.kuhin-section-title` for section headings
- [ ] Use `.kuhin-badge` for category/status labels
- [ ] Ensure buttons use `.btn-primary` or `.btn-outline-primary`
- [ ] Remove fade-in-up and animation-delay inline styles (use CSS)
- [ ] Ensure responsive grid: `col-md-6 col-lg-4` pattern
- [ ] Check footer styling consistency
- [ ] Verify navigation consistency
- [ ] Test on mobile, tablet, and desktop

---

## 📂 **File Structure Reference**

```
templates/
├── base.html (master template with navigation, footer)
├── about.html ✓ (standardized)
├── contact.html ✓ (standardized)
├── events.html ✓ (standardized)
├── gallery.html ✓ (standardized)
├── programs.html ✓ (updated)
├── resources.html ✓ (standardized)
├── team.html (needs review)
├── blogs/
│   ├── blog_list.html ✓ (fixed)
│   └── blog_detail.html
├── components/
│   ├── hero.html
│   ├── card-blog.html
│   ├── card-event.html
│   ├── card-news.html
│   └── ...
├── home/
│   ├── index.html
│   ├── enhanced_index.html
│   └── new_index.html
└── news/
    ├── news_list.html
    └── news_detail.html
```

---

## 🎯 **Design Principles**

1. **Consistency**: All pages follow the same color, typography, and component patterns
2. **Readability**: Clear hierarchy with appropriate font sizes and spacing
3. **Professional**: Clean, modern design appropriate for an academic health informatics club
4. **Responsive**: Mobile-first approach that works on all devices
5. **Accessibility**: Proper semantic HTML, color contrast, ARIA labels
6. **Performance**: Minimal inline styles, rely on CSS classes

---

## 🔧 **Quick Reference: CSS Variable Usage**

```css
/* Colors */
color: var(--primary-color);         /* #2c3e91 - links, text */
color: var(--primary-light);         /* #3d5fff - hover states */
background: var(--hero-gradient);    /* Hero sections */
background: var(--light-bg);        /* Section backgrounds */

/* Spacing (use Bootstrap classes instead) */
padding: var(--spacing-lg);     /* 1.5rem */
margin-bottom: var(--spacing-md); /* 1rem */
```

---

*Last Updated: February 23, 2025*
*Design System Owner: KUHIN Web Development Team*

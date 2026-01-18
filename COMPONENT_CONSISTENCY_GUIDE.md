# KUHIN Component Consistency Guide

## Overview
This document outlines the unified design system and component standards that ensure consistency across all pages on the KUHIN website. All components have been updated to maintain a cohesive visual identity and user experience.

---

## Color Palette (Design System)

### Primary Colors
- **Primary Blue**: `#2c3e91` - Main brand color for CTAs, highlights, and primary actions
- **Secondary Teal**: `#00897b` - Used for accents and secondary elements
- **Accent Purple**: `#7e57c2` - Used for highlights and special sections

### Neutral Colors
- **Dark**: `#1a1a2e` - Text and dark backgrounds
- **Light Gray**: `#b2bec3` - Borders and secondary text
- **Lightest Gray**: `#f5f6fa` - Background and cards
- **White**: `#ffffff` - Primary background

### Semantic Colors
- **Success**: `#27ae60` - Positive states
- **Warning**: `#f39c12` - Caution/pending states
- **Danger**: `#e74c3c` - Error states
- **Info**: `#3498db` - Information states

---

## Component Library

### 1. **Pagination Component** (`pagination.html`)
**Purpose**: Navigating through paginated content (blogs, events, resources)

**Key Features**:
- Glass-panel container with backdrop blur
- Intelligent page number display with ellipsis
- Active page highlighting with primary color
- Hover effects with lift animation
- Responsive design (hides labels on mobile)
- Accessibility: ARIA labels and focus states

**Styling**:
```css
- Min width: 44px for clickable areas
- Border radius: 10px
- Hover: Translate Y -2px + box-shadow
- Active: Primary color with 6px shadow
```

**Usage**:
```django
{% include 'components/pagination.html' with page_obj=page_obj %}
```

---

### 2. **Hero Section** (`hero.html`)
**Purpose**: Page header with title, subtitle, and optional badge

**Key Features**:
- Background image with blur and brightness filter
- Default gradient fallback
- Animated badge with icon
- Staggered fade-in animations for title and subtitle
- Full-width responsive design
- Decorative pattern overlay

**Styling**:
```css
- Min height: 420px
- Border bottom-right radius: 50px
- Gradient fallback: #0f172a → #1e293b
- Animations: 0.8s fadeInUp with 0.1s delays
```

**Usage**:
```django
{% include 'components/hero.html' with 
    title="Page Title" 
    subtitle="Description" 
    badge_text="Badge" 
    badge_icon="fas fa-icon"
%}
```

---

### 3. **Breadcrumb Navigation** (`breadcrumb.html`)
**Purpose**: Help users understand page hierarchy

**Key Features**:
- Home link with icon
- Dynamic breadcrumb items
- Custom separator styling for dark backgrounds
- Hover underline animation
- Focus states for accessibility
- Responsive font sizing

**Styling**:
```css
- Separator: "/" with custom color
- Hover: White text + underline animation
- Active: Bold white text
- Focus: 2px outline with primary color
```

**Usage**:
```django
{% include 'components/breadcrumb.html' with breadcrumb_items=breadcrumbs %}
```

---

### 4. **Blog Card** (`card-blog.html`)
**Purpose**: Displaying individual blog posts in grid layouts

**Key Features**:
- Featured image with hover zoom effect
- Category badge in top-right corner
- Publication date and view count
- Author avatar with initials
- Line-clamped title and excerpt
- "Read more" link with arrow animation
- Glass-panel with backdrop blur

**Styling**:
```css
- Image height: 220px
- Card height: 100% (flex)
- Background: rgba(248, 249, 250, 0.7)
- Hover: Lift -8px + enhanced shadow
- Line clamp: 2 lines for title, 3 for excerpt
```

**Usage**:
```django
{% include 'components/card-blog.html' with blog=blog_post %}
```

---

### 5. **Event Card** (`card-event.html`)
**Purpose**: Showcasing upcoming and past events

**Key Features**:
- Event image with hover scale effect
- Status badge (Upcoming/Ongoing/Past)
- Date overlay with gradient background
- Location with icon
- Event description excerpt
- "Event Details" link with arrow

**Styling**:
```css
- Image height: 180px
- Status badges: Color-coded (Blue/Orange/Gray)
- Date overlay: Gradient from top with shadow text
- Hover: Lift -8px + shadow enhancement
```

**Usage**:
```django
{% include 'components/card-event.html' with event=event_obj %}
```

---

### 6. **News Card** (`card-news.html`)
**Purpose**: Displaying news and announcements

**Key Features**:
- Date badge in top-left (primary color background)
- Read button in top-right corner
- News title with line clamping
- Description excerpt with line clamp
- "Announcement" label with icon
- "Read More" text appears on hover

**Styling**:
```css
- Card background: Glass effect with blur
- Date badge: Primary color with opacity
- Hover: Opacity change on "Read More" text
- Line clamp: 2 lines for title, 3 for excerpt
```

**Usage**:
```django
{% include 'components/card-news.html' with news=news_update %}
```

---

### 7. **Empty State** (`empty-state.html`)
**Purpose**: Showing when no content is available

**Key Features**:
- Animated icon (scale-in animation)
- Title and message
- Optional call-to-action button
- Glass-panel styling
- Gradient background decoration

**Styling**:
```css
- Container width: 300px-500px
- Icon: Scale from 0 with 0.5s duration
- Button: Outline primary with hover lift
- Background: Gradient with opacity
```

**Usage**:
```django
{% include 'components/empty-state.html' 
    icon="fas fa-inbox" 
    title="No items found" 
    message="Try adjusting filters." 
    cta_text="Go Back" 
    cta_url="/"
%}
```

---

### 8. **CTA Banner** (`cta-banner.html`)
**Purpose**: Call-to-action sections with background and button

**Key Features**:
- Gradient background with decorative elements
- Animated floating icons (DNA & Network)
- Title, description, and button
- Staggered fade-in animations
- Responsive padding and font sizes

**Styling**:
```css
- Background: Linear gradient #0f172a → #1e293b
- Border radius: 50px
- Button: Scale on hover (1.05) with glow effect
- Decorative elements: Positioned absolutely with opacity
```

**Usage**:
```django
{% include 'components/cta-banner.html' 
    title="Join KUHIN" 
    text="Become part..." 
    button_text="Join" 
    button_url="/join/"
%}
```

---

## Unified Styling Standards

### Glass Panel Effect
All card-based components use a unified glass-panel style:
```css
.glass-panel {
    background: rgba(248, 249, 250, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(226, 232, 240, 0.5);
}
```

### Hover Animations
**Lift effect** (used on cards):
```css
.hover-lift:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 30px rgba(44, 62, 145, 0.15);
}
```

**Scale effect** (used on buttons):
```css
.hover-scale:hover {
    transform: scale(1.05-1.1);
}
```

### Fade-in Animation
All components use this entrance animation:
```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Text Clamping
- **Line clamp 2**: Used for titles (min-height: 3rem)
- **Line clamp 3**: Used for excerpts
- **Line clamp 4**: Used for longer descriptions

```css
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
```

---

## Responsive Design Breakpoints

### Desktop (≥ 1024px)
- Full component display
- All labels visible
- Optimal spacing and padding

### Tablet (768px - 1023px)
- Adjusted font sizes
- Reduced padding
- Modified column layouts

### Mobile (< 768px)
- Hidden text labels (icons only)
- Reduced padding and spacing
- Smaller minimum touch targets (40px)
- Simplified layouts (single column)

---

## Accessibility Standards

### Color Contrast
- Primary text on backgrounds: ≥ 4.5:1 ratio
- Secondary text: ≥ 3:1 ratio
- Focus indicators: 2px solid outline

### Interactive Elements
- Minimum touch target: 44px × 44px
- Focus states: Visible outline
- ARIA labels: All links and buttons labeled
- Semantic HTML: Proper heading hierarchy

### Motion
- Animations: 0.3s - 0.8s duration
- Easing: cubic-bezier(0.4, 0, 0.2, 1)
- Prefers-reduced-motion: Respected (optional enhancement)

---

## Pages Using These Components

### Homepage (`/`)
- Hero section with hero component
- Feature sections with cards (blog, events, news)
- CTA banner for engagement
- Pagination for featured items

### Team Page (`/team/`)
- Hero section
- Team member cards
- Consistent styling with other pages

### Blog Page (`/blogs/`)
- Hero section
- Blog card grid
- Pagination for blog posts
- Search/filter panel

### Events Page (`/events/`)
- Hero section
- Event card grid
- Status badges
- Pagination support

### Resources Page (`/resources/`)
- Hero section
- Resource cards
- Consistent design with blog/events

---

## Implementation Checklist

- [x] Pagination component updated
- [x] Hero component enhanced
- [x] Breadcrumb styling improved
- [x] Blog card unified
- [x] Event card unified
- [x] News card unified
- [x] Empty state styled
- [x] CTA banner enhanced
- [x] Color system unified
- [x] Animations standardized
- [x] Responsive design verified
- [x] Accessibility enhanced

---

## Future Enhancements

1. **Dark mode support** - Add CSS variables for dark theme
2. **Animation preferences** - Respect `prefers-reduced-motion`
3. **RTL support** - Add right-to-left language support
4. **Additional card types** - Gallery cards, testimonial cards
5. **Theme customization** - Allow CSS variable overrides
6. **Component variants** - Size and style variations

---

## Questions or Issues?

If you encounter any inconsistencies or issues with the components:
1. Check against this guide
2. Verify all component files are up to date
3. Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
4. Run Django server with `python manage.py runserver`
5. Contact the development team

---

**Last Updated**: January 18, 2026
**Version**: 1.0 - Full Component System

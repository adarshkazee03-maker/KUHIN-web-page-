# KUHIN Component Design System

## Overview
This document outlines the unified design system across all reusable template components. All components follow consistent styling, animations, and accessibility standards.

---

## Design Tokens

### Colors
- **Primary Color**: `#0891b2` (`var(--primary-color)`)
- **Primary Dark**: `#0e7490`
- **Secondary Color**: `#64748b`
- **Success**: `#10b981`
- **Warning**: `#f59e0b`
- **Danger**: `#ef4444`
- **Text Dark**: `#1e293b`
- **Text Muted**: `#64748b`
- **Light Background**: `#f8f9fa`
- **Border Color**: `rgba(226, 232, 240, 0.8)`

### Spacing
- Base unit: `0.25rem`
- Padding: `0.5rem`, `1rem`, `1.5rem`, `2rem`, `3rem`, `4rem`, `5rem`
- Gap: `0.25rem`, `0.5rem`, `1rem`, `1.5rem`, `2rem`

### Border Radius
- Small: `6px` to `8px`
- Medium: `12px` to `16px`
- Large: `20px` to `24px` (`rounded-4`)
- XL: `32px` to `48px` (`rounded-5`)

### Typography
- **Heading 1 (display)**: `2.5rem`, `700 weight`
- **Heading 2**: `1.75rem - 2rem`, `700 weight`
- **Heading 3-4**: `1.25rem - 1.5rem`, `600-700 weight`
- **Body**: `1rem`, `400-500 weight`
- **Small**: `0.875rem`, `400-500 weight`

### Shadows
- **Light**: `0 1px 3px rgba(0, 0, 0, 0.1)`
- **Medium**: `0 4px 6px rgba(0, 0, 0, 0.1)`
- **Glow**: `0 0 25px rgba(255, 255, 255, 0.4)`

---

## Shared Utility Classes

### Layout
- `glass-panel`: Modern glassmorphism effect with backdrop blur
- `fade-in-up`: Entrance animation (fade + slide up)
- `transition-all`: Smooth all-property transitions (0.3s ease)
- `transition-transform`: Transform-specific transitions
- `transition-colors`: Color-specific transitions
- `transition-opacity`: Opacity transitions

### Hover Effects
- `hover-lift`: Card elevation on hover with shadow change
- `hover-scale`: Scale up effect on hover (1.08x)
- `group-hover-scale`: Scale when parent `.group` is hovered
- `group-hover-text`: Text color change on parent hover

### Text Utilities
- `line-clamp-2`: Limit text to 2 lines with ellipsis
- `line-clamp-3`: Limit text to 3 lines with ellipsis
- `text-shadow-sm`: Subtle text shadow

---

## Component Standards

### 1. **Pagination Component**
**File**: `templates/components/pagination.html`

**Features**:
- Glass-panel wrapper with rounded corners
- Primary color highlighting for active page
- Chevron icons for navigation clarity
- Hover scale effects on buttons
- Responsive button sizing
- Accessibility labels on all links

**Usage**:
```django
{% include 'components/pagination.html' with page_obj=page_obj %}
```

**Key Styles**:
- Button height: `40px` (desktop), `36px` (mobile)
- Active state: Primary color background
- Hover state: Primary color border + light background

---

### 2. **Breadcrumb Component**
**File**: `templates/components/breadcrumb.html`

**Features**:
- Dynamic breadcrumb items
- Separator styling with `/`
- Home link always included
- Current page indicator with bold styling
- Hover effects with text-shadow glow

**Usage**:
```django
{% include 'components/breadcrumb.html' with breadcrumb_items=breadcrumbs %}
```

**Expected Context**:
```python
breadcrumb_items = [
    {'label': 'Blog', 'url': '/blog/'},
    {'label': 'Article Title', 'url': None}  # None = current page
]
```

---

### 3. **Section Header Component**
**File**: `templates/components/section-header.html`

**Features**:
- Fade-in-up animation on load
- Badge with icon for visual interest
- Underlined title with primary color
- Optional subtitle in muted text
- Responsive font sizing (clamp)

**Usage**:
```django
{% include 'components/section-header.html' with title="Our Services" subtitle="Discover what we offer" %}
```

---

### 4. **Card Components**

#### Card Blog
**File**: `templates/components/card-blog.html`

**Features**:
- Featured image with lazy loading
- Category badge
- Author information
- View count
- Read more link with arrow animation
- Hover lift effect

**Usage**:
```django
{% include 'components/card-blog.html' with blog=blog_post %}
```

---

#### Card Event
**File**: `templates/components/card-event.html`

**Features**:
- Event image header
- Status badge (Upcoming/Ongoing/Past)
- Date overlay with gradient
- Location information
- Event description excerpt
- Responsive layout

**Usage**:
```django
{% include 'components/card-event.html' with event=event_obj %}
```

---

#### Card News
**File**: `templates/components/card-news.html`

**Features**:
- Date badge with icon
- News title
- Description excerpt
- Action button
- Announcement indicator
- Hover reveal effects

**Usage**:
```django
{% include 'components/card-news.html' with news=news_update %}
```

---

### 5. **CTA Banner Component**
**File**: `templates/components/cta-banner.html`

**Features**:
- Gradient background
- Floating decorative elements
- Optional badge
- Call-to-action button
- Responsive typography
- Hover scale effect on button

**Usage**:
```django
{% include 'components/cta-banner.html' with 
    title="Join KUHIN" 
    text="Become part of our community" 
    button_text="Get Started" 
    button_url="/join/" 
%}
```

---

### 6. **Empty State Component**
**File**: `templates/components/empty-state.html`

**Features**:
- Customizable icon
- Title and message
- Call-to-action button
- Scale animation on icon
- Glass panel styling

**Usage**:
```django
{% include 'components/empty-state.html' 
    icon="fas fa-inbox" 
    title="No items found" 
    message="Try adjusting your filters." 
    cta_text="Go Back" 
    cta_url="/" 
%}
```

---

### 7. **Hero Component**
**File**: `templates/components/hero.html`

**Features**:
- Full-width hero section
- Background image with blur effect
- Default gradient fallback
- Badge with optional icon
- Large display heading
- Subtitle support

**Usage**:
```django
{% include 'components/hero.html' 
    title="Welcome to KUHIN" 
    subtitle="Innovating for tomorrow" 
    image_url="/static/img/hero.jpg" 
    badge_text="Featured" 
    badge_icon="fas fa-star" 
%}
```

---

## Animation Standards

### Fade In Up
Entrance animation for components:
```css
animation: fadeInUp 0.6s ease-out;
```

### Hover Effects
- **Scale**: `transform: scale(1.08)`
- **Lift**: `transform: translateY(-8px)`
- **Glow**: `box-shadow: 0 15px 30px rgba(8, 145, 178, 0.1)`

### Transition Timing
- Standard: `0.3s ease`
- Fast: `0.2s ease`
- Smooth: `0.6s ease-out`

---

## Accessibility Standards

✅ **Implemented Across All Components**:
- Semantic HTML (`<nav>`, `<article>`, `<section>`)
- ARIA labels on interactive elements
- `aria-current="page"` for active navigation
- `aria-label` attributes on icon-only buttons
- Alt text on images
- Color contrast compliance (WCAG AA)
- Keyboard navigation support
- Focus indicators

---

## Responsive Breakpoints

- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px
- **Large**: > 1200px

**Mobile-First Approach**: Base styles apply to mobile, then enhanced for larger screens.

---

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

**CSS Features Used**:
- CSS Grid & Flexbox
- CSS Variables (custom properties)
- Backdrop Blur
- CSS Animations
- CSS Gradients
- Object Fit

---

## Color Palette Reference

```
Primary:       #0891b2 (Cyan)
Secondary:     #64748b (Slate)
Success:       #10b981 (Emerald)
Warning:       #f59e0b (Amber)
Danger:        #ef4444 (Red)
Dark:          #1e293b (Slate Dark)
Light:         #f8f9fa (Off White)
```

---

## Icon Library

Using **Font Awesome 6** for all icons:
- Navigation: `fa-chevron-*`, `fa-arrow-*`, `fa-home`
- Content: `fa-newspaper`, `fa-calendar-alt`, `fa-map-marker-alt`
- Social: `fa-linkedin-in`, `fa-github`, `fa-envelope`
- Utility: `fa-star`, `fa-inbox`, `fa-network-wired`

---

## Best Practices

### When Creating New Components:
1. Use `glass-panel` for card-like containers
2. Add `fade-in-up` animation for entrance
3. Include `hover-lift` or `hover-scale` for interactivity
4. Use semantic HTML elements
5. Include proper ARIA labels
6. Wrap styles in `<style>` tag within component
7. Use CSS variables for colors
8. Test on mobile devices
9. Follow the naming conventions in this guide

### Common Patterns:
- **Hover State**: Combine `transition-all` + `hover-*` class
- **Active State**: Primary color background + white text
- **Disabled State**: `opacity-50` + `cursor-not-allowed`
- **Loading State**: Use animation or spinner icon

---

## Updates & Maintenance

Last Updated: January 18, 2026
Design System Version: 2.0
Maintained By: KUHIN Development Team

---

## References

- Bootstrap 5.3 Documentation
- Font Awesome 6 Icons
- WCAG 2.1 Accessibility Guidelines
- CSS Variables Best Practices

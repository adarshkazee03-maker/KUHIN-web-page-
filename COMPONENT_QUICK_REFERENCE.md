# Component Quick Reference Guide

## 🎨 Design System Quick Start

### Primary Colors
```css
Primary:   #0891b2
Secondary: #64748b
Success:   #10b981
Warning:   #f59e0b
Danger:    #ef4444
Dark:      #1e293b
Light:     #f8f9fa
```

### Essential Utility Classes
| Class | Purpose | Example |
|-------|---------|---------|
| `glass-panel` | Glassmorphism container | Card wrapper |
| `fade-in-up` | Entrance animation | Component load |
| `hover-lift` | Elevation on hover | Card hover |
| `hover-scale` | Scale on hover | Button hover |
| `transition-all` | Smooth transitions | Interactive elements |
| `rounded-4` | 24px border radius | Containers |
| `rounded-5` | 48px border radius | Large containers |
| `shadow-sm` | Subtle shadow | Cards |
| `line-clamp-2` | 2-line text limit | Headings |
| `line-clamp-3` | 3-line text limit | Descriptions |

---

## 📦 Components at a Glance

### Pagination
```django
{% include 'components/pagination.html' with page_obj=page_obj %}
```
**Features**: Glass panel, hover effects, accessibility labels, responsive
**Icons**: Chevron double/single arrows

### Breadcrumb
```django
{% include 'components/breadcrumb.html' with breadcrumb_items=breadcrumbs %}
```
**Context Required**:
```python
breadcrumb_items = [
    {'label': 'Home', 'url': '/'},
    {'label': 'Blog', 'url': '/blog/'},
    {'label': 'Article Title', 'url': None}  # Current page
]
```
**Features**: Dynamic items, home link, current page indicator, hover glow

### Section Header
```django
{% include 'components/section-header.html' 
    title="Title Text"
    subtitle="Optional subtitle"
%}
```
**Features**: Badge, underlined title, animations, responsive

### Card Blog
```django
{% include 'components/card-blog.html' with blog=blog_post %}
```
**Blog Model Fields**:
- `featured_image`, `title`, `slug`, `category`, `created_at`
- `author`, `views`, `content`

### Card Event
```django
{% include 'components/card-event.html' with event=event_obj %}
```
**Event Model Fields**:
- `image`, `title`, `slug`, `date`, `location`, `description`, `status`

### Card News
```django
{% include 'components/card-news.html' with news=news_update %}
```
**News Model Fields**:
- `title`, `slug`, `description`, `created_at`

### CTA Banner
```django
{% include 'components/cta-banner.html'
    title="Call to Action"
    text="Description text"
    button_text="Button Text"
    button_url="/path/"
%}
```

### Empty State
```django
{% include 'components/empty-state.html'
    icon="fas fa-inbox"
    title="No Items"
    message="Description"
    cta_text="Go Back"
    cta_url="/"
%}
```

### Hero
```django
{% include 'components/hero.html'
    title="Page Title"
    subtitle="Subtitle"
    image_url="/static/img/hero.jpg"
    badge_text="Badge"
    badge_icon="fas fa-star"
%}
```

---

## 🎯 Common Patterns

### Button Styling
```html
<!-- Primary Button -->
<a href="/link" class="btn btn-primary rounded-pill px-4 py-2">
    Button Text
</a>

<!-- Secondary Button -->
<button class="btn btn-outline-primary rounded-pill px-4 py-2 hover-scale">
    Button Text
</button>
```

### Card Container
```html
<div class="glass-panel h-100 p-4 rounded-4 hover-lift transition-all">
    <!-- Card content -->
</div>
```

### Hover Effects
```html
<!-- Hover Scale -->
<div class="hover-scale">Scale on hover</div>

<!-- Hover Lift -->
<div class="hover-lift transition-all">Lift on hover</div>

<!-- Hover with Color -->
<a class="transition-colors hover-text-primary">Colored link</a>
```

### Animations
```html
<!-- Fade in on load -->
<div class="fade-in-up">Fades in from bottom</div>

<!-- With delay -->
<h1 class="fade-in-up" style="transition-delay: 0.1s;">Delayed animation</h1>
```

### Responsive Text
```html
<!-- Responsive heading -->
<h1 style="font-size: clamp(1.5rem, 5vw, 2.5rem);">
    Responsive Title
</h1>
```

### Icon + Text
```html
<span class="d-flex align-items-center gap-2">
    <i class="fas fa-icon"></i>
    Text content
</span>
```

---

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

### Common Responsive Classes
```html
<!-- Show on desktop only -->
<div class="d-none d-lg-block">Desktop content</div>

<!-- Show on mobile only -->
<div class="d-lg-none">Mobile content</div>

<!-- Responsive padding -->
<div class="p-2 p-md-3 p-lg-4">Responsive padding</div>

<!-- Responsive text size -->
<h2 class="fs-1 fs-md-2 fs-lg-3">Responsive heading</h2>
```

---

## ♿ Accessibility Checklist

- [ ] Semantic HTML (`<nav>`, `<article>`, `<section>`)
- [ ] ARIA labels on interactive elements
- [ ] `aria-current="page"` on active navigation
- [ ] Alt text on all images
- [ ] Color contrast WCAG AA compliant
- [ ] Keyboard navigation working
- [ ] Focus indicators visible
- [ ] Form labels associated with inputs
- [ ] Error messages linked to form fields
- [ ] Title attributes on icon-only buttons

---

## 🎨 Typography

### Heading Sizes
```html
<h1 class="display-4 fw-bold">Display 4 - Main heading</h1>
<h2 class="fs-2 fw-bold">Heading 2 - Section</h2>
<h3 class="fs-3 fw-bold">Heading 3 - Subsection</h3>
<h4 class="fs-4 fw-bold">Heading 4 - Card title</h4>
```

### Text Weights
- `fw-light` - 300
- `fw-normal` - 400
- `fw-semibold` - 600
- `fw-bold` - 700

### Text Colors
```html
<p class="text-dark">Dark text</p>
<p class="text-muted">Muted text</p>
<p class="text-primary">Primary color</p>
<p class="text-white-50">Light on dark</p>
```

---

## 🔧 Debugging Tips

### Common Issues

**Component not showing**
- Check include path: `{% include 'components/filename.html' %}`
- Verify context variables passed
- Check template syntax in Django

**Styles not applying**
- Verify CSS variables are defined in main stylesheet
- Check Bootstrap version compatibility
- Clear browser cache
- Inspect element for specificity issues

**Animations not working**
- Ensure animation-duration is defined
- Check if animations disabled in user preferences
- Verify `fade-in-up` class is applied
- Check browser DevTools timeline

**Icons not showing**
- Verify Font Awesome is loaded in base template
- Use correct icon class: `fas` (solid), `far` (regular), `fab` (brand)
- Check icon name spelling
- Add `me-2` or `ms-2` for spacing

---

## 🚀 Performance Tips

1. **Use lazy loading on images**
   ```html
   <img src="..." loading="lazy" alt="...">
   ```

2. **Optimize animations**
   - Use `transform` and `opacity` (GPU-accelerated)
   - Avoid animating `width`, `height`, `left`, `top`

3. **CSS Variables usage**
   - Define at root or component level
   - Use for colors, sizes, transitions
   - Fallbacks for browser support

4. **Class usage**
   - Leverage Bootstrap utilities
   - Minimize custom CSS
   - Use utility classes over inline styles

---

## 📚 Resources

- **Font Awesome**: https://fontawesome.com/
- **Bootstrap 5**: https://getbootstrap.com/
- **CSS Variables**: MDN Web Docs
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

---

## 💬 Template Syntax Quick Ref

```django
{# Comments #}
{{ variable }}
{% tag %}

{# Conditionals #}
{% if condition %}
    <p>Content</p>
{% endif %}

{# Loops #}
{% for item in items %}
    <div>{{ item }}</div>
{% endfor %}

{# Includes #}
{% include 'components/file.html' with param=value %}

{# URL reversal #}
{% url 'view_name' arg1 arg2 %}

{# Static files #}
{% load static %}
<img src="{% static 'img/file.png' %}" alt="...">

{# Filters #}
{{ text|truncatewords:20 }}
{{ date|date:"M d, Y" }}
{{ text|upper }}
```

---

**Last Updated**: January 18, 2026
**Version**: 2.0

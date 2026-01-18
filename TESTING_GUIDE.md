# Quick Testing Guide - Search & Homepage Features

## Prerequisites
- Django development server running: `python3 manage.py runserver`
- Admin user created: `python3 manage.py createsuperuser`
- Some sample content (blogs, events, news, members, resources)

---

## Testing Search Functionality

### 1. Global Search
**URL**: `http://localhost:8000/search/?q=django`

**Steps**:
1. Visit the search page with a query parameter
2. Click "All" filter to see all results
3. Try filtering by content type (Blog, News, Event, etc.)
4. Use date filters to narrow results
5. Verify results appear with correct metadata

**Expected Results**:
- Results grouped by content type
- Badges showing content type (BLOG, NEWS, EVENT, etc.)
- View counts for blogs
- Location for events
- Status badges for events

### 2. Autocomplete Search
**Steps**:
1. Go to `http://localhost:8000/search/`
2. Click in the search box
3. Type at least 2 characters (e.g., "hea")
4. Wait 300ms for debounce
5. Dropdown suggestions should appear

**Expected Results**:
- Suggestions appear in dropdown
- Includes recent searches, blog titles, event names, member names
- Clicking a suggestion fills search box and submits
- Works with arrow keys and Enter

### 3. Trending Searches
**Steps**:
1. Go to search page with query: `http://localhost:8000/search/?q=health`
2. Look at right sidebar "Trending Searches"
3. Try different search terms
4. Visit `/search/trending/` to see trending page

**Expected Results**:
- Popular searches displayed with tag styling
- Clicking trending tag performs that search
- Trending page shows trending content across all types

### 4. Search Analytics (Admin)
**Steps**:
1. Go to Admin: `http://localhost:8000/admin/`
2. Navigate to Search Queries
3. Perform some searches on the site
4. Refresh admin page

**Expected Results**:
- Search queries listed with count
- Count increases with repeated searches
- Sorted by popularity and recency
- Last searched date updates

---

## Testing Homepage Interactive Features

### 1. Hero Carousel
**Steps**:
1. Go to Admin and add announcements:
   - Add 2-3 announcements with different titles
   - Set different display orders
   - Make them all active
2. Go to homepage: `http://localhost:8000/`
3. Watch the carousel

**Expected Results**:
- First announcement shows automatically
- Carousel transitions every 5 seconds
- Dots at bottom are clickable
- Current slide highlighted
- Smooth fade transitions
- CTA button works if link provided

### 2. Event Countdown Timer
**Steps**:
1. Make sure you have an upcoming event
2. Go to Admin → Events
3. Verify event has:
   - Status = "upcoming"
   - Date in future
   - Time set
4. Go to homepage

**Expected Results**:
- Countdown section displays at top
- Shows event title and location
- Timer counts down in real-time
- Updates every second
- Days, Hours, Minutes, Seconds shown

### 3. Statistics Counter Animation
**Steps**:
1. Go to homepage
2. Scroll to Stats Counter section
3. Watch the numbers animate

**Expected Results**:
- Numbers animate from 0 to target value
- Takes about 2 seconds
- Animation triggers when scrolled into view
- Only animates once per page load
- Shows member count, events held, blog posts

### 4. Member Spotlight
**Steps**:
1. Go to Admin → Member Spotlights
2. Add a spotlight:
   - Select a member
   - Add spotlight title
   - Add custom text about member
   - Add key achievement
   - Set as active
   - Set current dates
3. Go to homepage

**Expected Results**:
- Member spotlight displays prominently
- Shows member photo
- Displays name and position
- Shows custom spotlight text
- Shows key achievement badge
- If no spotlight, shows random active member

### 5. Achievements Section
**Steps**:
1. Go to Admin → Achievements
2. Add several achievements:
   - Set as featured
   - Add different types (Award, Milestone, etc.)
   - Select Font Awesome icons (fa-trophy, fa-star, etc.)
   - Add title and description
   - (Optional) Add stat value and label
3. Go to homepage

**Expected Results**:
- Featured achievements display in grid
- Icons show for each achievement
- Can scroll through multiple achievements
- Hover effect on cards
- Statistics box appears if stat_value set

### 6. Testimonials Section
**Steps**:
1. Go to Admin → Testimonials
2. Add several testimonials:
   - Mark as featured
   - Set different ratings (3-5 stars)
   - Upload photos or leave blank
   - Set display order
3. Go to homepage

**Expected Results**:
- 3 featured testimonials display in row
- Shows testimonial text in italic
- Shows author name, position, and photo
- Star rating displays correctly
- Hover effects work
- Responsive on mobile (stacks vertically)

### 7. Latest Content Grid
**Steps**:
1. Make sure you have:
   - At least 3 published blogs
   - At least 5 active news updates
   - At least 3 upcoming events
2. Go to homepage

**Expected Results**:
- Latest blogs section shows 3 most recent
- Latest news shows 5 most recent
- Upcoming events shows 3 soonest events
- Each item shows relevant metadata
- "View All" buttons link to respective pages
- Responsive layout on mobile

### 8. Activity Feed
**Steps**:
1. Admin adds/publishes blog posts or news
2. Go to Admin → Activity Feed
3. Verify new activities auto-created
4. Go to homepage

**Expected Results**:
- Latest activities show in timeline
- Shows type icon and color
- Shows title and description
- Shows "X ago" timestamp
- Links to related content if available
- Timeline style with icons

### 9. Trending Content
**Steps**:
1. Make sure you have viewed blogs recently
2. Go to Admin → Content Views
3. Check weekly_views counts
4. Go to homepage

**Expected Results**:
- Trending section shows top 3 blogs this week
- Displays view counts
- Numbered 1, 2, 3
- Links to trending blog posts
- Ranked by weekly views

---

## Testing Admin Interfaces

### Search Queries Admin
**URL**: `http://localhost:8000/admin/search/searchquery/`

**Steps**:
1. Perform several searches on site
2. Open this admin page
3. Verify queries listed

**Expected Results**:
- All searches logged with count
- Count increases on repeated searches
- Last searched date updates
- Searchable by query text
- Read-only (can't add manually)

### Content Views Admin
**URL**: `http://localhost:8000/admin/search/contentview/`

**Steps**:
1. Visit some blog posts and pages
2. Open this admin page
3. Check view counts

**Expected Results**:
- Content tracked with view counts
- Content type shows (blog, news, etc.)
- Object ID identifies which item
- Weekly views tracked separately
- Sortable by views
- Read-only (auto-tracked)

### Announcements Admin
**URL**: `http://localhost:8000/admin/homepage_features/announcement/`

**Steps**:
1. Add an announcement with:
   - Title: "Welcome!"
   - Subtitle: "Test subtitle"
   - Button text: "Learn More"
   - Button link: `/about/`
   - Set active
   - Set background color to #667eea
2. Check "Currently Active" indicator
3. Refresh homepage to see it

**Expected Results**:
- Announcement appears in admin list
- "Currently Active" shows as checkmark if active
- Announcement shows on homepage if active and in date range
- Can edit display order
- Fieldsets organize settings logically

### Testimonials Admin
**URL**: `http://localhost:8000/admin/homepage_features/testimonial/`

**Steps**:
1. Add testimonial with:
   - Name: "John Doe"
   - Position: "Club President"
   - Text: "This club is amazing!"
   - Rating: 5
   - Mark as featured
2. Refresh homepage

**Expected Results**:
- Testimonial appears in grid if featured
- Rating shows as stars
- Name and position display correctly
- Featured ones show on homepage first

---

## Performance Testing

### 1. Page Load Time
- First load: Should be < 2 seconds
- Subsequent loads: Should be < 1 second

### 2. Search Response Time
- Autocomplete: Should respond in < 500ms
- Search results: Should render in < 1 second
- Trending: Should load instantly

### 3. Admin Interface
- Admin pages load quickly (< 2 seconds)
- Can handle hundreds of records smoothly

---

## Mobile Testing

### Steps:
1. Open homepage on mobile browser
2. Test search on mobile
3. Test carousel swipes
4. Test filter chips scroll

**Expected Results**:
- Responsive layout works
- Text readable on small screens
- Buttons easily tappable
- Images optimize for mobile
- Carousel works with touch

---

## Troubleshooting

### Search not showing results
- Check that content is published/active
- Verify models have required fields
- Check database has data

### Carousel not rotating
- Check JavaScript console for errors
- Verify announcements are active
- Check browser supports CSS animations

### Countdown not updating
- Check event has future date
- Verify JavaScript enabled
- Check browser console for errors

### Stats not animating
- Try scrolling page to trigger
- Check JavaScript enabled
- Inspect browser console

---

## Browser Compatibility

Tested and working on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Required features:
- CSS3 animations
- JavaScript ES6
- Intersection Observer API
- Fetch API

---

## Sample Test Data SQL

To reset and add test data:

```sql
-- Clear existing data
DELETE FROM search_searchquery;
DELETE FROM search_contentview;
DELETE FROM homepage_features_announcement;
DELETE FROM homepage_features_testimonial;
DELETE FROM homepage_features_achievement;

-- Example: Add test announcement
INSERT INTO homepage_features_announcement 
(title, subtitle, background_color, is_active, display_order, start_date, end_date)
VALUES ('Welcome to KUHIN', 'Join our community', '#667eea', 1, 0, NOW(), NULL);

-- Example: Add test testimonial
INSERT INTO homepage_features_testimonial 
(name, position, testimonial_text, rating, is_featured, display_order)
VALUES ('Alice Smith', 'Member', 'Great club!', 5, 1, 0);
```

---

## Notes

- All timestamps use Asia/Kathmandu timezone
- Images auto-optimize with Pillow
- CKEditor handles rich text in announcements
- Admin uses Bootstrap 5 styling
- All models include created_at and updated_at timestamps
- Models support soft delete via is_active flag (where applicable)

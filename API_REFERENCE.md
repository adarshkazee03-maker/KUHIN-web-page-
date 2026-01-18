# API Reference - Search & Discovery System

## Base URL
```
http://localhost:8000/search/
```

---

## Endpoints

### 1. Global Search
**URL**: `/search/`  
**Method**: `GET`  
**Content-Type**: `text/html`

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search query (minimum 1 character) |
| type | string | No | Content type filter: 'all', 'blog', 'news', 'event', 'resource', 'member' (default: 'all') |
| date_from | date | No | Start date filter (YYYY-MM-DD) |
| date_to | date | No | End date filter (YYYY-MM-DD) |
| page | int | No | Page number for pagination (future) |

#### Example Requests
```
GET /search/?q=health
GET /search/?q=django&type=blog
GET /search/?q=event&type=event&date_from=2025-01-01&date_to=2025-12-31
```

#### Response
Returns HTML page with results grouped by content type.

**Result Card Structure**:
```html
<div class="result-card">
    <span class="badge">TYPE</span>
    <h3>Content Title</h3>
    <div class="meta">Author, Date, Category</div>
    <div class="snippet">First 30 words of content</div>
</div>
```

#### Success Response
- Status: 200 OK
- Shows results with:
  - Total result count
  - Results grouped by type
  - Trending searches sidebar
  - Pagination (future)

#### Example
```bash
curl "http://localhost:8000/search/?q=health&type=blog"
```

---

### 2. Autocomplete Suggestions
**URL**: `/search/autocomplete/`  
**Method**: `GET`  
**Content-Type**: `application/json`

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Query text (minimum 2 characters for suggestions) |

#### Response Format
```json
{
    "suggestions": [
        "health informatics",
        "health and wellness",
        "healthy lifestyle",
        "John Health",
        "...more suggestions"
    ]
}
```

#### Status Codes
- **200**: Success with suggestions array (can be empty)
- **400**: Bad request (invalid parameters)

#### Examples

**Request with results**:
```bash
curl "http://localhost:8000/search/autocomplete/?q=hea"
```

**Response**:
```json
{
    "suggestions": [
        "health informatics",
        "Health Tech Blog",
        "Healthcare Awareness",
        "Helen - Member"
    ]
}
```

**Request without results**:
```bash
curl "http://localhost:8000/search/autocomplete/?q=xyz"
```

**Response**:
```json
{
    "suggestions": []
}
```

#### Implementation (JavaScript)
```javascript
const query = 'hea';
const response = await fetch(`/search/autocomplete/?q=${encodeURIComponent(query)}`);
const data = await response.json();
console.log(data.suggestions); // Array of suggestions
```

---

### 3. Trending Content
**URL**: `/search/trending/`  
**Method**: `GET`  
**Content-Type**: `text/html`

#### Parameters
None required. Shows trending content across all types.

#### Response
Returns HTML page displaying trending content with:
- Trending blog posts
- Trending news
- Trending events
- Trending resources

#### Example
```bash
curl "http://localhost:8000/search/trending/"
```

---

### 4. Quick Stats API
**URL**: `/search/api/stats/`  
**Method**: `GET`  
**Content-Type**: `application/json`

#### Response Format
```json
{
    "total_blogs": 45,
    "total_news": 23,
    "total_events": 12,
    "total_resources": 78,
    "total_members": 34,
    "trending_searches": [
        {
            "query": "django",
            "count": 15
        },
        {
            "query": "health",
            "count": 12
        },
        {
            "query": "python",
            "count": 8
        }
    ]
}
```

#### Example
```bash
curl "http://localhost:8000/search/api/stats/"
```

#### Use Cases
- Homepage statistics display
- Admin dashboard
- Analytics reporting
- Real-time content metrics

---

### 5. Recommendations
**URL**: `/search/recommendations/<content_type>/<object_id>/`  
**Method**: `GET`  
**Content-Type**: `text/html`

#### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| content_type | string | Yes | Type of content: 'blog', 'news', 'event', 'resource', 'member' |
| object_id | int | Yes | Primary key of the content item |

#### Response
Returns recommendations for similar content based on:
1. Same category (if applicable)
2. Trending similar content

#### Status Codes
- **200**: Recommendations found
- **404**: Content not found
- **400**: Invalid content type

#### Examples
```bash
# Get recommendations for blog post with ID 5
curl "http://localhost:8000/search/recommendations/blog/5/"

# Get recommendations for event with ID 3
curl "http://localhost:8000/search/recommendations/event/3/"
```

#### Side Effects
- Records a view for the content
- Records user interaction for personalization
- Updates content view metrics

---

## Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Search returns results |
| 400 | Bad Request | Missing required parameter |
| 404 | Not Found | Recommendations for non-existent content |
| 500 | Server Error | Database connection error |

---

## Search Result Structure

### Blog Result
```json
{
    "type": "blog",
    "id": 1,
    "title": "Django Best Practices",
    "author": "John Doe",
    "category": "Technology",
    "created_at": "2025-01-15",
    "views": 245,
    "snippet": "This blog discusses Django best practices..."
}
```

### Event Result
```json
{
    "type": "event",
    "id": 3,
    "title": "Health Informatics Workshop",
    "date": "2025-02-20",
    "time": "14:30",
    "location": "Main Hall",
    "status": "upcoming",
    "snippet": "Learn about health informatics in this workshop..."
}
```

### Member Result
```json
{
    "type": "member",
    "id": 5,
    "name": "Alice Johnson",
    "position": "Project Lead",
    "email": "alice@example.com",
    "photo_url": "/media/members/alice.jpg"
}
```

### News Result
```json
{
    "type": "news",
    "id": 2,
    "title": "New Partnership Announcement",
    "created_at": "2025-01-14",
    "snippet": "We are excited to announce our new partnership..."
}
```

### Resource Result
```json
{
    "type": "resource",
    "id": 7,
    "title": "Health Data Standards Guide",
    "category": "Documentation",
    "resource_type": "document",
    "is_featured": true,
    "snippet": "Complete guide to health data standards..."
}
```

---

## Rate Limiting & Caching

### Current Implementation
- No rate limiting on search endpoints
- Database queries are unoptimized (for future caching)
- Sessions tracked for recommendation system

### Recommended Future Implementation
```python
@cache_page(60 * 5)  # Cache for 5 minutes
def trending_content(request):
    # Returns cached trending data
    pass

@ratelimit(key='ip', rate='100/h', method='GET')
def global_search(request):
    # Max 100 searches per hour per IP
    pass
```

---

## Error Responses

### Missing Query Parameter
```json
{
    "error": "Search query is required",
    "query": null
}
```

### Invalid Content Type
```json
{
    "error": "Invalid content type",
    "valid_types": ["blog", "news", "event", "resource", "member"]
}
```

### Database Error
```json
{
    "error": "Unable to fetch search results",
    "status": "error"
}
```

---

## Data Models Reference

### SearchQuery (for search tracking)
```python
{
    "id": 1,
    "query": "django",
    "count": 15,  # Total search count
    "created_at": "2025-01-01T10:00:00Z",
    "last_searched": "2025-01-15T14:30:00Z"
}
```

### ContentView (for trending calculation)
```python
{
    "id": 1,
    "content_type": "blog",
    "object_id": 5,
    "view_count": 245,  # All-time views
    "weekly_views": 43,  # Views this week
    "last_viewed": "2025-01-15T14:30:00Z",
    "weekly_reset_date": "2025-01-08"
}
```

### UserRecommendation (for personalization)
```python
{
    "id": 1,
    "session_key": "abc123def456...",
    "content_type": "blog",
    "object_id": 5,
    "interaction_type": "view",  # view, click, read, search
    "score": 1.0,  # Weighted score
    "created_at": "2025-01-15T14:30:00Z"
}
```

---

## Integration Examples

### JavaScript - Fetch Search Results
```javascript
async function searchContent(query, type = 'all') {
    const params = new URLSearchParams({
        q: query,
        type: type
    });
    
    const response = await fetch(`/search/?${params}`);
    const html = await response.text();
    document.getElementById('results').innerHTML = html;
}

// Usage
searchContent('django', 'blog');
```

### JavaScript - Get Autocomplete Suggestions
```javascript
async function getSuggestions(query) {
    if (query.length < 2) return [];
    
    const response = await fetch(`/search/autocomplete/?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    return data.suggestions;
}

// Usage with debounce
let debounceTimer;
document.getElementById('searchInput').addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        getSuggestions(e.target.value).then(suggestions => {
            console.log('Suggestions:', suggestions);
        });
    }, 300);
});
```

### Python - Get Stats
```python
import requests

response = requests.get('http://localhost:8000/search/api/stats/')
stats = response.json()

print(f"Total blogs: {stats['total_blogs']}")
print(f"Total events: {stats['total_events']}")
print(f"Trending searches: {stats['trending_searches']}")
```

---

## Performance Metrics

### Search Response Time
- < 500ms for < 100 results
- < 2s for large datasets
- Can be optimized with caching

### Autocomplete Response
- < 200ms typical
- Debounced at 300ms client-side
- Combines multiple sources efficiently

### Trending Calculation
- < 100ms for top 10
- Weekly views reset on schedule
- Cacheable for 24 hours

---

## Security Considerations

### Input Validation
- Query strings sanitized with `striptags`
- SQL injection prevented via Django ORM
- XSS prevention via template escaping

### Rate Limiting (Future)
- Implement per-IP rate limiting
- Session-based user throttling
- API key management for external access

### CSRF Protection
- All POST requests require CSRF token
- GET endpoints are CSRF-exempt (intended)
- Safe for third-party integration

---

## Versioning

Current API Version: **1.0**

Future versions may include:
- v2: JSON API endpoints for all search
- v2: Advanced filtering options
- v2: Pagination support
- v3: GraphQL endpoint

---

## Support & Documentation

- Full implementation guide: See `SEARCH_HOMEPAGE_FEATURES_GUIDE.md`
- Testing guide: See `TESTING_GUIDE.md`
- Admin guide: See project documentation

/**
 * KUHIN Web Portal - Bio-Digital Theme JavaScript
 * Handles animations, scroll effects, and interactive UI elements
 * Bio-digital enhanced user experience
 */

document.addEventListener('DOMContentLoaded', function() {
    
    /* -----------------------------------------------------------
       1. Navbar Scroll Effect (Glassmorphism toggle)
    ----------------------------------------------------------- */
    const navbar = document.getElementById('mainNav');
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            navbar.classList.add('shadow-sm');
            navbar.style.padding = '0.5rem 0';
        } else {
            navbar.classList.remove('shadow-sm');
            navbar.style.padding = '1rem 0';
        }
        
        // Hide navbar on scroll down, show on scroll up (mobile)
        if (window.innerWidth < 768) {
            if (currentScroll > lastScroll && currentScroll > 300) {
                navbar.style.transform = 'translateY(-100%)';
            } else {
                navbar.style.transform = 'translateY(0)';
            }
        }
        
        lastScroll = currentScroll;
    });

    /* -----------------------------------------------------------
       2. Scroll Reveal Animation (Intersection Observer)
    ----------------------------------------------------------- */
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, observerOptions);

    // Observe fade-in and slide-in elements
    const animatedElements = document.querySelectorAll(
        '.fade-in-up, .slide-in-left, .slide-in-right, .slide-in-up'
    );
    animatedElements.forEach(el => observer.observe(el));


    /* -----------------------------------------------------------
       3. Hero Parallax Effect (Advanced)
    ----------------------------------------------------------- */
    const heroPattern = document.querySelector('.hero-bg-pattern');
    if (heroPattern) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            heroPattern.style.transform = `translateY(${scrolled * 0.4}px)`;
        });
    }

    /* -----------------------------------------------------------
       4. Card Hover 3D Tilt Effect (Subtle Enhanced)
    ----------------------------------------------------------- */
    const cards = document.querySelectorAll(
        '.stat-card, .timeline-content, .card:not(.modal-content)'
    );
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Very subtle movement for elegant effect
            const moveX = (x - rect.width / 2) / 20; 
            const moveY = (y - rect.height / 2) / 20;

            card.style.transform = `translate(${moveX}px, ${moveY}px))`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translate(0, 0)';
        });
    });

    /* -----------------------------------------------------------
       5. Search Modal Interactive Enhancement
    ----------------------------------------------------------- */
    const searchModal = document.getElementById('searchModal');
    const searchInput = searchModal ? searchModal.querySelector('input') : null;
    
    if (searchModal && searchInput) {
        searchModal.addEventListener('show.bs.modal', function () {
            setTimeout(() => searchInput.focus(), 100);
        });

        // Search suggestions on input
        searchInput.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length > 2) {
                // Add search suggestions via API call here
                console.log('Search query:', query);
            }
        }, 300));

        // Clear on ESC
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                searchInput.value = '';
            }
        });
    }

    /* -----------------------------------------------------------
       6. Global Keyboard Shortcuts
    ----------------------------------------------------------- */
    document.addEventListener('keydown', function(e) {
        // Press "/" to open search
        if (e.key === '/' && !searchInput) {
            if (searchModal) {
                const modal = new bootstrap.Modal(searchModal);
                modal.show();
            }
            e.preventDefault();
        }
        
        // Press "Escape" to close modals
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                bootstrap.Modal.getInstance(modal).hide();
            });
        }
    });

    /* -----------------------------------------------------------
       7. Active Navigation Link Indicator
    ----------------------------------------------------------- */
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const currentLocation = location.pathname;

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active');
        }
    });

    /* -----------------------------------------------------------
       8. Smooth Scroll Behavior
    ----------------------------------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                const headerOffset = 100;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    /* -----------------------------------------------------------
       9. Stat Counter Animation (Number Increment)
    ----------------------------------------------------------- */
    const statCards = document.querySelectorAll('.stat-card h3, .stat-card .display-5');
    
    function animateStats() {
        statCards.forEach(stat => {
            const finalValue = parseInt(stat.textContent);
            if (!isNaN(finalValue)) {
                let currentValue = 0;
                const increment = Math.ceil(finalValue / 30);
                const interval = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        stat.textContent = finalValue;
                        clearInterval(interval);
                    } else {
                        stat.textContent = currentValue;
                    }
                }, 30);
            }
        });
    }

    // Trigger animation when stats section is visible
    const statsSection = document.querySelector('.stats-container, .stats-section');
    if (statsSection) {
        const statsObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                animateStats();
                statsObserver.unobserve(statsSection);
            }
        }, { threshold: 0.1 });
        
        statsObserver.observe(statsSection);
    }

    /* -----------------------------------------------------------
       10. Form Validation Enhancement
    ----------------------------------------------------------- */
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    /* -----------------------------------------------------------
       11. Loading State Enhancement
    ----------------------------------------------------------- */
    document.addEventListener('click', function(e) {
        if (e.target.matches('button[type="submit"]')) {
            const button = e.target;
            const originalText = button.textContent;
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            
            setTimeout(() => {
                button.disabled = false;
                button.textContent = originalText;
            }, 3000);
        }
    });

    /* -----------------------------------------------------------
       12. Responsive Image Lazy Loading
    ----------------------------------------------------------- */
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    /* -----------------------------------------------------------
       13. Mobile Menu Auto-Close
    ----------------------------------------------------------- */
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks2 = navbarCollapse ? navbarCollapse.querySelectorAll('.nav-link') : [];
    
    navLinks2.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                navbarCollapse.classList.remove('show');
            }
        });
    });

    /* -----------------------------------------------------------
       14. Utility: Debounce Function
    ----------------------------------------------------------- */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /* -----------------------------------------------------------
       15. Page Load Animation
    ----------------------------------------------------------- */
    window.addEventListener('load', function() {
        document.body.classList.add('page-loaded');
    });

    /* -----------------------------------------------------------
       16. Fade-in All Elements on Load
    ----------------------------------------------------------- */
    document.querySelectorAll('.fade-in-up').forEach((el, index) => {
        el.style.setProperty('--animation-delay', `${index * 0.1}s`);
    });

});

/* --- Additional Global Utilities --- */

// Tooltip initialization (Bootstrap)
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Popover initialization (Bootstrap)
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

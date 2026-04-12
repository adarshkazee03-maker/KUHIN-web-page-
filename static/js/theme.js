// Theme Toggle JavaScript
const THEME_KEY = 'kuhin-theme';
const html = document.getElementById('html-root');
const toggleBtn = document.getElementById('theme-toggle');
const icon = document.getElementById('theme-icon');
const label = document.getElementById('theme-label');

function getSystemTheme() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function getCurrentTheme() {
  return localStorage.getItem(THEME_KEY) || getSystemTheme();
}

function applyTheme(theme) {
  if (!html) return;
  
  html.setAttribute('data-bs-theme', theme);
  
  if (icon) {
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
  
  if (label) {
    label.textContent = theme === 'dark' ? 'Light' : 'Dark';
  }
  
  // Update button title
  if (toggleBtn) {
    toggleBtn.title = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
  }
}

function toggleTheme() {
  const current = getCurrentTheme();
  const next = current === 'dark' ? 'light' : 'dark';
  localStorage.setItem(THEME_KEY, next);
  applyTheme(next);
}

// Apply theme on page load
document.addEventListener('DOMContentLoaded', function() {
  applyTheme(getCurrentTheme());
  
  // Add navbar scroll effect
  const navbar = document.getElementById('mainNav');
  if (navbar) {
    window.addEventListener('scroll', function() {
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }
});

// Sync if user changes OS preference while tab is open
// Only if user hasn't explicitly set a preference
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  if (!localStorage.getItem(THEME_KEY)) {
    applyTheme(e.matches ? 'dark' : 'light');
  }
});

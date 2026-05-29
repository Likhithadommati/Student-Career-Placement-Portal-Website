// Main JavaScript for Career Portal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers
    initBootstrap();
    
    // Form validation
    setupFormValidation();
    
    // Other utilities
    setupUtilities();
});

// Initialize Bootstrap components
function initBootstrap() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            // Remove and re-add was-validated class for re-validation
            form.classList.add('was-validated');
        }, false);
    });
}

// Utilities
function setupUtilities() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Smooth scroll for anchor links
    setupSmoothScroll();
    
    // Confirm delete actions
    setupDeleteConfirmation();
}

// Smooth scroll
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Delete confirmation
function setupDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-delete, .delete-btn, [data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

// Skill progress update
function updateSkillProgress(skillId, percentage) {
    const progressBar = document.querySelector(`[data-skill-id="${skillId}"] .progress-bar`);
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';
    }
}

// Real-time search
function setupLiveSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            const searchTerm = this.value.toLowerCase();
            const items = document.querySelectorAll('.searchable-item');
            
            items.forEach(item => {
                if (item.textContent.toLowerCase().includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
}

// Chart initialization for dashboard
function initializeDashboardCharts() {
    // Skills Chart
    const skillsCtx = document.getElementById('skillsChart');
    if (skillsCtx) {
        new Chart(skillsCtx, {
            type: 'doughnut',
            data: {
                labels: ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
                datasets: [{
                    data: window.skillsData || [0, 0, 0, 0],
                    backgroundColor: [
                        '#ffc107',
                        '#17a2b8',
                        '#28a745',
                        '#007bff'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true
            }
        });
    }
    
    // Progress Chart
    const progressCtx = document.getElementById('progressChart');
    if (progressCtx) {
        new Chart(progressCtx, {
            type: 'bar',
            data: {
                labels: window.progressLabels || [],
                datasets: [{
                    label: 'Progress %',
                    data: window.progressData || [],
                    backgroundColor: '#007bff'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Toggle password visibility
function setupPasswordToggle() {
    const toggleButtons = document.querySelectorAll('.password-toggle');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.previousElementSibling;
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            }
        });
    });
}

// API call helper
async function apiCall(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Call Error:', error);
        showAlert('An error occurred. Please try again.', 'danger');
    }
}

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.getElementById('alertContainer') || 
                          document.querySelector('.container-fluid');
    
    if (alertContainer) {
        const alertDiv = document.createElement('div');
        alertDiv.innerHTML = alertHTML;
        alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
        
        // Auto close after 5 seconds
        setTimeout(() => {
            alertDiv.querySelector('.btn-close').click();
        }, 5000);
    }
}

// Pagination
function setupPagination() {
    const paginationLinks = document.querySelectorAll('.pagination a');
    paginationLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.href) {
                window.location.href = this.href;
            }
        });
    });
}

// Initialize on page load
window.addEventListener('load', function() {
    setupPasswordToggle();
    setupLiveSearch();
    setupPagination();
    initializeDashboardCharts();
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in-on-scroll').forEach(el => {
    observer.observe(el);
});

// Add fade-in animation class
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        animation: fadeIn 0.6s ease-in forwards;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

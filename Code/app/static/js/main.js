// Main JavaScript for Chirec

// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Auto-hide flash messages after 5 seconds
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// User Mode Toggle
function toggleUserMode() {
    fetch('/api/toggle-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => console.error('Error toggling mode:', error));
}

// Socket.IO Setup for Real-time Messaging
let socket;
if (typeof io !== 'undefined') {
    socket = io();

    socket.on('connect', function() {
        console.log('Connected to server');
    });

    socket.on('new_message', function(data) {
        handleNewMessage(data);
    });

    socket.on('message_count', function(data) {
        updateMessageCount(data.count);
    });
}

function handleNewMessage(data) {
    // Update UI with new message
    const messageContainer = document.getElementById('messages-container');
    if (messageContainer) {
        const messageElement = createMessageElement(data);
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    // Update unread count
    updateMessageCount();
}

function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message-bubble ${message.is_sender ? 'sent' : 'received'}`;
    div.innerHTML = `
        <p>${escapeHtml(message.content)}</p>
        <span class="text-xs opacity-75">${formatTime(message.timestamp)}</span>
    `;
    return div;
}

function updateMessageCount(count) {
    const countElement = document.getElementById('message-count');
    if (countElement) {
        if (count && count > 0) {
            countElement.textContent = count > 99 ? '99+' : count;
            countElement.style.display = 'flex';
        } else {
            countElement.style.display = 'none';
        }
    }
}

// Send Message Function
function sendMessage(conversationId, content) {
    if (socket) {
        socket.emit('send_message', {
            conversation_id: conversationId,
            content: content
        });
    }
}

// Infinite Scroll for Job Feed
function initJobScroller() {
    const scroller = document.getElementById('job-scroller');
    if (!scroller) return;

    let isLoading = false;
    let page = 1;

    scroller.addEventListener('scroll', function() {
        if (isLoading) return;

        const scrollPosition = scroller.scrollTop + scroller.clientHeight;
        const scrollHeight = scroller.scrollHeight;

        if (scrollPosition >= scrollHeight - 100) {
            loadMoreJobs(++page);
        }
    });
}

function loadMoreJobs(page) {
    isLoading = true;

    fetch(`/jobs/feed?page=${page}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.jobs && data.jobs.length > 0) {
            appendJobs(data.jobs);
        }
        isLoading = false;
    })
    .catch(error => {
        console.error('Error loading jobs:', error);
        isLoading = false;
    });
}

function appendJobs(jobs) {
    const container = document.getElementById('job-scroller');
    jobs.forEach(job => {
        const jobCard = createJobCard(job);
        container.appendChild(jobCard);
    });
}

function createJobCard(job) {
    const div = document.createElement('div');
    div.className = 'job-card-fullscreen';
    div.innerHTML = `
        <div class="max-w-2xl w-full bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8">
            <div class="flex items-center justify-between mb-4">
                <h2 class="text-3xl font-bold text-gray-800 dark:text-white">${escapeHtml(job.title)}</h2>
                <button onclick="saveJob(${job.id})" class="text-blue-600 hover:text-blue-700">
                    <i class="fas fa-bookmark text-2xl"></i>
                </button>
            </div>
            <p class="text-xl text-gray-600 dark:text-gray-400 mb-4">${escapeHtml(job.company)}</p>
            <p class="text-gray-700 dark:text-gray-300 mb-6">${escapeHtml(job.description)}</p>
            <div class="flex flex-wrap gap-2 mb-6">
                ${job.skills.map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`).join('')}
            </div>
            <div class="flex gap-4">
                <button onclick="applyJob(${job.id})" class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition">
                    Apply Now
                </button>
                <button onclick="skipJob(${job.id})" class="flex-1 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white py-3 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition">
                    Skip
                </button>
            </div>
        </div>
    `;
    return div;
}

// Job Actions
function saveJob(jobId) {
    fetch(`/jobs/${jobId}/save`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Job saved!', 'success');
        }
    })
    .catch(error => console.error('Error saving job:', error));
}

function applyJob(jobId) {
    window.location.href = `/jobs/${jobId}/apply`;
}

function skipJob(jobId) {
    // Scroll to next job
    const scroller = document.getElementById('job-scroller');
    if (scroller) {
        scroller.scrollBy({
            top: window.innerHeight,
            behavior: 'smooth'
        });
    }
}

// Event Actions
function enrollEvent(eventId) {
    fetch(`/events/${eventId}/enroll`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Successfully enrolled!', 'success');
            location.reload();
        } else {
            showNotification(data.message || 'Enrollment failed', 'error');
        }
    })
    .catch(error => console.error('Error enrolling:', error));
}

function bookmarkEvent(eventId) {
    fetch(`/events/${eventId}/bookmark`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Event bookmarked!', 'success');
        }
    })
    .catch(error => console.error('Error bookmarking:', error));
}

// Utility Functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;

    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;

    return date.toLocaleDateString();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} bg-white dark:bg-gray-800 shadow-lg rounded-lg p-4 max-w-md flex items-center justify-between animate-slide-in fixed top-20 right-4 z-50`;

    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle';
    const color = type === 'success' ? 'green' : type === 'error' ? 'red' : 'blue';

    notification.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-${icon} text-${color}-500 mr-3"></i>
            <span class="text-gray-800 dark:text-gray-200">${escapeHtml(message)}</span>
        </div>
        <button onclick="this.parentElement.remove()" class="ml-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <i class="fas fa-times"></i>
        </button>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initJobScroller();

    // Request notification permission for messages
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
});

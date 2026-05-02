/**
 * API Helper Functions
 * Handles all API calls to the backend
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Make API call to backend
 * @param {string} endpoint - API endpoint (e.g., '/auth/login')
 * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
 * @param {object} data - Request body data
 * @returns {Promise} Response data
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        // Get token from localStorage
        const token = localStorage.getItem('token');
        
        // Prepare request options
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        // Add Authorization header if token exists
        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }
        
        // Add request body if data is provided
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        // Make API call
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        // Parse response
        const responseData = await response.json();
        
        // Handle errors
        if (!response.ok) {
            throw new Error(responseData.error || `API Error: ${response.status}`);
        }
        
        return responseData;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Format date to readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Get status badge HTML
 * @param {string} status - Task status
 * @returns {string} HTML badge
 */
function getStatusBadge(status) {
    const statusMap = {
        'todo': 'To Do',
        'in_progress': 'In Progress',
        'done': 'Done'
    };
    
    return `<span class="status-badge status-${status}">${statusMap[status] || status}</span>`;
}

/**
 * Check if date is overdue
 * @param {string} dateString - ISO date string
 * @returns {boolean} True if date is in the past
 */
function isOverdue(dateString) {
    if (!dateString) return false;
    return new Date(dateString) < new Date();
}

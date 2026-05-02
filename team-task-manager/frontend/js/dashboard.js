/**
 * Dashboard Page Functions
 * Handles dashboard statistics and recent tasks
 */

// Store current project filter
let currentProjectFilter = null;

/**
 * Initialize dashboard
 */
async function initDashboard() {
    try {
        // Load projects for filter
        await loadProjectsFilter();
        
        // Load initial stats
        await loadDashboardStats();
        
        // Load projects summary
        await loadProjectsSummary();
        
        // Load recent tasks
        await loadRecentTasks();
        
        // Setup event listeners
        setupEventListeners();
    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

/**
 * Load projects for filter dropdown
 */
async function loadProjectsFilter() {
    try {
        const response = await apiCall('/projects', 'GET');
        const projectFilter = document.getElementById('projectFilter');
        
        // Clear existing options except the first one
        projectFilter.innerHTML = '<option value="">All Projects</option>';
        
        // Add project options
        response.projects.forEach(project => {
            const option = document.createElement('option');
            option.value = project.id;
            option.textContent = project.title;
            projectFilter.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading projects filter:', error);
    }
}

/**
 * Load dashboard statistics
 */
async function loadDashboardStats() {
    try {
        const queryParam = currentProjectFilter ? `?project_id=${currentProjectFilter}` : '';
        const response = await apiCall(`/dashboard/stats${queryParam}`, 'GET');
        
        // Update stat cards
        document.getElementById('totalTasks').textContent = response.total_tasks;
        document.getElementById('completedTasks').textContent = response.completed_tasks;
        document.getElementById('pendingTasks').textContent = response.pending_tasks;
        document.getElementById('overdueTasks').textContent = response.overdue_tasks;
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

/**
 * Load projects summary
 */
async function loadProjectsSummary() {
    try {
        const response = await apiCall('/dashboard/projects-summary', 'GET');
        const container = document.getElementById('projectsSummary');
        
        container.innerHTML = '';
        
        if (response.projects.length === 0) {
            container.innerHTML = '<p>No projects found. <a href="projects.html">Create one</a></p>';
            return;
        }
        
        response.projects.forEach(item => {
            const project = item.project;
            const progressPercent = item.total_tasks > 0 
                ? (item.completed_tasks / item.total_tasks * 100).toFixed(0)
                : 0;
            
            const card = document.createElement('div');
            card.className = 'project-summary-card';
            card.innerHTML = `
                <h4>${project.title}</h4>
                <p style="font-size: 0.9rem; color: #666;">${project.description || 'No description'}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progressPercent}%"></div>
                </div>
                <div class="task-counts">
                    <span>Total: ${item.total_tasks}</span>
                    <span>Completed: ${item.completed_tasks}</span>
                    <span>Pending: ${item.pending_tasks}</span>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading projects summary:', error);
    }
}

/**
 * Load recent tasks
 */
async function loadRecentTasks() {
    try {
        const queryParam = currentProjectFilter ? `?project_id=${currentProjectFilter}` : '';
        const response = await apiCall(`/dashboard/tasks${queryParam}`, 'GET');
        const tableBody = document.getElementById('tasksTableBody');
        
        tableBody.innerHTML = '';
        
        if (response.tasks.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">No tasks found</td></tr>';
            return;
        }
        
        // Show only first 10 tasks
        response.tasks.slice(0, 10).forEach(task => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${task.title}</strong></td>
                <td>${task.project_id}</td>
                <td>${getStatusBadge(task.status)}</td>
                <td>${task.assigned_user ? task.assigned_user.name : 'Unassigned'}</td>
                <td>${formatDate(task.due_date)}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading recent tasks:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Project filter change
    document.getElementById('projectFilter').addEventListener('change', async (e) => {
        currentProjectFilter = e.target.value || null;
        await loadDashboardStats();
        await loadRecentTasks();
    });
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    initDashboard();
});

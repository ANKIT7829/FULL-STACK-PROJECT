/**
 * Tasks Page Functions
 * Handles user's assigned tasks
 */

let currentTaskId = null;
let currentUser = null;

/**
 * Initialize tasks page
 */
async function initTasks() {
    try {
        currentUser = getCurrentUser();
        
        // Load projects for filter
        await loadProjectsFilterTasks();
        
        // Load my tasks
        await loadMyTasks();
        
        // Setup event listeners
        setupTaskEventListeners();
        
        // Setup modals
        setupTaskModals();
    } catch (error) {
        console.error('Error initializing tasks page:', error);
    }
}

/**
 * Load projects for filter dropdown
 */
async function loadProjectsFilterTasks() {
    try {
        const response = await apiCall('/projects', 'GET');
        const projectFilter = document.getElementById('projectFilterTasks');
        
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
 * Load user's assigned tasks
 */
async function loadMyTasks() {
    try {
        const statusFilter = document.getElementById('statusFilter').value;
        const projectFilter = document.getElementById('projectFilterTasks').value;
        
        let url = '/dashboard/my-tasks';
        const params = [];
        
        if (statusFilter) {
            params.push(`status=${statusFilter}`);
        }
        
        if (projectFilter) {
            params.push(`project_id=${projectFilter}`);
        }
        
        if (params.length > 0) {
            url += '?' + params.join('&');
        }
        
        const response = await apiCall(url, 'GET');
        const tableBody = document.getElementById('myTasksTableBody');
        
        tableBody.innerHTML = '';
        
        if (response.tasks.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">No tasks found</td></tr>';
            return;
        }
        
        response.tasks.forEach(task => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${task.title}</strong></td>
                <td>Project ${task.project_id}</td>
                <td>${getStatusBadge(task.status)}</td>
                <td>${formatDate(task.due_date)}</td>
                <td>
                    <div class="task-actions">
                        <button class="btn btn-primary btn-small" onclick="openTaskEditModal(${task.id})">Edit</button>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading my tasks:', error);
    }
}

/**
 * Setup event listeners
 */
function setupTaskEventListeners() {
    // Status filter change
    document.getElementById('statusFilter').addEventListener('change', loadMyTasks);
    
    // Project filter change
    document.getElementById('projectFilterTasks').addEventListener('change', loadMyTasks);
}

/**
 * Setup task modals
 */
function setupTaskModals() {
    // Close buttons for edit modal
    document.querySelectorAll('#taskEditModal .close-btn, #taskEditModal .close-modal-btn').forEach(btn => {
        btn.addEventListener('click', closeTaskEditModal);
    });
    
    // Form submit
    document.getElementById('taskEditForm').addEventListener('submit', updateTask);
}

/**
 * Open task edit modal
 */
async function openTaskEditModal(taskId) {
    try {
        currentTaskId = taskId;
        const response = await apiCall(`/tasks/${taskId}`, 'GET');
        const task = response;
        
        // Populate form
        document.getElementById('editTaskTitle').value = task.title;
        document.getElementById('editTaskDescription').value = task.description || '';
        document.getElementById('editTaskStatus').value = task.status;
        
        // Format date for input
        if (task.due_date) {
            const date = new Date(task.due_date);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            document.getElementById('editTaskDueDate').value = `${year}-${month}-${day}`;
        }
        
        // Open modal
        document.getElementById('taskEditModal').classList.add('active');
    } catch (error) {
        alert('Error loading task: ' + error.message);
    }
}

/**
 * Close task edit modal
 */
function closeTaskEditModal() {
    document.getElementById('taskEditModal').classList.remove('active');
    document.getElementById('taskEditForm').reset();
}

/**
 * Update task
 */
async function updateTask(e) {
    e.preventDefault();
    
    try {
        const title = document.getElementById('editTaskTitle').value;
        const description = document.getElementById('editTaskDescription').value;
        const status = document.getElementById('editTaskStatus').value;
        const due_date = document.getElementById('editTaskDueDate').value;
        
        const data = {
            title,
            description,
            status
        };
        
        if (due_date) {
            data.due_date = due_date;
        }
        
        await apiCall(`/tasks/${currentTaskId}`, 'PUT', data);
        
        // Reload tasks and close modal
        await loadMyTasks();
        closeTaskEditModal();
        
        alert('Task updated successfully');
    } catch (error) {
        alert('Error updating task: ' + error.message);
    }
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    initTasks();
});

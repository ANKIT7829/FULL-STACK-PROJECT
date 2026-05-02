/**
 * Projects Page Functions
 * Handles project management and member management
 */

let currentProjectId = null;
let currentUser = null;

/**
 * Initialize projects page
 */
async function initProjects() {
    try {
        currentUser = getCurrentUser();
        
        // Show admin controls if user is admin
        if (isAdmin()) {
            document.getElementById('adminControls').style.display = 'block';
            setupCreateProjectBtn();
        }
        
        // Load projects
        await loadProjects();
        
        // Setup modals
        setupModals();
    } catch (error) {
        console.error('Error initializing projects:', error);
    }
}

/**
 * Load all projects
 */
async function loadProjects() {
    try {
        const response = await apiCall('/projects', 'GET');
        const container = document.getElementById('projectsContainer');
        
        container.innerHTML = '';
        
        if (response.projects.length === 0) {
            if (isAdmin()) {
                container.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No projects yet. <button class="btn btn-primary" onclick="openCreateProjectModal()">Create one</button></p>';
            } else {
                container.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">No projects assigned to you.</p>';
            }
            return;
        }
        
        response.projects.forEach(project => {
            const card = document.createElement('div');
            card.className = 'project-card';
            
            const actions = `
                <div class="project-actions">
                    <button class="btn btn-primary btn-small" onclick="openProjectDetails(${project.id})">View</button>
                    ${isAdmin() ? `
                        <button class="btn btn-secondary btn-small" onclick="editProject(${project.id})">Edit</button>
                        <button class="btn btn-danger btn-small" onclick="deleteProject(${project.id})">Delete</button>
                    ` : ''}
                </div>
            `;
            
            card.innerHTML = `
                <h3>${project.title}</h3>
                <p>${project.description || 'No description'}</p>
                <div class="project-meta">
                    <span>Creator: ${project.creator.name}</span>
                    <span>Members: ${project.members ? project.members.length : 0}</span>
                </div>
                ${actions}
            `;
            
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

/**
 * Setup create project button
 */
function setupCreateProjectBtn() {
    document.getElementById('createProjectBtn').addEventListener('click', openCreateProjectModal);
}

/**
 * Open create project modal
 */
function openCreateProjectModal() {
    document.getElementById('projectModal').classList.add('active');
}

/**
 * Close project modal
 */
function closeProjectModal() {
    document.getElementById('projectModal').classList.remove('active');
    document.getElementById('projectForm').reset();
}

/**
 * Setup modals
 */
function setupModals() {
    // Close buttons for create project modal
    document.querySelectorAll('#projectModal .close-btn, #projectModal .close-modal-btn').forEach(btn => {
        btn.addEventListener('click', closeProjectModal);
    });
    
    // Close buttons for project details modal
    document.querySelectorAll('#projectDetailsModal .close-btn, #projectDetailsModal .close-modal-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById('projectDetailsModal').classList.remove('active');
        });
    });
    
    // Form submit
    document.getElementById('projectForm').addEventListener('submit', createProject);
}

/**
 * Create new project
 */
async function createProject(e) {
    e.preventDefault();
    
    const title = document.getElementById('projectTitle').value;
    const description = document.getElementById('projectDescription').value;
    
    try {
        await apiCall('/projects', 'POST', { title, description });
        
        // Reload projects and close modal
        await loadProjects();
        closeProjectModal();
        
        // Show success message
        alert('Project created successfully');
    } catch (error) {
        alert('Error creating project: ' + error.message);
    }
}

/**
 * Open project details modal
 */
async function openProjectDetails(projectId) {
    try {
        currentProjectId = projectId;
        const response = await apiCall(`/projects/${projectId}`, 'GET');
        const project = response;
        
        // Update modal content
        document.getElementById('detailsProjectTitle').textContent = project.title;
        document.getElementById('detailsProjectDescription').textContent = project.description || 'No description';
        
        // Load team members if admin
        if (isAdmin()) {
            loadTeamMembers(projectId);
        }
        
        // Load tasks
        loadProjectTasks(projectId);
        
        // Open modal
        document.getElementById('projectDetailsModal').classList.add('active');
    } catch (error) {
        alert('Error loading project: ' + error.message);
    }
}

/**
 * Load team members
 */
async function loadTeamMembers(projectId) {
    try {
        const teamSection = document.getElementById('teamMembersSection');
        teamSection.style.display = 'block';
        
        // In a full app, we'd fetch members from the project details
        // For now, showing placeholder
        document.getElementById('teamMembersList').innerHTML = '<p>Team members list</p>';
        document.getElementById('adminMemberControls').style.display = 'block';
    } catch (error) {
        console.error('Error loading team members:', error);
    }
}

/**
 * Load project tasks
 */
async function loadProjectTasks(projectId) {
    try {
        const response = await apiCall(`/tasks?project_id=${projectId}`, 'GET');
        const tasksList = document.getElementById('projectTasksList');
        
        tasksList.innerHTML = '';
        
        if (response.tasks.length === 0) {
            tasksList.innerHTML = '<tr><td colspan="4" style="text-align: center;">No tasks yet</td></tr>';
            return;
        }
        
        response.tasks.forEach(task => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${task.title}</td>
                <td>${getStatusBadge(task.status)}</td>
                <td>${task.assigned_user ? task.assigned_user.name : 'Unassigned'}</td>
                <td>${formatDate(task.due_date)}</td>
            `;
            tasksList.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading project tasks:', error);
    }
}

/**
 * Delete project
 */
async function deleteProject(projectId) {
    if (!confirm('Are you sure you want to delete this project? All tasks will be deleted.')) {
        return;
    }
    
    try {
        await apiCall(`/projects/${projectId}`, 'DELETE');
        
        // Reload projects
        await loadProjects();
        
        alert('Project deleted successfully');
    } catch (error) {
        alert('Error deleting project: ' + error.message);
    }
}

/**
 * Edit project (placeholder - can be extended)
 */
function editProject(projectId) {
    alert('Edit functionality can be implemented');
}

/**
 * Initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    initProjects();
});

<template>
  <div class="app">
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed }">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-mark">
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
              <rect x="2" y="2" width="8" height="8" rx="2" fill="#3b82f6"/>
              <rect x="12" y="2" width="8" height="8" rx="2" fill="#93c5fd"/>
              <rect x="2" y="12" width="8" height="8" rx="2" fill="#93c5fd"/>
              <rect x="12" y="12" width="8" height="8" rx="2" fill="#3b82f6"/>
            </svg>
          </div>
          <div class="logo-text">
            <h1>{{ t('nav.companyName') }}</h1>
            <span class="subtitle">{{ t('nav.subtitle') }}</span>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav" aria-label="Primary">
        <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M3 11L3 17C3 17.5523 3.44772 18 4 18L7 18C7.55228 18 8 17.5523 8 17L8 11" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M12 7L12 17C12 17.5523 12.4477 18 13 18L16 18C16.5523 18 17 17.5523 17 17L17 7" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M3 18L17 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M2 11L7 5L11 8L18 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.overview') }}</span>
        </router-link>

        <router-link to="/inventory" class="nav-item" :class="{ active: $route.path === '/inventory' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2L17.5 6.25V13.75L10 18L2.5 13.75V6.25L10 2Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M2.5 6.25L10 10.5L17.5 6.25" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M10 10.5V18" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.inventory') }}</span>
        </router-link>

        <router-link to="/orders" class="nav-item" :class="{ active: $route.path === '/orders' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5 2.5H15C15.5523 2.5 16 2.94772 16 3.5V17.5L13 15.5L10 17.5L7 15.5L4 17.5V3.5C4 2.94772 4.44772 2.5 5 2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M7 7H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M7 10.5H13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.orders') }}</span>
        </router-link>

        <router-link to="/spending" class="nav-item" :class="{ active: $route.path === '/spending' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 2V18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M13.5 5.5C13.5 4.11929 11.9853 3 10.1 3H9.9C8.01472 3 6.5 4.11929 6.5 5.5C6.5 6.88071 8.01472 8 9.9 8H10.1C11.9853 8 13.5 9.11929 13.5 10.5C13.5 11.8807 11.9853 13 10.1 13H9.9C8.01472 13 6.5 11.8807 6.5 10.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.finance') }}</span>
        </router-link>

        <router-link to="/demand" class="nav-item" :class="{ active: $route.path === '/demand' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M2.5 17.5L7 11L10.5 14L17.5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M13 5H17.5V9.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span class="nav-label">{{ t('nav.demandForecast') }}</span>
        </router-link>

        <router-link to="/restocking" class="nav-item" :class="{ active: $route.path === '/restocking' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C12.1472 3 14.0705 3.96995 15.3511 5.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M15 2.5V5.5H12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span class="nav-label">Restocking</span>
        </router-link>

        <router-link to="/reports" class="nav-item" :class="{ active: $route.path === '/reports' }">
          <span class="nav-icon" aria-hidden="true">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M5.5 2.5H11.5L15.5 6.5V16.5C15.5 17.0523 15.0523 17.5 14.5 17.5H5.5C4.94772 17.5 4.5 17.0523 4.5 16.5V3.5C4.5 2.94772 4.94772 2.5 5.5 2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M11.5 2.5V6.5H15.5" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M7.5 10.5H12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              <path d="M7.5 13.5H12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </span>
          <span class="nav-label">Reports</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button class="collapse-btn" @click="toggleSidebar" :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" :style="{ transform: sidebarCollapsed ? 'rotate(180deg)' : 'none' }">
            <path d="M11 3.5L5.5 9L11 14.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="nav-label">Collapse</span>
        </button>
      </div>
    </aside>

    <div class="app-body">
      <header class="top-header">
        <div class="search-bar">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="5.5" stroke="currentColor" stroke-width="1.5"/>
            <path d="M12.5 12.5L16 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="search"
            class="search-input"
            placeholder="Search inventory, orders..."
            aria-label="Search inventory and orders"
          />
        </div>

        <div class="header-actions">
          <div class="header-notifications">
            <button
              class="icon-button"
              @click="toggleNotifications"
              @blur="handleNotificationsBlur"
              title="Notifications"
              aria-label="Notifications"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2.5C7.51472 2.5 5.5 4.51472 5.5 7V9.5C5.5 10.5 5 11.5 4.5 12.25C4.16667 12.75 4.5 13.5 5.1 13.5H14.9C15.5 13.5 15.8333 12.75 15.5 12.25C15 11.5 14.5 10.5 14.5 9.5V7C14.5 4.51472 12.4853 2.5 10 2.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                <path d="M8 16C8 16.8284 8.89543 17.5 10 17.5C11.1046 17.5 12 16.8284 12 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
              <span class="notification-dot" aria-hidden="true"></span>
            </button>

            <div v-if="showNotifications" class="dropdown-panel notifications-panel">
              <div class="dropdown-panel-title">Notifications</div>
              <div class="notifications-empty">No new notifications</div>
            </div>
          </div>

          <div class="header-settings">
            <button
              class="icon-button"
              @click="toggleSettings"
              @blur="handleSettingsBlur"
              title="Settings"
              aria-label="Settings"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 12.5C11.3807 12.5 12.5 11.3807 12.5 10C12.5 8.61929 11.3807 7.5 10 7.5C8.61929 7.5 7.5 8.61929 7.5 10C7.5 11.3807 8.61929 12.5 10 12.5Z" stroke="currentColor" stroke-width="1.5"/>
                <path d="M16.25 10C16.25 10.3 16.23 10.59 16.2 10.88L17.5 11.9C17.63 12 17.66 12.18 17.58 12.33L16.33 14.52C16.25 14.67 16.07 14.73 15.92 14.67L14.39 14.05C14.07 14.3 13.72 14.5 13.34 14.66L13.11 16.29C13.08 16.45 12.95 16.56 12.79 16.56H10.29C10.13 16.56 10 16.45 9.98 16.29L9.75 14.66C9.37 14.5 9.02 14.3 8.7 14.05L7.17 14.67C7.02 14.73 6.84 14.67 6.76 14.52L5.51 12.33C5.43 12.18 5.46 12 5.59 11.9L6.89 10.88C6.86 10.59 6.84 10.29 6.84 10C6.84 9.71 6.86 9.41 6.89 9.12L5.59 8.1C5.46 8 5.43 7.82 5.51 7.67L6.76 5.48C6.84 5.33 7.02 5.27 7.17 5.33L8.7 5.95C9.02 5.7 9.37 5.5 9.75 5.34L9.98 3.71C10 3.55 10.13 3.44 10.29 3.44H12.79C12.95 3.44 13.08 3.55 13.11 3.71L13.34 5.34C13.72 5.5 14.07 5.7 14.39 5.95L15.92 5.33C16.07 5.27 16.25 5.33 16.33 5.48L17.58 7.67C17.66 7.82 17.63 8 17.5 8.1L16.2 9.12C16.23 9.41 16.25 9.7 16.25 10Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              </svg>
            </button>

            <div v-if="showSettings" class="dropdown-panel settings-panel">
              <div class="dropdown-panel-title">Language</div>
              <LanguageSwitcher />
            </div>
          </div>

          <ProfileMenu
            @show-profile-details="showProfileDetails = true"
            @show-tasks="showTasks = true"
          />
        </div>
      </header>

      <FilterBar />

      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const showProfileDetails = ref(false)
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Sidebar collapse state
    const sidebarCollapsed = ref(false)
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }

    // Header search (UI-only; no backend search endpoint exists yet)
    const searchQuery = ref('')

    // Notifications dropdown (placeholder content, no API wired yet)
    const showNotifications = ref(false)
    const toggleNotifications = () => {
      showNotifications.value = !showNotifications.value
    }
    const handleNotificationsBlur = () => {
      setTimeout(() => {
        showNotifications.value = false
      }, 200)
    }

    // Settings dropdown (hosts the language switcher, moved out of the header)
    const showSettings = ref(false)
    const toggleSettings = () => {
      showSettings.value = !showSettings.value
    }
    const handleSettingsBlur = () => {
      setTimeout(() => {
        showSettings.value = false
      }, 200)
    }

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    // Tasks are loaded from currentUser.value.tasks, no API endpoint needed
    // onMounted(loadTasks)

    return {
      t,
      sidebarCollapsed,
      toggleSidebar,
      searchQuery,
      showNotifications,
      toggleNotifications,
      handleNotificationsBlur,
      showSettings,
      toggleSettings,
      handleSettingsBlur,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #ffffff;
  color: #0f172a;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: flex;
  min-height: 100vh;
}

/* ---------- Sidebar ---------- */

.sidebar {
  width: 260px;
  flex-shrink: 0;
  background: #f8fafc;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  transition: width 0.2s ease;
  z-index: 110;
}

.sidebar.collapsed {
  width: 76px;
}

.sidebar-header {
  padding: 1.25rem 1.25rem 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  overflow: hidden;
}

.logo-mark {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
}

.sidebar.collapsed .logo-text {
  display: none;
}

.logo h1 {
  font-size: 1.0625rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
  line-height: 1.2;
}

.subtitle {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 400;
  display: block;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  color: #475569;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: 8px;
  transition: background-color 0.15s ease, color 0.15s ease;
  white-space: nowrap;
  overflow: hidden;
}

.nav-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar.collapsed .nav-label {
  display: none;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
}

.nav-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.nav-item.active {
  background: #dbeafe;
  color: #3b82f6;
}

.sidebar-footer {
  padding: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  background: none;
  border: none;
  border-radius: 8px;
  color: #64748b;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.collapse-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.collapse-btn svg {
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.sidebar.collapsed .collapse-btn {
  justify-content: center;
}

.sidebar.collapsed .collapse-btn .nav-label {
  display: none;
}

/* ---------- App body / top header ---------- */

.app-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.top-header {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1.5rem;
  height: 64px;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  max-width: 420px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-bar:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: #ffffff;
}

.search-icon {
  color: #94a3b8;
  flex-shrink: 0;
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  font-family: inherit;
  font-size: 0.875rem;
  color: #0f172a;
  width: 100%;
}

.search-input::placeholder {
  color: #94a3b8;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-left: auto;
}

.icon-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-button:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #0f172a;
}

.notification-dot {
  position: absolute;
  top: 7px;
  right: 8px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ef4444;
  border: 1.5px solid #ffffff;
}

.header-notifications,
.header-settings {
  position: relative;
}

.dropdown-panel {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 240px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 0.75rem;
}

.dropdown-panel-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.625rem;
  padding: 0 0.25rem;
}

.notifications-empty {
  padding: 0.75rem 0.25rem;
  font-size: 0.875rem;
  color: #64748b;
  text-align: center;
}

/* ---------- Main content ---------- */

.main-content {
  flex: 1;
  width: 100%;
  padding: 1.5rem;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.375rem;
  letter-spacing: -0.025em;
}

.page-header p {
  color: #64748b;
  font-size: 0.938rem;
}

/* Responsive grid: 1 col mobile, 2 col tablet, 3 col desktop */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-card {
  background: white;
  padding: 1.25rem;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.stat-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.625rem;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: #ea580c;
}

.stat-card.success .stat-value {
  color: #059669;
}

.stat-card.danger .stat-value {
  color: #dc2626;
}

.stat-card.info .stat-value {
  color: #2563eb;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.25rem;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.875rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
  border-bottom: 1px solid #e2e8f0;
}

th {
  text-align: left;
  padding: 0.5rem 0.75rem;
  font-weight: 600;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid #f1f5f9;
  color: #334155;
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

.badge {
  display: inline-block;
  padding: 0.313rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: #d1fae5;
  color: #065f46;
}

.badge.warning {
  background: #fed7aa;
  color: #92400e;
}

.badge.danger {
  background: #fecaca;
  color: #991b1b;
}

.badge.info {
  background: #dbeafe;
  color: #1e40af;
}

.badge.increasing {
  background: #d1fae5;
  color: #065f46;
}

.badge.decreasing {
  background: #fecaca;
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: #fecaca;
  color: #991b1b;
}

.badge.medium {
  background: #fed7aa;
  color: #92400e;
}

.badge.low {
  background: #dbeafe;
  color: #1e40af;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  font-size: 0.938rem;
}

/* ---------- Responsive ---------- */

@media (max-width: 768px) {
  .sidebar {
    width: 76px;
  }

  .sidebar .logo-text,
  .sidebar .nav-label {
    display: none;
  }

  .sidebar .nav-item,
  .sidebar .collapse-btn {
    justify-content: center;
  }

  .search-bar {
    max-width: 220px;
  }
}
</style>

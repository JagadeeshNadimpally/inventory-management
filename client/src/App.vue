<template>
  <div class="app" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo-mark">IM</div>
        <span class="sidebar-company">{{ t('nav.companyName') }}</span>
        <button
          class="sidebar-toggle"
          @click="toggleSidebar"
          :title="sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M4 6H20M4 12H20M4 18H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/" class="sidebar-link" :class="{ active: $route.path === '/' }" :title="t('nav.overview')">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="3" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="13" y="3" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="3" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2"/>
            <rect x="13" y="13" width="8" height="8" rx="1" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span class="sidebar-label">{{ t('nav.overview') }}</span>
        </router-link>

        <router-link to="/inventory" class="sidebar-link" :class="{ active: $route.path === '/inventory' }" :title="t('nav.inventory')">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M21 8L12 3L3 8L12 13L21 8Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M3 8V16L12 21L21 16V8" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M12 13V21" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span class="sidebar-label">{{ t('nav.inventory') }}</span>
        </router-link>

        <router-link to="/orders" class="sidebar-link" :class="{ active: $route.path === '/orders' }" :title="t('nav.orders')">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <rect x="5" y="4" width="14" height="17" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M9 3H15V5H9V3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            <path d="M8 11H16M8 15H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="sidebar-label">{{ t('nav.orders') }}</span>
        </router-link>

        <router-link to="/spending" class="sidebar-link" :class="{ active: $route.path === '/spending' }" :title="t('nav.finance')">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M12 2V22" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M17 6C17 6 15 5 12 5C9 5 7 6.5 7 8.5C7 10.5 9 11 12 11.5C15 12 17 12.5 17 15C17 17 15 18.5 12 18.5C9 18.5 7 17 7 17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="sidebar-label">{{ t('nav.finance') }}</span>
        </router-link>

        <router-link to="/demand" class="sidebar-link" :class="{ active: $route.path === '/demand' }" :title="t('nav.demandForecast')">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M3 17L9 11L13 15L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M15 7H21V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="sidebar-label">{{ t('nav.demandForecast') }}</span>
        </router-link>

        <router-link to="/reports" class="sidebar-link" :class="{ active: $route.path === '/reports' }" title="Reports">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M4 20V10M12 20V4M20 20V14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span class="sidebar-label">Reports</span>
        </router-link>

        <router-link to="/restocking" class="sidebar-link" :class="{ active: $route.path === '/restocking' }" title="Restocking">
          <svg class="sidebar-icon" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M21 12A9 9 0 1 1 18.5 5.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <path d="M21 4V8H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 9V15M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
          <span class="sidebar-label">Restocking</span>
        </router-link>
      </nav>
    </aside>

    <div class="main-area">
      <header class="top-bar">
        <input type="text" class="search-input" placeholder="Search...">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
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

    const storedCollapsed = localStorage.getItem('sidebar-collapsed')
    const sidebarCollapsed = ref(
      storedCollapsed !== null ? storedCollapsed === 'true' : window.innerWidth < 1024
    )

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebar-collapsed', sidebarCollapsed.value.toString())
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

    onMounted(loadTasks)

    return {
      t,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask,
      sidebarCollapsed,
      toggleSidebar
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
  background: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
  transition: grid-template-columns 0.2s ease;
}

.app.sidebar-collapsed {
  grid-template-columns: 72px 1fr;
}

.sidebar {
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  height: 100vh;
  z-index: 100;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 1rem;
  height: 70px;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.logo-mark {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.813rem;
  letter-spacing: 0.025em;
}

.sidebar-company {
  flex: 1;
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-collapsed .sidebar-company {
  display: none;
}

.sidebar-toggle {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.375rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.sidebar-toggle:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.sidebar-collapsed .sidebar-toggle {
  margin: 0 auto;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.75rem;
  overflow-y: auto;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.938rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.sidebar-link:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.sidebar-link.active {
  color: #2563eb;
  background: #eff6ff;
}

.sidebar-icon {
  flex-shrink: 0;
}

.sidebar-label {
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-collapsed .sidebar-label {
  display: none;
}

.sidebar-collapsed .sidebar-link {
  justify-content: center;
}

.main-area {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.top-bar {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  z-index: 90;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 2rem;
  height: 70px;
}

.search-input {
  flex: 1;
  max-width: 320px;
  padding: 0.5rem 0.875rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.875rem;
  font-family: inherit;
  color: #1e293b;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: #cbd5e1;
  background: white;
}

.top-bar > .language-switcher {
  margin-left: auto;
}

.main-content {
  flex: 1;
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
  padding: 1.5rem 2rem;
}

@media (max-width: 640px) {
  .app,
  .app.sidebar-collapsed {
    grid-template-columns: 72px 1fr;
  }

  .sidebar-company,
  .sidebar-label {
    display: none;
  }

  .sidebar-link {
    justify-content: center;
  }

  .sidebar-toggle {
    margin: 0 auto;
  }
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
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
  border-radius: 10px;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.25rem;
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
</style>

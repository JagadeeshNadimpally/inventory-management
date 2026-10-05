<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.budgetSection.title') }}</h3>
        </div>
        <div class="budget-controls">
          <div class="budget-stat">
            <span class="budget-stat-label">{{ t('restocking.budgetSection.maxBudgetLabel') }}</span>
            <span class="budget-stat-value">{{ currencySymbol }}{{ maxBudget.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</span>
          </div>
          <div class="budget-slider-group">
            <label class="budget-slider-label">
              {{ t('restocking.budgetSection.budgetLabel') }}:
              <strong>{{ currencySymbol }}{{ budgetValue.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</strong>
            </label>
            <input
              type="range"
              class="budget-slider"
              min="0"
              :max="maxBudget || 0"
              step="100"
              v-model.number="budgetValue"
            />
            <div class="budget-slider-range">
              <span>{{ currencySymbol }}0</span>
              <span>{{ currencySymbol }}{{ maxBudget.toLocaleString(undefined, { maximumFractionDigits: 0 }) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendations.title') }} ({{ filteredRecommendations.length }})</h3>
        </div>
        <div v-if="filteredRecommendations.length === 0" class="empty-state">
          {{ t('restocking.recommendations.noItems') }}
        </div>
        <div v-else class="table-container">
          <table>
            <thead>
              <tr>
                <th class="col-select">{{ t('restocking.recommendations.table.select') }}</th>
                <th>{{ t('restocking.recommendations.table.sku') }}</th>
                <th>{{ t('restocking.recommendations.table.itemName') }}</th>
                <th>{{ t('restocking.recommendations.table.currentDemand') }}</th>
                <th>{{ t('restocking.recommendations.table.forecastedDemand') }}</th>
                <th>{{ t('restocking.recommendations.table.unitCost') }}</th>
                <th>{{ t('restocking.recommendations.table.itemTotal') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredRecommendations" :key="item.sku">
                <td class="col-select">
                  <input
                    type="checkbox"
                    :checked="!!selectedMap[item.sku]"
                    @change="toggleSelection(item.sku)"
                  />
                </td>
                <td><strong>{{ item.sku }}</strong></td>
                <td>{{ translateProductName(item.item_name) }}</td>
                <td>{{ item.current_demand }}</td>
                <td><strong>{{ item.forecasted_demand }}</strong></td>
                <td>{{ currencySymbol }}{{ item.unit_cost.toFixed(2) }}</td>
                <td><strong>{{ currencySymbol }}{{ item.cost.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="card summary-card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.summary.title') }}</h3>
        </div>
        <div class="summary-grid">
          <div class="summary-item">
            <span class="summary-label">{{ t('restocking.summary.selectedItems') }}</span>
            <span class="summary-value">{{ selectedItemsList.length }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">{{ t('restocking.summary.totalCost') }}</span>
            <span class="summary-value">{{ currencySymbol }}{{ selectedItemsTotal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">{{ t('restocking.summary.remainingBudget') }}</span>
            <span class="summary-value" :class="{ negative: remainingBudget < 0 }">
              {{ currencySymbol }}{{ remainingBudget.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
            </span>
          </div>
        </div>

        <div v-if="successMessage" class="success-banner">{{ successMessage }}</div>
        <div v-if="placeError" class="error">{{ placeError }}</div>

        <button
          class="place-order-btn"
          :disabled="placing || selectedItemsList.length === 0"
          @click="placeOrder"
        >
          {{ placing ? t('restocking.placingOrder') : t('restocking.placeOrder') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, translateProductName } = useI18n()

    const currencySymbol = computed(() => {
      return currentCurrency.value === 'JPY' ? '¥' : '$'
    })

    const loading = ref(true)
    const error = ref(null)
    const placing = ref(false)
    const successMessage = ref(null)
    const placeError = ref(null)

    const inventoryItems = ref([])
    const demandForecasts = ref([])
    const budgetValue = ref(0)
    const selectedMap = ref({})

    // Use shared filters (restocking only supports warehouse/category, like inventory)
    const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()

    // Total value of current inventory on hand - defines the upper bound of the budget slider
    const maxBudget = computed(() => {
      return inventoryItems.value.reduce((sum, item) => sum + item.quantity_on_hand * item.unit_cost, 0)
    })

    // Match demand forecasts to inventory items by SKU to get unit cost,
    // then sort by forecasted_demand descending (highest priority items first)
    const combinedItems = computed(() => {
      const inventoryBySku = new Map(inventoryItems.value.map(item => [item.sku, item]))

      return demandForecasts.value
        .map(forecast => {
          const inventoryItem = inventoryBySku.get(forecast.item_sku)
          if (!inventoryItem) return null

          return {
            sku: forecast.item_sku,
            item_name: forecast.item_name,
            current_demand: forecast.current_demand,
            forecasted_demand: forecast.forecasted_demand,
            unit_cost: inventoryItem.unit_cost,
            cost: forecast.forecasted_demand * inventoryItem.unit_cost
          }
        })
        .filter(Boolean)
        .sort((a, b) => b.forecasted_demand - a.forecasted_demand)
    })

    // Greedily include items (highest demand first) while they still fit within budget
    const filteredRecommendations = computed(() => {
      let runningTotal = 0
      const result = []

      for (const item of combinedItems.value) {
        if (runningTotal + item.cost <= budgetValue.value) {
          result.push(item)
          runningTotal += item.cost
        }
      }

      return result
    })

    const selectedItemsList = computed(() => {
      return filteredRecommendations.value.filter(item => selectedMap.value[item.sku])
    })

    const selectedItemsTotal = computed(() => {
      return selectedItemsList.value.reduce((sum, item) => sum + item.cost, 0)
    })

    const remainingBudget = computed(() => budgetValue.value - selectedItemsTotal.value)

    const toggleSelection = (sku) => {
      selectedMap.value[sku] = !selectedMap.value[sku]
    }

    // Default to selecting every recommended item whenever the recommendation list changes
    watch(filteredRecommendations, (recs) => {
      const map = {}
      recs.forEach(item => {
        map[item.sku] = true
      })
      selectedMap.value = map
    })

    const loadData = async () => {
      try {
        loading.value = true
        error.value = null
        const filters = getCurrentFilters()

        // Restocking doesn't support month/status filters, only warehouse and category
        const [inventoryData, forecastData] = await Promise.all([
          api.getInventory({ warehouse: filters.warehouse, category: filters.category }),
          api.getDemandForecasts()
        ])

        inventoryItems.value = inventoryData
        demandForecasts.value = forecastData

        // Initialize the budget slider to half the available inventory value on first load
        if (budgetValue.value === 0) {
          budgetValue.value = Math.round(maxBudget.value / 2)
        }
      } catch (err) {
        error.value = 'Failed to load restocking data: ' + err.message
      } finally {
        loading.value = false
      }
    }

    // Watch for filter changes and reload data
    watch([selectedLocation, selectedCategory], () => {
      loadData()
    })

    const placeOrder = async () => {
      if (selectedItemsList.value.length === 0) {
        placeError.value = t('restocking.noSelection')
        return
      }

      placing.value = true
      placeError.value = null
      successMessage.value = null

      try {
        const payload = {
          items: selectedItemsList.value.map(item => ({
            item_sku: item.sku,
            item_name: item.item_name,
            quantity: item.forecasted_demand,
            unit_cost: item.unit_cost
          })),
          total_value: selectedItemsTotal.value
        }

        const order = await api.createRestockingOrder(payload)
        successMessage.value = t('restocking.orderSuccess', { orderNumber: order.order_number })

        // Reset the form after a successful submission
        budgetValue.value = 0
        selectedMap.value = {}
      } catch (err) {
        placeError.value = t('restocking.orderError') + ': ' + err.message
      } finally {
        placing.value = false
      }
    }

    onMounted(loadData)

    return {
      t,
      loading,
      error,
      placing,
      successMessage,
      placeError,
      budgetValue,
      selectedMap,
      maxBudget,
      filteredRecommendations,
      selectedItemsList,
      selectedItemsTotal,
      remainingBudget,
      toggleSelection,
      placeOrder,
      currencySymbol,
      translateProductName
    }
  }
}
</script>

<style scoped>
.budget-controls {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2rem;
}

.budget-stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.budget-stat-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.budget-stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
}

.budget-slider-group {
  flex: 1;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.budget-slider-label {
  font-size: 0.875rem;
  color: #334155;
}

.budget-slider-label strong {
  color: #0f172a;
}

.budget-slider {
  width: 100%;
  accent-color: #3b82f6;
  cursor: pointer;
}

.budget-slider-range {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #94a3b8;
}

.col-select {
  width: 70px;
  text-align: center;
}

.col-select input[type='checkbox'] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
  font-size: 0.938rem;
}

.summary-card {
  margin-bottom: 0;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.25rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.summary-value {
  font-size: 1.375rem;
  font-weight: 700;
  color: #0f172a;
}

.summary-value.negative {
  color: #dc2626;
}

.success-banner {
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.938rem;
}

.place-order-btn {
  padding: 0.75rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.place-order-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.place-order-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}
</style>

<template>
  <div class="restocking">
    <div class="page-header">
      <h2>Restocking</h2>
      <p>Get budget-based restocking recommendations and place orders</p>
    </div>

    <div class="card">
      <div class="card-header">
        <h3 class="card-title">Budget</h3>
      </div>
      <div class="budget-control">
        <input
          type="range"
          min="0"
          max="500000"
          step="1000"
          v-model.number="budget"
        >
        <span class="budget-value">Budget: {{ formatCurrency(budget) }}</span>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading recommendations...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

      <div v-if="recommendations.length === 0" class="card">
        <div class="empty-state">Enter a budget to get recommendations</div>
      </div>

      <div v-else class="card">
        <div class="card-header">
          <h3 class="card-title">Recommendations ({{ recommendations.length }})</h3>
        </div>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Name</th>
                <th>Category</th>
                <th>Warehouse</th>
                <th>Forecasted Demand</th>
                <th>Trend</th>
                <th>Recommended Qty</th>
                <th>Unit Cost</th>
                <th>Line Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="rec in recommendations" :key="rec.sku">
                <td><strong>{{ rec.sku }}</strong></td>
                <td>{{ rec.name }}</td>
                <td>{{ rec.category }}</td>
                <td>{{ rec.warehouse }}</td>
                <td>{{ rec.forecasted_demand }}</td>
                <td>
                  <span :class="['badge', getTrendClass(rec.trend)]">
                    {{ rec.trend }}
                  </span>
                </td>
                <td>{{ rec.recommended_quantity }}</td>
                <td>{{ formatCurrency(rec.unit_cost) }}</td>
                <td><strong>{{ formatCurrency(rec.line_total) }}</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="summary-line">
          Total: {{ formatCurrency(totalCost) }} / Budget: {{ formatCurrency(budget) }} / Remaining: {{ formatCurrency(remainingBudget) }}
        </div>

        <div class="order-action">
          <button
            class="place-order-btn"
            :disabled="recommendations.length === 0 || placingOrder"
            @click="placeOrder"
          >
            {{ placingOrder ? 'Placing Order...' : 'Place Order' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { api } from '../api'

export default {
  name: 'Restocking',
  setup() {
    const budget = ref(50000)
    const recommendations = ref([])
    const loading = ref(true)
    const error = ref(null)
    const placingOrder = ref(false)
    const successMessage = ref(null)

    let debounceTimer = null
    let successTimer = null

    const totalCost = computed(() => {
      return recommendations.value.reduce((sum, rec) => sum + rec.line_total, 0)
    })

    const remainingBudget = computed(() => {
      return budget.value - totalCost.value
    })

    const formatCurrency = (value) => {
      return '$' + Number(value || 0).toLocaleString('en-US', { maximumFractionDigits: 0 })
    }

    const getTrendClass = (trend) => {
      const trendMap = {
        increasing: 'success',
        stable: 'info',
        decreasing: 'warning'
      }
      return trendMap[trend] || 'info'
    }

    const loadRecommendations = async () => {
      try {
        loading.value = true
        error.value = null
        recommendations.value = await api.getRestockRecommendations(budget.value)
      } catch (err) {
        error.value = 'Failed to load restocking recommendations: ' + err.message
      } finally {
        loading.value = false
      }
    }

    const placeOrder = async () => {
      if (recommendations.value.length === 0) return
      try {
        placingOrder.value = true
        const items = recommendations.value.map(rec => ({
          sku: rec.sku,
          name: rec.name,
          quantity: rec.recommended_quantity,
          unit_price: rec.unit_cost
        }))

        await api.createRestockOrder({ items, budget: budget.value })

        successMessage.value = 'Order placed successfully!'
        recommendations.value = []

        if (successTimer) clearTimeout(successTimer)
        successTimer = setTimeout(() => {
          successMessage.value = null
        }, 2000)
      } catch (err) {
        error.value = 'Failed to place order: ' + err.message
      } finally {
        placingOrder.value = false
      }
    }

    // Debounce budget changes before refetching recommendations
    watch(budget, () => {
      if (debounceTimer) clearTimeout(debounceTimer)
      debounceTimer = setTimeout(() => {
        loadRecommendations()
      }, 300)
    })

    onMounted(() => {
      loadRecommendations()
    })

    onBeforeUnmount(() => {
      if (debounceTimer) clearTimeout(debounceTimer)
      if (successTimer) clearTimeout(successTimer)
    })

    return {
      budget,
      recommendations,
      loading,
      error,
      placingOrder,
      successMessage,
      totalCost,
      remainingBudget,
      formatCurrency,
      getTrendClass,
      placeOrder
    }
  }
}
</script>

<style scoped>
.budget-control {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.budget-control input[type="range"] {
  flex: 1;
  max-width: 400px;
}

.budget-value {
  font-size: 0.938rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-size: 0.938rem;
}

.summary-line {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  font-size: 0.938rem;
  font-weight: 600;
  color: #0f172a;
}

.order-action {
  margin-top: 1.25rem;
  display: flex;
  justify-content: flex-end;
}

.place-order-btn {
  padding: 0.625rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.place-order-btn:hover:not(:disabled) {
  background: #1d4ed8;
}

.place-order-btn:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.success-message {
  background: #d1fae5;
  border: 1px solid #a7f3d0;
  color: #065f46;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.938rem;
  font-weight: 500;
}
</style>

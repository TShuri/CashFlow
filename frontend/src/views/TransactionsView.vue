<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Движение денежных средств</h1>
      <router-link to="/create" class="btn btn-primary"> Добавить операцию </router-link>
    </div>

    <!-- Фильтры -->
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Фильтры</h5>
        <div class="row g-3">
          <!-- Период дат -->
          <div class="col-md-3">
            <label class="form-label">Дата с</label>
            <input
              v-model="filters.date_from"
              type="date"
              class="form-control"
              @change="applyFilters"
            />
          </div>
          <div class="col-md-3">
            <label class="form-label">Дата по</label>
            <input
              v-model="filters.date_to"
              type="date"
              class="form-control"
              @change="applyFilters"
            />
          </div>

          <!-- Статус -->
          <div class="col-md-2">
            <label class="form-label">Статус</label>
            <select v-model="filters.status" class="form-select" @change="applyFilters">
              <option value="">Все</option>
              <option v-for="status in statuses" :key="status.id" :value="status.id">
                {{ status.name }}
              </option>
            </select>
          </div>

          <!-- Тип -->
          <div class="col-md-2">
            <label class="form-label">Тип</label>
            <select v-model="filters.type" class="form-select" @change="applyFilters">
              <option value="">Все</option>
              <option v-for="type in types" :key="type.id" :value="type.id">
                {{ type.name }}
              </option>
            </select>
          </div>

          <!-- Категория -->
          <div class="col-md-2">
            <label class="form-label">Категория</label>
            <select v-model="filters.category" class="form-select" @change="applyFilters">
              <option value="">Все</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Подкатегория -->
          <div class="col-md-2">
            <label class="form-label">Подкатегория</label>
            <select v-model="filters.subcategory" class="form-select" @change="applyFilters">
              <option value="">Все</option>
              <option
                v-for="subcategory in subcategories"
                :key="subcategory.id"
                :value="subcategory.id"
              >
                {{ subcategory.name }}
              </option>
            </select>
          </div>

          <!-- Кнопка сброса -->
          <div class="col-md-2 d-flex align-items-end">
            <button @click="resetFilters" class="btn btn-outline-secondary w-100">Сбросить</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Таблица -->
    <div class="card">
      <div class="card-body">
        <div v-if="loading" class="text-center">
          <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-else-if="transactions.length === 0" class="text-center text-muted py-4">
          <div class="empty-state">
            <h5>{{ getEmptyStateTitle() }}</h5>
            <p>{{ getEmptyStateMessage() }}</p>
            <button v-if="hasActiveFilters()" @click="resetFilters" class="btn btn-primary mt-2">
              Сбросить фильтры
            </button>
            <router-link v-else to="/create" class="btn btn-primary mt-2">
              Добавить первую операцию
            </router-link>
          </div>
        </div>

        <table v-else class="table table-striped table-hover">
          <thead>
            <tr>
              <th>Дата</th>
              <th>Тип</th>
              <th>Категория</th>
              <th>Подкатегория</th>
              <th>Сумма</th>
              <th>Статус</th>
              <th>Комментарий</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="transaction in transactions" :key="transaction.id">
              <td>{{ formatDate(transaction.operation_date) }}</td>
              <td>
                <span :class="getTypeBadgeClass(transaction.type_name)">
                  {{ transaction.type_name }}
                </span>
              </td>
              <td>{{ transaction.category_name }}</td>
              <td>{{ transaction.subcategory_name }}</td>
              <td :class="getAmountClass(transaction.type_name)">
                {{ formatCurrency(transaction.amount) }}
              </td>
              <td>
                <span class="badge bg-secondary">{{ transaction.status_name }}</span>
              </td>
              <td>
                <span v-if="transaction.comment" class="comment-preview">
                  {{ truncateComment(transaction.comment) }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td>
                <router-link
                  :to="{ name: 'edit-transaction', params: { id: transaction.id } }"
                  class="btn btn-sm btn-outline-primary me-1"
                >
                  Редактировать
                </router-link>
                <button @click="openDeleteModal(transaction)" class="btn btn-sm btn-outline-danger">
                  Удалить
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления -->
    <ConfirmModal
      :show="showDeleteModal"
      title="Подтверждение удаления"
      :message="deleteMessage"
      :loading="deleteLoading"
      @confirm="handleDelete"
      @close="closeDeleteModal"
    />
  </div>
</template>

<script>
import { useTransactionsStore } from '@/stores/transactions'
import { mapState, mapActions } from 'pinia'
import ConfirmModal from '@/components/ConfirmModal.vue'

export default {
  name: 'TransactionsView',
  components: {
    ConfirmModal,
  },
  data() {
    return {
      filters: {
        date_from: '',
        date_to: '',
        status: '',
        type: '',
        category: '',
        subcategory: '',
      },
      filterTimeout: null,
      showDeleteModal: false,
      deleteLoading: false,
      transactionToDelete: null,
    }
  },
  computed: {
    ...mapState(useTransactionsStore, [
      'transactions',
      'statuses',
      'types',
      'categories',
      'subcategories',
      'loading',
      'error',
    ]),
    deleteMessage() {
      if (!this.transactionToDelete) return ''
      return `Вы уверены, что хотите удалить операцию от ${this.formatDate(this.transactionToDelete.operation_date)} на сумму ${this.formatCurrency(this.transactionToDelete.amount)}?`
    },
  },
  methods: {
    ...mapActions(useTransactionsStore, [
      'loadTransactions',
      'loadReferences',
      'deleteTransaction',
    ]),

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU')
    },

    formatCurrency(amount) {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
      }).format(amount)
    },

    getTypeBadgeClass(typeName) {
      return typeName === 'Пополнение' ? 'badge bg-success' : 'badge bg-danger'
    },

    getAmountClass(typeName) {
      return typeName === 'Пополнение' ? 'text-success fw-bold' : 'text-danger fw-bold'
    },

    truncateComment(comment) {
      return comment.length > 50 ? comment.substring(0, 50) + '...' : comment
    },

    // Открытие модального окна удаления
    openDeleteModal(transaction) {
      this.transactionToDelete = transaction
      this.showDeleteModal = true
    },

    // Закрытие модального окна
    closeDeleteModal() {
      this.showDeleteModal = false
      this.transactionToDelete = null
      this.deleteLoading = false
    },

    // Обработка удаления
    async handleDelete() {
      if (!this.transactionToDelete) return

      this.deleteLoading = true
      try {
        await this.deleteTransaction(this.transactionToDelete.id)
        await this.loadTransactions(this.filters)
        this.closeDeleteModal()
      } catch (error) {
        console.error('Error deleting transaction:', error)
        this.error = 'Ошибка при удалении: ' + (error.response?.data || error.message)
        this.closeDeleteModal()
      }
    },

    // Применение фильтров с дебаунсом
    applyFilters() {
      clearTimeout(this.filterTimeout)
      this.filterTimeout = setTimeout(() => {
        this.loadTransactions(this.filters)
      }, 300)
    },

    // Сброс фильтров
    resetFilters() {
      this.filters = {
        date_from: '',
        date_to: '',
        status: '',
        type: '',
        category: '',
        subcategory: '',
      }
      this.loadTransactions()
    },

    // Проверяем есть ли активные фильтры
    hasActiveFilters() {
      return Object.values(this.filters).some(
        (value) => value !== '' && value !== null && value !== undefined,
      )
    },

    // Заголовок для пустого состояния
    getEmptyStateTitle() {
      return this.hasActiveFilters() ? 'Нет транзакций по выбранным фильтрам' : 'Нет транзакций'
    },

    // Сообщение для пустого состояния
    getEmptyStateMessage() {
      if (this.hasActiveFilters()) {
        const activeFilters = []
        if (this.filters.date_from || this.filters.date_to) activeFilters.push('дате')
        if (this.filters.status) activeFilters.push('статусу')
        if (this.filters.type) activeFilters.push('типу')
        if (this.filters.category) activeFilters.push('категории')
        if (this.filters.subcategory) activeFilters.push('подкатегории')

        return `Попробуйте изменить фильтры по ${activeFilters.join(', ')}`
      }
      return 'Добавьте первую операцию в систему'
    },
  },

  async mounted() {
    await this.loadReferences()
    await this.loadTransactions()
  },
}
</script>

<style scoped>
.badge {
  font-size: 0.8em;
}

.table th {
  border-top: none;
  font-weight: 600;
}

.empty-state {
  padding: 2rem;
}

.empty-state h5 {
  color: #6c757d;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #868e96;
  margin-bottom: 1.5rem;
}
</style>

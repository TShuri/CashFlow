<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>{{ isEdit ? 'Редактирование операции' : 'Добавление операции' }}</h1>
      <router-link to="/" class="btn btn-outline-secondary"> ← Назад к списку </router-link>
    </div>

    <!-- Состояние загрузки при редактировании -->
    <div v-if="loadingData && isEdit" class="text-center py-5">
      <!-- ← loadingData -->
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Загрузка...</span>
      </div>
      <p class="mt-2 text-muted">Загрузка данных операции...</p>
    </div>

    <!-- Форма -->
    <div v-else class="card">
      <div class="card-body">
        <form @submit.prevent="submitForm">
          <div class="row g-3">
            <!-- Дата операции -->
            <div class="col-md-6">
              <label class="form-label">Дата операции *</label>
              <input
                v-model="form.operation_date"
                type="date"
                class="form-control"
                :class="{ 'is-invalid': errors.operation_date }"
                required
              />
              <div class="invalid-feedback">{{ errors.operation_date }}</div>
            </div>

            <!-- Статус -->
            <div class="col-md-6">
              <label class="form-label">Статус *</label>
              <select
                v-model="form.status"
                class="form-select"
                :class="{ 'is-invalid': errors.status }"
                required
              >
                <option value="">Выберите статус</option>
                <option v-for="status in statuses" :key="status.id" :value="status.id">
                  {{ status.name }}
                </option>
              </select>
              <div class="invalid-feedback">{{ errors.status }}</div>
            </div>

            <!-- Тип операции -->
            <div class="col-md-6">
              <label class="form-label">Тип операции *</label>
              <select
                v-model="form.type"
                class="form-select"
                :class="{ 'is-invalid': errors.type }"
                @change="onTypeChange"
                required
              >
                <option value="">Выберите тип</option>
                <option v-for="type in types" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
              <div class="invalid-feedback">{{ errors.type }}</div>
            </div>

            <!-- Категория -->
            <div class="col-md-6">
              <label class="form-label">Категория *</label>
              <select
                v-model="form.category"
                class="form-select"
                :class="{ 'is-invalid': errors.category }"
                @change="onCategoryChange"
                :disabled="!form.type"
                required
              >
                <option value="">Выберите категорию</option>
                <option
                  v-for="category in filteredCategories"
                  :key="category.id"
                  :value="category.id"
                >
                  {{ category.name }}
                </option>
              </select>
              <div class="invalid-feedback">{{ errors.category }}</div>
            </div>

            <!-- Подкатегория -->
            <div class="col-md-6">
              <label class="form-label">Подкатегория *</label>
              <select
                v-model="form.subcategory"
                class="form-select"
                :class="{ 'is-invalid': errors.subcategory }"
                :disabled="!form.category"
                required
              >
                <option value="">Выберите подкатегорию</option>
                <option
                  v-for="subcategory in filteredSubcategories"
                  :key="subcategory.id"
                  :value="subcategory.id"
                >
                  {{ subcategory.name }}
                </option>
              </select>
              <div class="invalid-feedback">{{ errors.subcategory }}</div>
            </div>

            <!-- Сумма -->
            <div class="col-md-6">
              <label class="form-label">Сумма (руб) *</label>
              <input
                v-model.number="form.amount"
                type="number"
                step="0.01"
                min="0.01"
                class="form-control"
                :class="{ 'is-invalid': errors.amount }"
                placeholder="0.00"
                required
              />
              <div class="invalid-feedback">{{ errors.amount }}</div>
            </div>

            <!-- Комментарий -->
            <div class="col-12">
              <label class="form-label">Комментарий</label>
              <textarea
                v-model="form.comment"
                class="form-control"
                rows="3"
                placeholder="Необязательный комментарий"
              ></textarea>
            </div>
          </div>

          <!-- Кнопки -->
          <div class="mt-4">
            <button type="submit" class="btn btn-primary me-2" :disabled="loading">
              {{ loading ? 'Сохранение...' : isEdit ? 'Обновить' : 'Создать' }}
            </button>
            <router-link to="/" class="btn btn-outline-secondary"> Отмена </router-link>
          </div>

          <!-- Ошибки -->
          <div v-if="serverError" class="alert alert-danger mt-3">
            {{ serverError }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useTransactionsStore } from '@/stores/transactions'
import { mapState, mapActions } from 'pinia'

export default {
  name: 'TransactionFormView',
  props: {
    id: String, // для редактирования
  },
  data() {
    return {
      form: {
        operation_date: this.getTodayDate(),
        status: '',
        type: '',
        category: '',
        subcategory: '',
        amount: '',
        comment: '',
      },
      errors: {},
      serverError: null,
      loading: false,
      loadingData: false,
    }
  },
  computed: {
    ...mapState(useTransactionsStore, ['statuses', 'types', 'categories', 'subcategories']),
    isEdit() {
      return !!this.id
    },
    filteredCategories() {
      if (!this.form.type) return []
      return this.categories.filter((cat) => cat.type == this.form.type)
    },
    filteredSubcategories() {
      if (!this.form.category) return []
      return this.subcategories.filter((sub) => sub.category == this.form.category)
    },
  },
  methods: {
    ...mapActions(useTransactionsStore, [
      'loadReferences',
      'loadCategories',
      'loadSubcategories',
      'createTransaction',
      'updateTransaction',
      'loadTransaction',
    ]),

    getTodayDate() {
      return new Date().toISOString().split('T')[0]
    },

    onTypeChange() {
      // Сбрасываем категорию и подкатегорию при смене типа
      this.form.category = ''
      this.form.subcategory = ''
      this.errors.category = ''
      this.errors.subcategory = ''

      if (this.form.type) {
        this.loadCategories(this.form.type)
      }
    },

    onCategoryChange() {
      // Сбрасываем подкатегорию при смене категории
      this.form.subcategory = ''
      this.errors.subcategory = ''

      if (this.form.category) {
        this.loadSubcategories(this.form.category)
      }
    },

    validateForm() {
      this.errors = {}

      if (!this.form.operation_date) {
        this.errors.operation_date = 'Дата операции обязательна'
      }
      if (!this.form.status) {
        this.errors.status = 'Статус обязателен'
      }
      if (!this.form.type) {
        this.errors.type = 'Тип операции обязателен'
      }
      if (!this.form.category) {
        this.errors.category = 'Категория обязательна'
      }
      if (!this.form.subcategory) {
        this.errors.subcategory = 'Подкатегория обязательна'
      }
      if (!this.form.amount || this.form.amount <= 0) {
        this.errors.amount = 'Сумма должна быть положительным числом'
      }

      return Object.keys(this.errors).length === 0
    },

    async submitForm() {
      if (!this.validateForm()) return

      this.loading = true
      this.serverError = null

      try {
        if (this.isEdit) {
          await this.updateTransaction(this.id, this.form)
        } else {
          await this.createTransaction(this.form)
        }
        this.$router.push('/')
      } catch (error) {
        if (error.response?.data) {
          // Обработка ошибок валидации с сервера
          const serverErrors = error.response.data
          for (const field in serverErrors) {
            this.errors[field] = serverErrors[field].join(', ')
          }
          this.serverError = 'Исправьте ошибки в форме'
        } else {
          this.serverError = 'Ошибка при сохранении: ' + error.message
        }
      } finally {
        this.loading = false
      }
    },

    // Загрузка существующей транзакции
    async loadTransactionData() {
      if (!this.isEdit) return

      this.loadingData = true
      try {
        const transaction = await this.loadTransaction(this.id)

        // Заполняем форму данными
        this.form = {
          operation_date: transaction.operation_date,
          status: transaction.status,
          type: transaction.type,
          category: transaction.category,
          subcategory: transaction.subcategory,
          amount: parseFloat(transaction.amount),
          comment: transaction.comment || '',
        }

        // Загружаем соответствующие категории и подкатегории
        if (transaction.type) {
          await this.loadCategories(transaction.type)
        }
        if (transaction.category) {
          await this.loadSubcategories(transaction.category)
        }
      } catch (error) {
        this.serverError = 'Ошибка при загрузке данных: ' + error.message
      } finally {
        this.loadingData = false
      }
    },
  },
  async mounted() {
    await this.loadReferences()

    if (this.isEdit) {
      await this.loadTransactionData()
    }
  },
}
</script>

<style scoped>
.form-select:disabled {
  background-color: #e9ecef;
  opacity: 1;
}
</style>

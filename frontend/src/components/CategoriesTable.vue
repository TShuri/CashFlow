<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>Категории</h5>
      <button class="btn btn-primary btn-sm" @click="showAddForm = true">Добавить категорию</button>
    </div>

    <!-- Сообщения об ошибках -->
    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''"></button>
    </div>

    <!-- Сообщения об успехе -->
    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''"></button>
    </div>

    <!-- Форма добавления категории -->
    <div v-if="showAddForm" class="card mb-3">
      <div class="card-body">
        <form @submit.prevent="addCategory">
          <div class="row g-2">
            <div class="col-md-4">
              <input
                v-model="newCategory.name"
                type="text"
                class="form-control"
                placeholder="Название категории"
                required
              />
            </div>
            <div class="col-md-4">
              <select v-model="newCategory.type" class="form-select" required>
                <option value="">Выберите тип</option>
                <option v-for="type in types" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
            </div>
            <div class="col-md-4">
              <button type="submit" class="btn btn-success btn-sm me-2">Добавить</button>
              <button type="button" class="btn btn-secondary btn-sm" @click="showAddForm = false">
                Отмена
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Таблица категорий -->
    <div class="card">
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <!-- <th>ID</th> -->
              <th>Название</th>
              <th>Тип операции</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in categories" :key="category.id">
              <!-- <td>{{ category.id }}</td> -->
              <td>
                <span v-if="!category.editing">{{ category.name }}</span>
                <input
                  v-else
                  v-model="category.editName"
                  type="text"
                  class="form-control form-control-sm"
                />
              </td>
              <td>
                <span v-if="!category.editing">{{ getTypeName(category.type) }}</span>
                <select v-else v-model="category.editType" class="form-select form-select-sm">
                  <option v-for="type in types" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </td>
              <td>
                <button
                  v-if="!category.editing"
                  @click="startEdit(category)"
                  class="btn btn-outline-primary btn-sm me-1"
                >
                  Редактировать
                </button>
                <button v-else @click="saveEdit(category)" class="btn btn-success btn-sm me-1">
                  Сохранить
                </button>
                <button
                  v-if="!category.editing"
                  @click="openDeleteModal(category)"
                  class="btn btn-outline-danger btn-sm"
                >
                  Удалить
                </button>
                <button v-else @click="cancelEdit(category)" class="btn btn-secondary btn-sm">
                  Отмена
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
      :warning-message="deleteWarning"
      :loading="deleteLoading"
      @confirm="handleDelete"
      @close="closeDeleteModal"
    />
  </div>
</template>

<script>
import { referencesAPI } from '@/services/api'
import ConfirmModal from '@/components/ConfirmModal.vue'

export default {
  name: 'CategoriesTable',
  components: {
    ConfirmModal,
  },
  data() {
    return {
      categories: [],
      types: [],
      showAddForm: false,
      newCategory: { name: '', type: '' },
      errorMessage: '',
      successMessage: '',
      showDeleteModal: false,
      deleteLoading: false,
      categoryToDelete: null,
    }
  },
  computed: {
    deleteMessage() {
      if (!this.categoryToDelete) return ''
      return `Вы уверены, что хотите удалить категорию "${this.categoryToDelete.name}"?`
    },
    deleteWarning() {
      return 'Внимание: это действие нельзя отменить.'
    },
  },
  methods: {
    async loadCategories() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getCategories()

        const categoriesData = response.data.results || response.data
        this.categories = Array.isArray(categoriesData)
          ? categoriesData.map((c) => ({
              ...c,
              editing: false,
              editName: c.name,
              editType: c.type,
            }))
          : []
      } catch (error) {
        console.error('Error loading categories:', error)
        this.showError('Не удалось загрузить список категорий')
      }
    },

    async loadTypes() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getTypes()

        const typesData = response.data.results || response.data
        this.types = Array.isArray(typesData) ? typesData : []
      } catch (error) {
        console.error('Error loading types:', error)
        this.showError('Не удалось загрузить список типов операций')
      }
    },

    getTypeName(typeId) {
      const type = this.types.find((t) => t.id === typeId)
      return type ? type.name : 'Неизвестный тип'
    },

    async addCategory() {
      try {
        this.errorMessage = ''
        await referencesAPI.createCategory(this.newCategory)
        this.newCategory = { name: '', type: '' }
        this.showAddForm = false
        this.showSuccess('Категория успешно добавлена')
        await this.loadCategories()
      } catch (error) {
        console.error('Error adding category:', error)
        this.showError('Не удалось добавить категорию')
      }
    },

    startEdit(category) {
      category.editing = true
      category.editName = category.name
      category.editType = category.type
    },

    async saveEdit(category) {
      try {
        this.errorMessage = ''
        await referencesAPI.updateCategory(category.id, {
          name: category.editName,
          type: category.editType,
        })
        category.name = category.editName
        category.type = category.editType
        category.editing = false
        this.showSuccess('Категория успешно обновлена')
      } catch (error) {
        console.error('Error updating category:', error)
        this.showError('Не удалось обновить категорию')
      }
    },

    cancelEdit(category) {
      category.editing = false
    },

    // Открытие модального окна удаления
    openDeleteModal(category) {
      this.categoryToDelete = category
      this.showDeleteModal = true
    },

    // Закрытие модального окна
    closeDeleteModal() {
      this.showDeleteModal = false
      this.categoryToDelete = null
      this.deleteLoading = false
    },

    // Обработка удаления
    async handleDelete() {
      if (!this.categoryToDelete) return

      this.deleteLoading = true
      try {
        await referencesAPI.deleteCategory(this.categoryToDelete.id)
        this.showSuccess('Категория успешно удалена')
        await this.loadCategories()
        this.closeDeleteModal()
      } catch (error) {
        console.error('Error deleting category:', error)

        // Проверяем код ошибки
        if (error.response && error.response.status === 500) {
          this.showError(
            'Не удается удалить категорию, так как есть записи транзакций с данной категорией',
          )
        } else {
          this.showError('Не удалось удалить категорию')
        }
        this.closeDeleteModal()
      }
    },

    showError(message) {
      this.errorMessage = message
      this.successMessage = ''
      // Автоматически скрывать ошибку через 5 секунд
      setTimeout(() => {
        if (this.errorMessage === message) {
          this.errorMessage = ''
        }
      }, 5000)
    },

    showSuccess(message) {
      this.successMessage = message
      this.errorMessage = ''
      // Автоматически скрывать успешное сообщение через 3 секунды
      setTimeout(() => {
        if (this.successMessage === message) {
          this.successMessage = ''
        }
      }, 3000)
    },
  },

  async mounted() {
    await this.loadTypes()
    await this.loadCategories()
  },
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>Подкатегории</h5>
      <button class="btn btn-primary btn-sm" @click="showAddForm = true">
        Добавить подкатегорию
      </button>
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

    <!-- Форма добавления подкатегории -->
    <div v-if="showAddForm" class="card mb-3">
      <div class="card-body">
        <form @submit.prevent="addSubcategory">
          <div class="row g-2">
            <div class="col-md-4">
              <input
                v-model="newSubcategory.name"
                type="text"
                class="form-control"
                placeholder="Название подкатегории"
                required
              />
            </div>
            <div class="col-md-4">
              <select v-model="newSubcategory.category" class="form-select" required>
                <option value="">Выберите категорию</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }} ({{ getTypeName(category.type) }})
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

    <!-- Таблица подкатегорий -->
    <div class="card">
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <!-- <th>ID</th> -->
              <th>Название</th>
              <th>Категория</th>
              <th>Тип операции</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="subcategory in subcategories" :key="subcategory.id">
              <!-- <td>{{ subcategory.id }}</td> -->
              <td>
                <span v-if="!subcategory.editing">{{ subcategory.name }}</span>
                <input
                  v-else
                  v-model="subcategory.editName"
                  type="text"
                  class="form-control form-control-sm"
                />
              </td>
              <td>
                <span v-if="!subcategory.editing">{{ getCategoryName(subcategory.category) }}</span>
                <select
                  v-else
                  v-model="subcategory.editCategory"
                  class="form-select form-select-sm"
                >
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }} ({{ getTypeName(category.type) }})
                  </option>
                </select>
              </td>
              <td>
                {{ getCategoryTypeName(subcategory.category) }}
              </td>
              <td>
                <button
                  v-if="!subcategory.editing"
                  @click="startEdit(subcategory)"
                  class="btn btn-outline-primary btn-sm me-1"
                >
                  Редактировать
                </button>
                <button v-else @click="saveEdit(subcategory)" class="btn btn-success btn-sm me-1">
                  Сохранить
                </button>
                <button
                  v-if="!subcategory.editing"
                  @click="openDeleteModal(subcategory)"
                  class="btn btn-outline-danger btn-sm"
                >
                  Удалить
                </button>
                <button v-else @click="cancelEdit(subcategory)" class="btn btn-secondary btn-sm">
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
  name: 'SubcategoriesTable',
  components: {
    ConfirmModal,
  },
  data() {
    return {
      subcategories: [],
      categories: [],
      types: [],
      showAddForm: false,
      newSubcategory: { name: '', category: '' },
      errorMessage: '',
      successMessage: '',
      showDeleteModal: false,
      deleteLoading: false,
      subcategoryToDelete: null,
    }
  },
  computed: {
    deleteMessage() {
      if (!this.subcategoryToDelete) return ''
      const categoryName = this.getCategoryName(this.subcategoryToDelete.category)
      return `Вы уверены, что хотите удалить подкатегорию "${this.subcategoryToDelete.name}" (категория: ${categoryName})?`
    },
    deleteWarning() {
      return 'Внимание: это действие нельзя отменить.'
    },
  },
  methods: {
    async loadSubcategories() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getSubcategories()

        const subcategoriesData = response.data.results || response.data
        this.subcategories = Array.isArray(subcategoriesData)
          ? subcategoriesData.map((s) => ({
              ...s,
              editing: false,
              editName: s.name,
              editCategory: s.category,
            }))
          : []
      } catch (error) {
        console.error('Error loading subcategories:', error)
        this.showError('Не удалось загрузить список подкатегорий')
      }
    },

    async loadCategories() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getCategories()

        const categoriesData = response.data.results || response.data
        this.categories = Array.isArray(categoriesData) ? categoriesData : []
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

    getCategoryName(categoryId) {
      const category = this.categories.find((c) => c.id === categoryId)
      return category ? category.name : 'Неизвестная категория'
    },

    getTypeName(typeId) {
      const type = this.types.find((t) => t.id === typeId)
      return type ? type.name : 'Неизвестный тип'
    },

    getCategoryTypeName(categoryId) {
      const category = this.categories.find((c) => c.id === categoryId)
      return category ? this.getTypeName(category.type) : 'Неизвестный тип'
    },

    async addSubcategory() {
      try {
        this.errorMessage = ''
        await referencesAPI.createSubcategory(this.newSubcategory)
        this.newSubcategory = { name: '', category: '' }
        this.showAddForm = false
        this.showSuccess('Подкатегория успешно добавлена')
        await this.loadSubcategories()
      } catch (error) {
        console.error('Error adding subcategory:', error)
        this.showError('Не удалось добавить подкатегорию')
      }
    },

    startEdit(subcategory) {
      subcategory.editing = true
      subcategory.editName = subcategory.name
      subcategory.editCategory = subcategory.category
    },

    async saveEdit(subcategory) {
      try {
        this.errorMessage = ''
        await referencesAPI.updateSubcategory(subcategory.id, {
          name: subcategory.editName,
          category: subcategory.editCategory,
        })
        subcategory.name = subcategory.editName
        subcategory.category = subcategory.editCategory
        subcategory.editing = false
        this.showSuccess('Подкатегория успешно обновлена')
      } catch (error) {
        console.error('Error updating subcategory:', error)
        this.showError('Не удалось обновить подкатегорию')
      }
    },

    cancelEdit(subcategory) {
      subcategory.editing = false
    },

    // Открытие модального окна удаления
    openDeleteModal(subcategory) {
      this.subcategoryToDelete = subcategory
      this.showDeleteModal = true
    },

    // Закрытие модального окна
    closeDeleteModal() {
      this.showDeleteModal = false
      this.subcategoryToDelete = null
      this.deleteLoading = false
    },

    // Обработка удаления
    async handleDelete() {
      if (!this.subcategoryToDelete) return

      this.deleteLoading = true
      try {
        await referencesAPI.deleteSubcategory(this.subcategoryToDelete.id)
        this.showSuccess('Подкатегория успешно удалена')
        await this.loadSubcategories()
        this.closeDeleteModal()
      } catch (error) {
        console.error('Error deleting subcategory:', error)

        // Проверяем код ошибки
        if (error.response && error.response.status === 500) {
          this.showError(
            'Не удается удалить подкатегорию, так как есть записи транзакций с данной подкатегорией',
          )
        } else {
          this.showError('Не удалось удалить подкатегорию')
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
    await this.loadSubcategories()
  },
}
</script>

<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>Типы операций</h5>
      <button class="btn btn-primary btn-sm" @click="showAddForm = true">Добавить тип</button>
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

    <!-- Форма добавления -->
    <div v-if="showAddForm" class="card mb-3">
      <div class="card-body">
        <form @submit.prevent="addType">
          <div class="row g-2">
            <div class="col-md-8">
              <input
                v-model="newType.name"
                type="text"
                class="form-control"
                placeholder="Название типа операции"
                required
              />
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

    <!-- Таблица типов -->
    <div class="card">
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <!-- <th>ID</th> -->
              <th>Название</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="type in types" :key="type.id">
              <!-- <td>{{ type.id }}</td> -->
              <td>
                <span v-if="!type.editing">{{ type.name }}</span>
                <input
                  v-else
                  v-model="type.editName"
                  type="text"
                  class="form-control form-control-sm"
                />
              </td>
              <td>
                <button
                  v-if="!type.editing"
                  @click="startEdit(type)"
                  class="btn btn-outline-primary btn-sm me-1"
                >
                  Редактировать
                </button>
                <button v-else @click="saveEdit(type)" class="btn btn-success btn-sm me-1">
                  Сохранить
                </button>
                <button
                  v-if="!type.editing"
                  @click="openDeleteModal(type)"
                  class="btn btn-outline-danger btn-sm"
                >
                  Удалить
                </button>
                <button v-else @click="cancelEdit(type)" class="btn btn-secondary btn-sm">
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
  name: 'TypesTable',
  components: {
    ConfirmModal,
  },
  data() {
    return {
      types: [],
      showAddForm: false,
      newType: { name: '' },
      errorMessage: '',
      successMessage: '',
      showDeleteModal: false,
      deleteLoading: false,
      typeToDelete: null,
    }
  },
  computed: {
    deleteMessage() {
      if (!this.typeToDelete) return ''
      return `Вы уверены, что хотите удалить тип операции "${this.typeToDelete.name}"?`
    },
    deleteWarning() {
      return 'Внимание: это действие нельзя отменить.'
    },
  },
  methods: {
    async loadTypes() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getTypes()

        const typesData = response.data.results || response.data
        this.types = Array.isArray(typesData)
          ? typesData.map((t) => ({ ...t, editing: false, editName: t.name }))
          : []
      } catch (error) {
        console.error('Error loading types:', error)
        this.showError('Не удалось загрузить список типов операций')
      }
    },

    async addType() {
      try {
        this.errorMessage = ''
        await referencesAPI.createType(this.newType)
        this.newType.name = ''
        this.showAddForm = false
        this.showSuccess('Тип операции успешно добавлен')
        await this.loadTypes()
      } catch (error) {
        console.error('Error adding type:', error)
        this.showError('Не удалось добавить тип операции')
      }
    },

    startEdit(type) {
      type.editing = true
      type.editName = type.name
    },

    async saveEdit(type) {
      try {
        this.errorMessage = ''
        await referencesAPI.updateType(type.id, { name: type.editName })
        type.name = type.editName
        type.editing = false
        this.showSuccess('Тип операции успешно обновлен')
      } catch (error) {
        console.error('Error updating type:', error)
        this.showError('Не удалось обновить тип операции')
      }
    },

    cancelEdit(type) {
      type.editing = false
    },

    // Открытие модального окна удаления
    openDeleteModal(type) {
      this.typeToDelete = type
      this.showDeleteModal = true
    },

    // Закрытие модального окна
    closeDeleteModal() {
      this.showDeleteModal = false
      this.typeToDelete = null
      this.deleteLoading = false
    },

    // Обработка удаления
    async handleDelete() {
      if (!this.typeToDelete) return

      this.deleteLoading = true
      try {
        await referencesAPI.deleteType(this.typeToDelete.id)
        this.showSuccess('Тип операции успешно удален')
        await this.loadTypes()
        this.closeDeleteModal()
      } catch (error) {
        console.error('Error deleting type:', error)

        // Проверяем код ошибки
        if (error.response && error.response.status === 500) {
          this.showError(
            'Не удается удалить тип операции, так как есть записи транзакций с данным типом',
          )
        } else {
          this.showError('Не удалось удалить тип операции')
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
  },
}
</script>

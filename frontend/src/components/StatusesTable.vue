<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h5>Статусы операций</h5>
      <button class="btn btn-primary btn-sm" @click="showAddForm = true">Добавить статус</button>
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
        <form @submit.prevent="addStatus">
          <div class="row g-2">
            <div class="col-md-8">
              <input
                v-model="newStatus.name"
                type="text"
                class="form-control"
                placeholder="Название статуса"
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

    <!-- Таблица статусов -->
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
            <tr v-for="status in statuses" :key="status.id">
              <!-- <td>{{ status.id }}</td> -->
              <td>
                <span v-if="!status.editing">{{ status.name }}</span>
                <input
                  v-else
                  v-model="status.editName"
                  type="text"
                  class="form-control form-control-sm"
                />
              </td>
              <td>
                <button
                  v-if="!status.editing"
                  @click="startEdit(status)"
                  class="btn btn-outline-primary btn-sm me-1"
                >
                  Редактировать
                </button>
                <button v-else @click="saveEdit(status)" class="btn btn-success btn-sm me-1">
                  Сохранить
                </button>
                <button
                  v-if="!status.editing"
                  @click="openDeleteModal(status)"
                  class="btn btn-outline-danger btn-sm"
                >
                  Удалить
                </button>
                <button v-else @click="cancelEdit(status)" class="btn btn-secondary btn-sm">
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
  name: 'StatusesTable',
  components: {
    ConfirmModal,
  },
  data() {
    return {
      statuses: [],
      showAddForm: false,
      newStatus: { name: '' },
      errorMessage: '',
      successMessage: '',
      showDeleteModal: false,
      deleteLoading: false,
      statusToDelete: null,
    }
  },
  computed: {
    deleteMessage() {
      if (!this.statusToDelete) return ''
      return `Вы уверены, что хотите удалить статус "${this.statusToDelete.name}"?`
    },
    deleteWarning() {
      return 'Внимание: это действие нельзя отменить.'
    },
  },
  methods: {
    async loadStatuses() {
      try {
        this.errorMessage = ''
        const response = await referencesAPI.getStatuses()
        const statusesData = response.data.results || response.data

        this.statuses = Array.isArray(statusesData)
          ? statusesData.map((s) => ({ ...s, editing: false, editName: s.name }))
          : []
      } catch (error) {
        console.error('Error loading statuses:', error)
        this.showError('Не удалось загрузить список статусов')
      }
    },

    async addStatus() {
      try {
        this.errorMessage = ''
        await referencesAPI.createStatus(this.newStatus)
        this.newStatus.name = ''
        this.showAddForm = false
        this.showSuccess('Статус успешно добавлен')
        await this.loadStatuses()
      } catch (error) {
        console.error('Error adding status:', error)
        this.showError('Не удалось добавить статус')
      }
    },

    startEdit(status) {
      status.editing = true
      status.editName = status.name
    },

    async saveEdit(status) {
      try {
        this.errorMessage = ''
        await referencesAPI.updateStatus(status.id, { name: status.editName })
        status.name = status.editName
        status.editing = false
        this.showSuccess('Статус успешно обновлен')
      } catch (error) {
        console.error('Error updating status:', error)
        this.showError('Не удалось обновить статус')
      }
    },

    cancelEdit(status) {
      status.editing = false
    },

    // Открытие модального окна удаления
    openDeleteModal(status) {
      this.statusToDelete = status
      this.showDeleteModal = true
    },

    // Закрытие модального окна
    closeDeleteModal() {
      this.showDeleteModal = false
      this.statusToDelete = null
      this.deleteLoading = false
    },

    // Обработка удаления
    async handleDelete() {
      if (!this.statusToDelete) return

      this.deleteLoading = true
      try {
        await referencesAPI.deleteStatus(this.statusToDelete.id)
        this.showSuccess('Статус успешно удален')
        await this.loadStatuses()
        this.closeDeleteModal()
      } catch (error) {
        console.error('Error deleting status:', error)

        // Проверяем код ошибки
        if (error.response && error.response.status === 500) {
          this.showError(
            'Не удается удалить статус, так как есть записи транзакций с данным статусом',
          )
        } else {
          this.showError('Не удалось удалить статус')
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
    await this.loadStatuses()
  },
}
</script>

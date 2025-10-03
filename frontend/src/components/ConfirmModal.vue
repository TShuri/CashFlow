<template>
  <div
    v-if="show"
    class="modal fade show d-block"
    tabindex="-1"
    role="dialog"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <p>{{ message }}</p>
          <div v-if="warningMessage" class="alert alert-warning mt-3">
            <small>{{ warningMessage }}</small>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="close">
            {{ cancelText }}
          </button>
          <button type="button" class="btn btn-danger" @click="confirm" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ confirmText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmModal',
  props: {
    show: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: 'Подтверждение удаления',
    },
    message: {
      type: String,
      required: true,
    },
    warningMessage: {
      type: String,
      default: '',
    },
    cancelText: {
      type: String,
      default: 'Отмена',
    },
    confirmText: {
      type: String,
      default: 'Удалить',
    },
    loading: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['confirm', 'close'],
  methods: {
    confirm() {
      this.$emit('confirm')
    },
    close() {
      this.$emit('close')
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        document.body.style.overflow = 'hidden'
      } else {
        document.body.style.overflow = ''
      }
    },
  },
}
</script>

<style scoped>
.modal {
  backdrop-filter: blur(2px);
}
</style>

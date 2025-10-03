import { defineStore } from 'pinia'
import { transactionsAPI, referencesAPI } from '@/services/api'

export const useTransactionsStore = defineStore('transactions', {
  state: () => ({
    transactions: [],
    statuses: [],
    types: [],
    categories: [],
    subcategories: [],
    loading: false,
    error: null,
  }),

  actions: {
    // Загрузка справочников
    async loadReferences() {
      try {
        const [statusesRes, typesRes, categoriesRes, subcategoriesRes] = await Promise.all([
          referencesAPI.getStatuses(),
          referencesAPI.getTypes(),
          referencesAPI.getCategories(),
          referencesAPI.getSubcategories(),
        ])
        this.statuses = statusesRes.data.results || statusesRes.data
        this.types = typesRes.data.results || typesRes.data
        this.categories = categoriesRes.data.results || categoriesRes.data
        this.subcategories = subcategoriesRes.data.results || subcategoriesRes.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Загрузка категорий по типу
    async loadCategories(typeId) {
      try {
        const response = await referencesAPI.getCategories(typeId)
        this.categories = response.data.results || response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Загрузка подкатегорий по категории
    async loadSubcategories(categoryId) {
      try {
        const response = await referencesAPI.getSubcategories(categoryId)
        this.subcategories = response.data.results || response.data
      } catch (error) {
        this.error = error.message
      }
    },

    // Загрузка транзакций
    async loadTransactions(params = {}) {
      this.loading = true
      try {
        // Очищаем пустые параметры
        const cleanParams = {}
        for (const key in params) {
          if (params[key] !== '' && params[key] !== null && params[key] !== undefined) {
            cleanParams[key] = params[key]
          }
        }

        const response = await transactionsAPI.getAll(cleanParams)
        this.transactions = response.data.results || response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    // Загрузка конкретной транзакции
    async loadTransaction(id) {
      try {
        const response = await transactionsAPI.getById(id)
        return response.data
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    // Создание транзакции
    async createTransaction(data) {
      try {
        await transactionsAPI.create(data)
        await this.loadTransactions() // Перезагружаем список
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    // Обновление транзакции
    async updateTransaction(id, data) {
      try {
        await transactionsAPI.update(id, data)
        await this.loadTransactions() // Перезагружаем список
      } catch (error) {
        this.error = error.message
        throw error
      }
    },

    // Удаление транзакции
    async deleteTransaction(id) {
      try {
        await transactionsAPI.delete(id)
        await this.loadTransactions() // Перезагружаем список
      } catch (error) {
        this.error = error.message
        throw error
      }
    },
  },

  getters: {
    // Можно добавить вычисляемые свойства
  },
})

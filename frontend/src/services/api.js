import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Сервисы для API endpoints
export const transactionsAPI = {
  // Транзакции
  getAll: (params = {}) => api.get('/transactions/', { params }),
  getById: (id) => api.get(`/transactions/${id}/`),
  create: (data) => api.post('/transactions/', data),
  update: (id, data) => api.put(`/transactions/${id}/`, data),
  delete: (id) => api.delete(`/transactions/${id}/`),
}

export const referencesAPI = {
  // Справочники
  getStatuses: () => api.get('/statuses/'),
  getTypes: () => api.get('/types/'),
  getCategories: (typeId) => api.get('/categories/', { params: { type: typeId } }),
  getSubcategories: (categoryId) =>
    api.get('/subcategories/', { params: { category: categoryId } }),
}

export default api

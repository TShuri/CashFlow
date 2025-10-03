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

  // CRUD методы
  createStatus: (data) => api.post('/statuses/', data),
  updateStatus: (id, data) => api.put(`/statuses/${id}/`, data),
  deleteStatus: (id) => api.delete(`/statuses/${id}/`),

  createType: (data) => api.post('/types/', data),
  updateType: (id, data) => api.put(`/types/${id}/`, data),
  deleteType: (id) => api.delete(`/types/${id}/`),

  createCategory: (data) => api.post('/categories/', data),
  updateCategory: (id, data) => api.put(`/categories/${id}/`, data),
  deleteCategory: (id) => api.delete(`/categories/${id}/`),

  createSubcategory: (data) => api.post('/subcategories/', data),
  updateSubcategory: (id, data) => api.put(`/subcategories/${id}/`, data),
  deleteSubcategory: (id) => api.delete(`/subcategories/${id}/`),
}

export default api

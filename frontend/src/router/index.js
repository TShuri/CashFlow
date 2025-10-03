import { createRouter, createWebHistory } from 'vue-router'
import TransactionsView from '@/views/TransactionsView.vue'
import TransactionFormView from '@/views/TransactionFormView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'transactions',
      component: TransactionsView,
    },
    {
      path: '/create',
      name: 'create-transaction',
      component: TransactionFormView,
    },
    {
      path: '/edit/:id',
      name: 'edit-transaction',
      component: TransactionFormView,
      props: true,
    },
    {
      path: '/references',
      name: 'references',
      component: () => import('@/views/ReferencesView.vue'),
    },
  ],
})

export default router

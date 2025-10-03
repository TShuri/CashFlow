<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1>Управление справочниками</h1>
    </div>

    <!-- Табы для разных справочников -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'statuses' }"
          @click="activeTab = 'statuses'"
          >Статусы</a
        >
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{ active: activeTab === 'types' }" @click="activeTab = 'types'"
          >Типы операций</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'categories' }"
          @click="activeTab = 'categories'"
          >Категории</a
        >
      </li>
      <li class="nav-item">
        <a
          class="nav-link"
          :class="{ active: activeTab === 'subcategories' }"
          @click="activeTab = 'subcategories'"
          >Подкатегории</a
        >
      </li>
    </ul>

    <!-- Компоненты для каждого справочника -->
    <StatusesTable v-if="activeTab === 'statuses'" />
    <TypesTable v-if="activeTab === 'types'" />
    <CategoriesTable v-if="activeTab === 'categories'" />
    <SubcategoriesTable v-if="activeTab === 'subcategories'" />
  </div>
</template>

<script>
import StatusesTable from '@/components/StatusesTable.vue'
import TypesTable from '@/components/TypesTable.vue'
import CategoriesTable from '@/components/CategoriesTable.vue'
import SubcategoriesTable from '@/components/SubcategoriesTable.vue'

export default {
  name: 'ReferencesView',
  components: {
    StatusesTable,
    TypesTable,
    CategoriesTable,
    SubcategoriesTable,
  },
  data() {
    return {
      activeTab: 'statuses',
    }
  },
}
</script>

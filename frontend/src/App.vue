<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand" href="#">CashFlow</a>
        <div class="navbar-nav">
          <router-link to="/" class="nav-link">Транзакции</router-link>
          <router-link to="/create" class="nav-link">Добавить</router-link>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

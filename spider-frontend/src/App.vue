<!-- src/App.vue -->
<script setup>
// 不再需要手动处理路由逻辑，router会自动处理
</script>

<template>
  <div id="app">
    <!-- router-view会根据路由自动渲染对应的组件 -->
    <router-view />
  </div>
</template>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
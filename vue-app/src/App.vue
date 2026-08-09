<script setup>
import { ref, provide } from 'vue'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import Workspace from './components/Workspace.vue'

const theme = ref('light')
const currentStep = ref(1)

const toggleTheme = () => {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme.value)
}

provide('theme', theme)
provide('currentStep', currentStep)
</script>

<template>
  <div class="app-layout">
    <Sidebar v-model:currentStep="currentStep" />
    <div class="main-content">
      <Header :theme="theme" @toggle-theme="toggleTheme" />
      <Workspace :currentStep="currentStep" />
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  background: var(--bg-primary);
}
</style>

<script setup>
defineProps({
  theme: String
})
const emit = defineEmits(['toggle-theme'])
</script>

<template>
  <header class="top-header">
    <div class="header-left">
      <span class="material-symbols-outlined" style="color: var(--text-secondary);">search</span>
      <input type="text" placeholder="Search data assets..." class="search-input" />
    </div>
    <div class="header-right">
      <button class="icon-btn" @click="emit('toggle-theme')">
        <span class="material-symbols-outlined">
          {{ theme === 'light' ? 'dark_mode' : 'light_mode' }}
        </span>
      </button>
      <div class="avatar">
        <span class="material-symbols-outlined">person</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.top-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 300px;
}

.search-input {
  border: none;
  background: transparent;
  outline: none;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 14px;
  width: 100%;
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icon-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--google-blue-alpha);
  color: var(--google-blue);
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<script setup>
defineProps({
  currentStep: Number
})
const emit = defineEmits(['update:currentStep'])

const steps = [
  { id: 1, name: 'Ingestion & Enrichment', icon: 'database' },
  { id: 2, name: 'Governance & Security', icon: 'shield' },
  { id: 3, name: 'Schema Discovery', icon: 'schema' },
  { id: 4, name: 'AI Data Modeling', icon: 'model_training' },
  { id: 5, name: 'Data Product Activation', icon: 'rocket_launch' }
]
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="brand">
        <span class="material-symbols-outlined icon-blue">deployed_code</span>
        <span class="brand-text">Data Fabric POC</span>
      </div>
    </div>
    <div class="sidebar-nav">
      <div class="section-header" style="padding: 0 16px;">Workflow Pipeline</div>
      <button 
        v-for="step in steps" 
        :key="step.id"
        class="nav-item"
        :class="{ active: currentStep === step.id }"
        @click="emit('update:currentStep', step.id)"
      >
        <span class="material-symbols-outlined" style="font-size: 18px;">{{ step.icon }}</span>
        <span>{{ step.id }}. {{ step.name }}</span>
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.icon-blue {
  color: var(--google-blue);
}

.sidebar-nav {
  padding: 24px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 16px;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 8px;
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-item:hover {
  background: var(--bg-primary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--google-blue-alpha);
  color: var(--google-blue);
  font-weight: 600;
}
</style>

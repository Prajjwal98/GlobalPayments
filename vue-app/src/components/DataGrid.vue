<script setup>
defineProps({
  columns: Array,
  data: Array,
  highlightCols: {
    type: Array,
    default: () => []
  }
})
</script>

<template>
  <div class="table-container card" style="padding: 0; overflow: hidden;">
    <table class="data-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, idx) in data" :key="idx" class="interactive-row">
          <td 
            v-for="col in columns" 
            :key="col"
            :class="{ highlight: highlightCols.includes(col) }"
          >
            {{ row[col] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th {
  text-align: left;
  padding: 12px 16px;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.data-table td {
  padding: 12px 16px;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.highlight {
  color: var(--google-blue);
  font-weight: 500;
  background: var(--google-blue-alpha);
}
</style>

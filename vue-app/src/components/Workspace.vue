<script setup>
import { ref, computed } from 'vue'
import DataGrid from './DataGrid.vue'

const props = defineProps({
  currentStep: Number
})

// MOCK DATA STATE
const rawData = [
  { TXN_ID: 'TXN-1528', USR_IDX: 'U-228', MERCH_CD: 'M-45', AMT_VAL: 11.95, TS_DT: '2023-10-01', CC_NUM: '4376-6305-6728-6674', USR_NM: 'John Doe' },
  { TXN_ID: 'TXN-3069', USR_IDX: 'U-412', MERCH_CD: 'M-87', AMT_VAL: 266.07, TS_DT: '2023-10-02', CC_NUM: '4161-6450-4703-3366', USR_NM: 'Jane Smith' },
  { TXN_ID: 'TXN-8067', USR_IDX: 'U-662', MERCH_CD: 'M-81', AMT_VAL: 306.16, TS_DT: '2023-10-03', CC_NUM: '4248-7029-9920-9714', USR_NM: 'Alice Jones' },
]

const rawColumns = ['TXN_ID', 'USR_IDX', 'MERCH_CD', 'AMT_VAL', 'TS_DT', 'CC_NUM', 'USR_NM']

const isEnriched = ref(false)
const isEnriching = ref(false)

const enrichedColumns = ['Transaction ID', 'User ID', 'Merchant Code', 'Amount ($)', 'Timestamp', 'Credit Card', 'Customer Name', 'Customer LTV ($)', 'Segment']
const enrichedData = computed(() => {
  if (!isEnriched.value) return []
  return rawData.map(row => ({
    'Transaction ID': row.TXN_ID,
    'User ID': row.USR_IDX,
    'Merchant Code': row.MERCH_CD,
    'Amount ($)': row.AMT_VAL,
    'Timestamp': row.TS_DT,
    'Credit Card': row.CC_NUM,
    'Customer Name': row.USR_NM,
    'Customer LTV ($)': (row.AMT_VAL * 2.1).toFixed(2),
    'Segment': row.AMT_VAL > 100 ? 'High Value' : 'Mid Value'
  }))
})

const triggerEnrichment = () => {
  isEnriching.value = true
  setTimeout(() => {
    isEnriched.value = true
    isEnriching.value = false
  }, 1500)
}
</script>

<template>
  <main class="workspace">
    <div class="step-container" v-if="currentStep === 1">
      <div class="workspace-header">
        <h2>Step 1: Data Ingestion & Enrichment</h2>
        <p style="color: var(--text-secondary); margin-top: 4px;">Transforming raw, undocumented operational data into understandable assets using Gemini LLM.</p>
      </div>

      <div class="split-view">
        <div class="split-pane">
          <div class="section-header">Raw Operational Data (Before)</div>
          <DataGrid :columns="rawColumns" :data="rawData" />
        </div>
        
        <div class="split-pane">
          <div class="section-header">AI Enriched Data (After)</div>
          
          <div v-if="!isEnriched" class="empty-state card">
            <span class="material-symbols-outlined" style="font-size: 32px; color: var(--google-blue); margin-bottom: 12px;">auto_awesome</span>
            <div style="margin-bottom: 16px; color: var(--text-secondary);">Awaiting AI enrichment...</div>
            <button class="btn btn-primary" @click="triggerEnrichment" :disabled="isEnriching">
              <span class="material-symbols-outlined" style="font-size: 18px;" v-if="!isEnriching">auto_awesome</span>
              <span class="material-symbols-outlined" style="font-size: 18px;" v-else>sync</span>
              {{ isEnriching ? 'Analyzing Schema...' : 'Suggest Derived Fields & Descriptions' }}
            </button>
          </div>
          
          <div v-else>
            <DataGrid :columns="enrichedColumns" :data="enrichedData" :highlightCols="['Customer LTV ($)', 'Segment']" />
            <div class="success-banner">
              <span class="material-symbols-outlined">check_circle</span>
              Metadata descriptions generated & derived fields added via Gemini API.
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="step-container" v-else>
      <div class="empty-state card" style="height: 400px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
        <span class="material-symbols-outlined" style="font-size: 48px; color: var(--text-secondary); margin-bottom: 16px;">construction</span>
        <h2>Step {{ currentStep }} Under Construction</h2>
        <p style="color: var(--text-secondary); margin-top: 8px;">(Only Step 1 is fully implemented for this Vue UI prototype)</p>
      </div>
    </div>

    <!-- Sliding Right Panel (Step 1) -->
    <transition name="slide">
      <div class="right-panel" v-if="currentStep === 1 && isEnriched">
        <div class="panel-header">
          <span class="material-symbols-outlined" style="color: var(--ai-purple);">auto_awesome</span>
          AI Metadata Dictionary
        </div>
        <div class="panel-content">
          <div class="meta-item">
            <div class="meta-title">Transaction ID</div>
            <div class="meta-desc">Unique identifier for the payment transaction.</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">User ID</div>
            <div class="meta-desc">Identifier mapping to the customer profile.</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">Merchant Code</div>
            <div class="meta-desc">Internal code for the acquiring merchant.</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">Amount ($)</div>
            <div class="meta-desc">Total fiat value of the transaction in USD.</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">Timestamp</div>
            <div class="meta-desc">Date and time the transaction was authorized.</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">Credit Card</div>
            <div class="meta-desc">Masked primary account number (PAN).</div>
          </div>
          <div class="meta-item">
            <div class="meta-title">Customer Name</div>
            <div class="meta-desc">Registered name of the cardholder.</div>
          </div>
          <div class="meta-item highlight-item">
            <div class="meta-title">
              Customer LTV ($)
              <span class="badge badge-purple" style="margin-left: 8px;">AI Derived</span>
            </div>
            <div class="meta-desc">Predictive metric for customer lifetime value based on spend history.</div>
          </div>
          <div class="meta-item highlight-item">
            <div class="meta-title">
              Segment
              <span class="badge badge-purple" style="margin-left: 8px;">AI Derived</span>
            </div>
            <div class="meta-desc">Categorical segmentation of the user for marketing targeting.</div>
          </div>
        </div>
      </div>
    </transition>
  </main>
</template>

<style scoped>
.workspace {
  flex: 1;
  padding: 32px 48px;
  overflow-y: auto;
  position: relative;
}

.step-container {
  max-width: 1200px;
  width: 100%;
}

.workspace-header {
  margin-bottom: 32px;
}

.split-view {
  display: flex;
  flex-direction: column;
  gap: 32px;
  /* Make room for the right panel if enriched */
  padding-right: v-bind('isEnriched && currentStep === 1 ? "400px" : "0"');
  transition: padding-right 0.3s ease;
}

.split-pane {
  flex: 1;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  text-align: center;
  border-style: dashed;
}

.success-banner {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(16, 185, 129, 0.1);
  color: var(--success-green);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 8px;
  font-weight: 500;
  font-size: 13px;
}

/* Sliding Right Panel */
.right-panel {
  position: absolute;
  top: 0;
  right: 0;
  width: 380px;
  height: 100%;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-left: 1px solid var(--border-color);
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  z-index: 10;
}

[data-theme='dark'] .right-panel {
  background: rgba(30, 41, 59, 0.7);
}

.panel-header {
  height: 64px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 24px;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-primary);
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
}

.meta-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.4;
}

.highlight-item {
  padding: 12px;
  background: var(--ai-purple-alpha);
  border-radius: 8px;
  border: 1px solid rgba(139, 92, 246, 0.1);
}

/* Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>

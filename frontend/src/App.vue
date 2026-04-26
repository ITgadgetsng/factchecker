<script setup lang="ts">
import { ref } from 'vue'

const question = ref('')
const result = ref('')
const resultType = ref('')
const loading = ref(false)
const submitted = ref(false)
const darkMode = ref(true)
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS

const examples = ["Is the sun a star?", "Is Nigeria in West Africa?", "Is Python a programming language?", "Is GenLayer an AI blockchain?"]

function fillQuestion(q: string) { question.value = q }
function toggleTheme() { darkMode.value = !darkMode.value }

async function checkFact() {
  loading.value = true
  submitted.value = false
  result.value = ''
  try {
    await fetch('https://studio.genlayer.com/api', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ jsonrpc: '2.0', method: 'eth_sendTransaction', params: [{ to: contractAddress, data: question.value }], id: 1 }) })
    submitted.value = true
  } catch (e) { console.error('FULL ERROR:', e); result.value = 'Submission failed.'; resultType.value = 'error' }
  loading.value = false
}

async function getResult() {
  loading.value = true
  try {
    const { createClient, createAccount } = await import('genlayer-js')
    const { studionet } = await import('genlayer-js/chains')
    const client = createClient({ chain: studionet, account: createAccount() })
    const answer = await client.readContract({ address: contractAddress, functionName: 'get_result', args: [] })
    result.value = answer ? '✅ TRUE' : '❌ FALSE'
    resultType.value = answer ? 'true' : 'false'
    submitted.value = false
  } catch (e) { console.error('FULL ERROR:', e); result.value = 'Could not get result yet.'; resultType.value = 'error' }
  loading.value = false
}
</script>

<template>
  <div class="page" :class="darkMode ? 'dark' : 'light'">
    <div class="card">
      <div class="top-bar">
        <div class="badge">🔗 Powered by GenLayer AI</div>
        <button class="theme-toggle" @click="toggleTheme">{{ darkMode ? '☀️ Light' : '🌙 Dark' }}</button>
      </div>
      <h1>🔍 AI Fact Checker</h1>
      <p class="subtitle">Ask any yes/no question and our decentralized AI will fact-check it on the blockchain</p>
      <div class="examples">
        <p class="examples-label">💡 Try these questions:</p>
        <div class="chips">
          <button v-for="q in examples" :key="q" class="chip" @click="fillQuestion(q)">{{ q }}</button>
        </div>
      </div>
      <input v-model="question" placeholder="e.g. Is the sun a star?" :disabled="loading" />
      <div class="buttons">
        <button class="btn-primary" @click="checkFact" :disabled="loading || !question">
          {{ loading ? '⏳ Processing...' : '🚀 Check Fact' }}
        </button>
        <button class="btn-secondary" @click="getResult" :disabled="loading">📊 Get Result</button>
      </div>
      <div v-if="submitted" class="submitted-msg">✅ Submitted! Wait 1-2 minutes then click <strong>Get Result</strong></div>
      <div v-if="result" class="result" :class="resultType">{{ result }}</div>
      <div class="footer">Built on <strong>GenLayer</strong> · Decentralized AI Consensus</div>
    </div>
  </div>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
.page { font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; transition: all 0.4s; }
.dark { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); }
.light { background: linear-gradient(135deg, #e0e7ff 0%, #f0f9ff 50%, #e8f5e9 100%); }
.card { border-radius: 24px; padding: 40px; max-width: 560px; width: 100%; text-align: center; transition: all 0.4s; }
.dark .card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 25px 50px rgba(0,0,0,0.4); }
.light .card { background: rgba(255,255,255,0.9); border: 1px solid rgba(0,0,0,0.08); box-shadow: 0 25px 50px rgba(0,0,0,0.1); }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.badge { background: rgba(79,70,229,0.3); border: 1px solid rgba(79,70,229,0.5); color: #a5b4fc; padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.theme-toggle { background: rgba(79,70,229,0.15); border: 1px solid rgba(79,70,229,0.3); color: #a5b4fc; padding: 6px 16px; border-radius: 20px; font-size: 12px; cursor: pointer; }
.light .theme-toggle { color: #4f46e5; }
h1 { font-size: 2rem; font-weight: 800; margin-bottom: 12px; }
.dark h1 { color: #fff; }
.light h1 { color: #1e1b4b; }
.subtitle { font-size: 14px; line-height: 1.6; margin-bottom: 20px; }
.dark .subtitle { color: #94a3b8; }
.light .subtitle { color: #475569; }
.examples { margin-bottom: 20px; text-align: left; }
.examples-label { font-size: 13px; color: #64748b; margin-bottom: 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { background: rgba(79,70,229,0.1); border: 1px solid rgba(79,70,229,0.3); color: #a5b4fc; padding: 6px 14px; border-radius: 20px; font-size: 12px; cursor: pointer; }
.light .chip { color: #4f46e5; }
.chip:hover { background: rgba(79,70,229,0.25); }
input { width: 100%; padding: 16px; border-radius: 12px; font-size: 16px; outline: none; margin-bottom: 16px; transition: all 0.3s; }
.dark input { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; }
.light input { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }
input::placeholder { color: #64748b; }
input:focus { border-color: #4f46e5; }
.buttons { display: flex; gap: 12px; margin-bottom: 16px; }
.btn-primary { flex: 1; padding: 16px; background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border: none; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(79,70,229,0.4); }
.btn-secondary { flex: 1; padding: 16px; background: rgba(5,150,105,0.2); color: #34d399; border: 1px solid rgba(5,150,105,0.4); border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-secondary:hover:not(:disabled) { transform: translateY(-2px); }
button:disabled { opacity: 0.5; cursor: not-allowed; transform: none !important; }
.submitted-msg { background: rgba(79,70,229,0.15); border: 1px solid rgba(79,70,229,0.3); color: #a5b4fc; padding: 16px; border-radius: 12px; font-size: 14px; margin-bottom: 16px; }
.result { padding: 24px; border-radius: 12px; font-size: 28px; font-weight: 800; margin-bottom: 16px; }
.result.true { background: rgba(5,150,105,0.15); border: 1px solid rgba(5,150,105,0.3); color: #34d399; }
.result.false { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3); color: #f87171; }
.result.error { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: #fbbf24; }
.footer { font-size: 13px; margin-top: 8px; }
.dark .footer { color: #475569; }
.light .footer { color: #94a3b8; }
</style>
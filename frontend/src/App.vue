<script setup lang="ts">
import { ref } from 'vue'

const question = ref('')
const result = ref('')
const resultType = ref('')
const loading = ref(false)
const submitted = ref(false)
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS

async function checkFact() {
  loading.value = true
  submitted.value = false
  result.value = ''
  try {
    const response = await fetch('https://studio.genlayer.com/api', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        jsonrpc: '2.0',
        method: 'eth_sendTransaction',
        params: [{ to: contractAddress, data: question.value }],
        id: 1
      })
    })
    console.log('submitted', await response.json())
    submitted.value = true
  } catch (e) {
    console.error('FULL ERROR:', e)
    result.value = 'Submission failed. Try again.'
    resultType.value = 'error'
  }
  loading.value = false
}

async function getResult() {
  loading.value = true
  try {
    const { createClient, createAccount } = await import('genlayer-js')
    const { studionet } = await import('genlayer-js/chains')
    const account = createAccount()
    const client = createClient({ chain: studionet, account })
    const answer = await client.readContract({
      address: contractAddress,
      functionName: 'get_result',
      args: []
    })
    result.value = answer ? '✅ TRUE' : '❌ FALSE'
    resultType.value = answer ? 'true' : 'false'
    submitted.value = false
  } catch (e) {
    console.error('FULL ERROR:', e)
    result.value = 'Could not get result yet. Try again.'
    resultType.value = 'error'
  }
  loading.value = false
}
</script>

<template>
  <div class="page">
    <div class="card">
      <div class="badge">🔗 Powered by GenLayer AI</div>
      <h1>🔍 AI Fact Checker</h1>
      <p class="subtitle">Ask any yes/no question and our decentralized AI will fact-check it on the blockchain</p>

      <div class="input-group">
        <input
          v-model="question"
          placeholder="e.g. Is the sun a star?"
          :disabled="loading"
        />
      </div>

      <div class="buttons">
        <button class="btn-primary" @click="checkFact" :disabled="loading || !question">
          <span v-if="loading">⏳ Processing...</span>
          <span v-else>🚀 Check Fact</span>
        </button>
        <button class="btn-secondary" @click="getResult" :disabled="loading">
          <span>📊 Get Result</span>
        </button>
      </div>

      <div v-if="submitted" class="submitted-msg">
        ✅ Question submitted to blockchain! Wait 1-2 minutes then click <strong>Get Result</strong>
      </div>

      <div v-if="result" class="result" :class="resultType">
        {{ result }}
      </div>

      <div class="footer">
        Built on <strong>GenLayer</strong> · Decentralized AI Consensus
      </div>
    </div>
  </div>
</template>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Segoe UI', Arial, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.page {
  width: 100%;
  display: flex;
  justify-content: center;
}

.card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 48px 40px;
  max-width: 520px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.badge {
  display: inline-block;
  background: rgba(79, 70, 229, 0.3);
  border: 1px solid rgba(79, 70, 229, 0.5);
  color: #a5b4fc;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-bottom: 20px;
}

h1 {
  color: #ffffff;
  font-size: 2.2rem;
  font-weight: 800;
  margin-bottom: 12px;
}

.subtitle {
  color: #94a3b8;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 32px;
}

.input-group {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  color: #ffffff;
  font-size: 16px;
  outline: none;
  transition: all 0.3s;
}

input::placeholder { color: #64748b; }
input:focus { border-color: #4f46e5; background: rgba(255,255,255,0.12); }
input:disabled { opacity: 0.5; }

.buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.btn-primary {
  flex: 1;
  padding: 16px;
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
}

.btn-secondary {
  flex: 1;
  padding: 16px;
  background: rgba(5, 150, 105, 0.2);
  color: #34d399;
  border: 1px solid rgba(5, 150, 105, 0.4);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-secondary:hover:not(:disabled) {
  transform: translateY(-2px);
  background: rgba(5, 150, 105, 0.3);
}

button:disabled { opacity: 0.5; cursor: not-allowed; transform: none !important; }

.submitted-msg {
  background: rgba(79, 70, 229, 0.15);
  border: 1px solid rgba(79, 70, 229, 0.3);
  color: #a5b4fc;
  padding: 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.result {
  padding: 24px;
  border-radius: 12px;
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 24px;
}

.result.true {
  background: rgba(5, 150, 105, 0.15);
  border: 1px solid rgba(5, 150, 105, 0.3);
  color: #34d399;
}

.result.false {
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.result.error {
  background: rgba(245, 158, 11, 0.15);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #fbbf24;
}

.footer {
  color: #475569;
  font-size: 13px;
  margin-top: 8px;
}
</style>
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
    <div class="bg-geo"></div>
    <div class="bg-blur"></div>
    <div class="card glass animate-in">
      <div class="top-bar">
        <div class="badge">
          <img src="/src/assets/logo.png" alt="GenLayer" class="badge-img" />
          <span>GenLayer AI</span>
        </div>
        <button class="theme-toggle" @click="toggleTheme">
          <span class="toggle-track">
            <span class="toggle-thumb" :class="{ on: !darkMode }"></span>
          </span>
          <span class="toggle-label">{{ darkMode ? 'Night' : 'Day' }}</span>
        </button>
      </div>
      <h1 class="fancy-title animate-title">AI Fact Checker</h1>
      <p class="subtitle animate-sub">Ask any yes/no question and our decentralized AI will fact-check it on the blockchain</p>
      <div class="examples animate-ex">
        <p class="examples-label">💡 Try these questions:</p>
        <div class="chips">
          <button v-for="q in examples" :key="q" class="chip" @click="fillQuestion(q)">{{ q }}</button>
        </div>
      </div>
      <input v-model="question" class="animate-input" placeholder="e.g. Is the sun a star?" :disabled="loading" />
      <div class="buttons animate-btns">
        <button class="btn-primary" @click="checkFact" :disabled="loading || !question">
          <span v-if="loading" class="loader"></span>
          <span v-else>Check Fact</span>
        </button>
        <button class="btn-secondary" @click="getResult" :disabled="loading">Get Result</button>
      </div>
      <transition name="pop">
        <div v-if="submitted" class="submitted-msg">✅ Submitted! Wait 1-2 minutes then click <strong>Get Result</strong></div>
      </transition>
      <transition name="pop">
        <div v-if="result" class="result" :class="resultType">{{ result }}</div>
      </transition>
      <div class="footer animate-footer">Built on <strong>GenLayer</strong> · Decentralized AI Consensus</div>
    </div>
  </div>
</template>


<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@700&family=Spectral:wght@400;700&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
.page {
  font-family: 'Spectral', serif;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  transition: background 0.6s cubic-bezier(.77,0,.18,1);
}
.dark {
  background: radial-gradient(ellipse at 60% 40%, #0f2027 0%, #2c5364 100%);
}
.light {
  background: radial-gradient(ellipse at 40% 60%, #fffbe6 0%, #f7e9d7 100%);
}
.bg-geo {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background: url('data:image/svg+xml;utf8,<svg width="100%25" height="100%25" xmlns="http://www.w3.org/2000/svg"><rect fill="none"/><g stroke="%23e0e7ff" stroke-width="1.5" opacity="0.08"><circle cx="50%25" cy="50%25" r="40%25"/><circle cx="50%25" cy="50%25" r="30%25"/><circle cx="50%25" cy="50%25" r="20%25"/></g></svg>') center/cover no-repeat;
}
.bg-blur {
  position: absolute;
  top: 10%; left: 60%; width: 420px; height: 420px;
  background: linear-gradient(135deg, #ffb347 0%, #00ffb8 100%);
  filter: blur(120px) saturate(1.5);
  opacity: 0.18;
  border-radius: 50%;
  z-index: 1;
  pointer-events: none;
  animation: float 8s ease-in-out infinite alternate;
}
@keyframes float {
  0% { transform: translateY(0) scale(1); }
  100% { transform: translateY(-40px) scale(1.1); }
}
.card {
  border-radius: 32px;
  padding: 48px 40px 36px 40px;
  max-width: 540px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 2;
  box-shadow: 0 12px 48px 0 rgba(0,0,0,0.18);
  margin: 0 auto;
  transition: box-shadow 0.4s, background 0.4s;
}
.glass {
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(18px) saturate(1.2);
  border: 1.5px solid rgba(255,255,255,0.22);
}
.dark .glass {
  background: rgba(24,28,38,0.55);
  border: 1.5px solid rgba(255,255,255,0.08);
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}
.badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(0,0,0,0.08);
  border-radius: 18px;
  padding: 5px 18px 5px 8px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  color: #ffb347;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.04);
}
.badge-img {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #fffbe6;
  box-shadow: 0 2px 8px 0 rgba(255,179,71,0.12);
  object-fit: cover;
  object-position: center;
  padding: 2px;
}
.theme-toggle {
  background: none;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  outline: none;
}
.toggle-track {
  width: 38px;
  height: 22px;
  background: #e0e7ff;
  border-radius: 12px;
  position: relative;
  transition: background 0.3s;
  display: flex;
  align-items: center;
}
.dark .toggle-track {
  background: #2c5364;
}
.toggle-thumb {
  width: 18px;
  height: 18px;
  background: #ffb347;
  border-radius: 50%;
  position: absolute;
  left: 2px;
  top: 2px;
  transition: left 0.3s cubic-bezier(.77,0,.18,1), background 0.3s;
  box-shadow: 0 2px 8px 0 rgba(255,179,71,0.18);
}
.toggle-thumb.on {
  left: 18px;
  background: #00ffb8;
}
.toggle-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 13px;
  color: #2c5364;
  font-weight: 700;
}
.dark .toggle-label {
  color: #ffb347;
}
.fancy-title {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -1.5px;
  margin-bottom: 10px;
  color: #2c5364;
  text-shadow: 0 2px 12px #ffb34733;
}
.dark .fancy-title {
  color: #ffb347;
  text-shadow: 0 2px 12px #2c536433;
}
.subtitle {
  font-size: 16px;
  line-height: 1.7;
  margin-bottom: 22px;
  color: #2c5364;
}
.dark .subtitle {
  color: #e0e7ff;
}
.examples {
  margin-bottom: 18px;
  text-align: left;
}
.examples-label {
  font-size: 13px;
  color: #00ffb8;
  margin-bottom: 8px;
  font-family: 'IBM Plex Mono', monospace;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.chip {
  background: linear-gradient(90deg, #ffb347 0%, #00ffb8 100%);
  color: #2c5364;
  padding: 7px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 700;
  border: none;
  cursor: pointer;
  transition: filter 0.2s, transform 0.2s;
  box-shadow: 0 2px 8px 0 #ffb34722;
}
.chip:hover {
  filter: brightness(1.1) saturate(1.2);
  transform: scale(1.07);
}
input {
  width: 100%;
  padding: 18px;
  border-radius: 14px;
  font-size: 17px;
  outline: none;
  margin-bottom: 18px;
  border: 1.5px solid #e0e7ff;
  background: rgba(255,255,255,0.7);
  color: #2c5364;
  font-family: 'Spectral', serif;
  transition: border-color 0.3s, background 0.3s;
}
.dark input {
  background: rgba(44,83,100,0.18);
  border: 1.5px solid #ffb347;
  color: #ffb347;
}
input::placeholder {
  color: #b0b8d1;
}
input:focus {
  border-color: #00ffb8;
  background: #fffbe6;
}
.dark input:focus {
  background: #2c5364;
}
.buttons {
  display: flex;
  gap: 14px;
  margin-bottom: 18px;
}
.btn-primary {
  flex: 1;
  padding: 16px;
  background: linear-gradient(90deg, #ffb347 0%, #00ffb8 100%);
  color: #2c5364;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 700;
  cursor: pointer;
  transition: filter 0.2s, transform 0.2s;
  box-shadow: 0 2px 12px 0 #ffb34722;
  position: relative;
  overflow: hidden;
}
.btn-primary:hover:not(:disabled) {
  filter: brightness(1.1) saturate(1.2);
  transform: scale(1.04);
}
.btn-secondary {
  flex: 1;
  padding: 16px;
  background: linear-gradient(90deg, #2c5364 0%, #00ffb8 100%);
  color: #fffbe6;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 700;
  cursor: pointer;
  transition: filter 0.2s, transform 0.2s;
  box-shadow: 0 2px 12px 0 #00ffb822;
}
.btn-secondary:hover:not(:disabled) {
  filter: brightness(1.1) saturate(1.2);
  transform: scale(1.04);
}
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}
.loader {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid #fffbe6;
  border-top: 3px solid #ffb347;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.submitted-msg {
  background: rgba(0,255,184,0.08);
  border: 1.5px solid #00ffb8;
  color: #00ffb8;
  padding: 16px;
  border-radius: 14px;
  font-size: 15px;
  margin-bottom: 16px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 700;
  letter-spacing: 0.2px;
}
.result {
  padding: 26px;
  border-radius: 14px;
  font-size: 30px;
  font-family: 'IBM Plex Mono', monospace;
  font-weight: 800;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px 0 #00ffb822;
  animation: pop-in 0.5s cubic-bezier(.77,0,.18,1);
}
.result.true {
  background: rgba(0,255,184,0.13);
  border: 1.5px solid #00ffb8;
  color: #00ffb8;
}
.result.false {
  background: rgba(255,71,71,0.13);
  border: 1.5px solid #ff4747;
  color: #ff4747;
}
.result.error {
  background: rgba(255,179,71,0.13);
  border: 1.5px solid #ffb347;
  color: #ffb347;
}
@keyframes pop-in {
  0% { transform: scale(0.7); opacity: 0; }
  80% { transform: scale(1.1); opacity: 1; }
  100% { transform: scale(1); }
}
.footer {
  font-size: 13px;
  margin-top: 10px;
  color: #2c5364;
  font-family: 'IBM Plex Mono', monospace;
  opacity: 0.7;
}
.dark .footer {
  color: #ffb347;
  opacity: 0.7;
}
/* Animations for orchestrated entrance */
.animate-in { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.1s both; }
.animate-title { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.2s both; }
.animate-sub { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.3s both; }
.animate-ex { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.4s both; }
.animate-input { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.5s both; }
.animate-btns { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.6s both; }
.animate-footer { animation: fade-in-up 1.1s cubic-bezier(.77,0,.18,1) 0.7s both; }
@keyframes fade-in-up {
  0% { opacity: 0; transform: translateY(40px); }
  100% { opacity: 1; transform: translateY(0); }
}
.pop-enter-active, .pop-leave-active {
  transition: all 0.4s cubic-bezier(.77,0,.18,1);
}
.pop-enter-from, .pop-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
.pop-enter-to, .pop-leave-from {
  opacity: 1;
  transform: scale(1);
}
@media (max-width: 700px) {
  .card {
    padding: 24px 8px 18px 8px;
    max-width: 98vw;
  }
  .fancy-title {
    font-size: 1.5rem;
  }
}
</style>
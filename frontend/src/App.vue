<script setup lang="ts">
import { ref } from 'vue'

const question = ref('')
const result = ref('')
const loading = ref(false)
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS

async function checkFact() {
  loading.value = true
  result.value = ''
  try {
    const { createClient, createAccount } = await import('genlayer-js')
    const { studionet } = await import('genlayer-js/chains')
    const account = createAccount()
    const client = createClient({ chain: studionet, account })
    
    await client.writeContract({
      address: contractAddress,
      functionName: 'check_fact',
      args: [question.value],
      value: 0n,
      awaited: false
    })

    result.value = '⏳ Question submitted! Check back in a minute...'
  } catch (e) {
    console.error('FULL ERROR:', e)
    result.value = 'Something went wrong. Try again.'
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
  } catch (e) {
    console.error('FULL ERROR:', e)
    result.value = 'Something went wrong.'
  }
  loading.value = false
}
</script>

<template>
  <div class="container">
    <h1>🔍 Fact Checker</h1>
    <p>Ask any yes/no question and AI will fact-check it</p>
    <input v-model="question" placeholder="e.g. Is the sun a star?" />
    <button @click="checkFact" :disabled="loading">
      {{ loading ? 'Checking...' : 'Check Fact' }}
    </button>
    <button @click="getResult" :disabled="loading" style="margin-left: 10px; background: #059669">
      Get Result
    </button>
    <div v-if="result" class="result">{{ result }}</div>
  </div>
</template>

<style>
body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; justify-content: center; padding: 50px; }
.container { background: white; padding: 40px; border-radius: 12px; max-width: 500px; width: 100%; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
h1 { color: #333; }
input { width: 100%; padding: 12px; margin: 20px 0 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; box-sizing: border-box; }
button { background: #4f46e5; color: white; border: none; padding: 12px 30px; border-radius: 8px; font-size: 16px; cursor: pointer; }
button:disabled { background: #999; }
.result { margin-top: 20px; font-size: 24px; font-weight: bold; }
</style>
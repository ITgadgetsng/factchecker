<script setup lang="ts">
import { ref } from 'vue'

const question = ref('')
const result = ref('')
const resultType = ref('')
const loading = ref(false)
const submitted = ref(false)
const darkMode = ref(true)
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS

const examples = [
  "Is the sun a star?",
  "Is Nigeria in West Africa?",
  "Is Python a programming language?",
  "Is water made of hydrogen and oxygen?",
  "Is GenLayer an AI blockchain?"
]

function fillQuestion(q: string) {
  question.value = q
}

function toggleTheme() {
  darkMode.value = !darkMode.value
}

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
  <div class="page" :class="darkMode ? 'dark' : 'light'">
    <div class="card">

      <div class="top-bar">
        <div class="
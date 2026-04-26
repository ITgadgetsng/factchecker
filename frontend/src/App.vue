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
      value: 0n
    })

    // Wait 30 seconds then read result
    await new Promise(resolve => setTimeout(resolve, 30000))
    
    const answer = await client.readContract({
      address: contractAddress,
      functionName: 'get_result',
      args: []
    })
    result.value = answer ? '✅ TRUE' : '❌ FALSE'
  } catch (e) {
    console.error('FULL ERROR:', e)
    result.value = 'Something went wrong. Try again.'
  }
  loading.value = false
}
</script>
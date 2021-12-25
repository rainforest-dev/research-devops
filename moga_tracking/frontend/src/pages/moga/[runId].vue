<template lang="pug">
div {{ volumeFractionLower }} - {{ volumeFractionUpper }}
</template>
<script setup lang="ts">
import { getRunInfo } from '@/utils/api';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
const route = useRoute()
const runId = Array.isArray(route.params.runId) ? route.params.runId[0] : route.params.runId
const volumeFractionUpper = ref<number>()
const volumeFractionLower = ref<number>()
onMounted(async () => {
  const volumeFraction = parseFloat(await getRunInfo(runId, 'volume_fraction'))
  const volumeFractionMomentum = parseFloat(await getRunInfo(runId, 'volume_fraction_momentum'))
  volumeFractionUpper.value = volumeFraction + volumeFractionMomentum
  volumeFractionLower.value = volumeFraction - volumeFractionMomentum
})
</script>
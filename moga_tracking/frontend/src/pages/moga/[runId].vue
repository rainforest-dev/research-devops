<template lang="pug">
div {{ runId }}
div {{ vf }}
</template>
<script setup lang="ts">
import { inject, reactive, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { mogaKey } from '@/providers';
import { getGen, getRunInfo } from '@/utils/api';

export interface Nacre {
  id: string;
  strength: number;
  toughness: number;
}

const route = useRoute()
const runId = Array.isArray(route.params.runId) ? route.params.runId[0] : route.params.runId
const gens = reactive<{ [gen: number]: Nacre[] }>({})

const { vf, addGen } = inject(mogaKey) ?? {}
watchEffect(async () => {
  const volumeFraction = parseFloat(await getRunInfo(runId, 'volume_fraction'))
  const volumeFractionMomentum = parseFloat(await getRunInfo(runId, 'volume_fraction_momentum'))
  if (vf) {
    vf.value = [volumeFraction - volumeFractionMomentum, volumeFraction + volumeFractionMomentum]
  }
})
watchEffect(async () => {
  var idx = 10
  while (true) {
    try {
      const gen = await getGen(runId, idx) || []
      gens[idx] = gen
      if (addGen)
        addGen(idx, { label: idx.toString(), data: gen.map(e => ({ x: e.strength, y: e.toughness })) })
      idx += 10
    } catch (error) {
      console.log(error)
      break
    }
  }
})
</script>
<template lang="pug">
ScatterChart(ref="scatterRef" :chart-data="data")
router-view
</template>
<script setup lang="ts">
import { computed, provide, reactive, ref, watchEffect } from 'vue';
import { useStorage } from '@vueuse/core';
import { ScatterChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
import * as chroma from 'chroma.ts'
import { NacreDB } from '@/types/api';
import { getDBTable } from '@/utils/api';
import * as providers from '@/providers';
import { mogaKey } from '@/providers';

Chart.register(...registerables)

const baseColor = ref<string>('OrRd')

const loading = ref(false)
const vf = useStorage('vf', [0, 1])
const dataset = ref<NacreDB[]>()
const gens = reactive<{ [key: number]: providers.ChartDataset }>({})
const colorscheme = computed(() => chroma.scale(baseColor.value).colors(Object.keys(gens).length))
const addGen = (key: number, data: providers.ChartDataset) => {
  gens[key] = data
}
watchEffect(async () => {
  loading.value = true
  dataset.value = await getDBTable('nacre', ['id', 'ultraStress', 'total_area'], undefined, vf.value)
  loading.value = false
})

const data = computed(() => ({
  datasets: [
    {
      label: "Dataset",
      data: (dataset.value ?? []).filter(e => e.strength && e.toughness).map(e => ({ x: e.strength!, y: e.toughness! }))
    },
    ...Object.values(gens).map((e, idx) => ({ ...e, backgroundColor: colorscheme.value[idx] }))
  ]
}))
provide(mogaKey, { vf, addGen })
</script>
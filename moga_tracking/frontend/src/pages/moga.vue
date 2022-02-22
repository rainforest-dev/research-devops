<template lang="pug">
.flex.flex-col.full
  .flex.items-center.space-x-2.p-2
    router-link(to="/moga" class="btn btn-outline hover:btn-circle")
      HomeIcon.h-5.w-5
    input.input.input-bordered(v-model="experimentName")
    select.select.select-bordered(:value="runId" @change="selectRun($event)")
      option(value="" selected disabled) Select a run
      option(v-for="item in runs" :key="item.id" :value="item.id") {{ item.id }} ({{ item.status }})
    span {{ vf[0].toFixed(2) }} - {{ vf[1].toFixed(2) }}
    button.btn.btn-outline(@click="exportChart")
      ShareIcon.h-5.w-5
  ScatterChart(ref="scatterRef" :chart-data="data" :options="options")
  .flex-grow.overflow-auto(v-show="selectedPoints.length > 0")
    .collapse.collapse-arrow(tabindex="0")
      input(type="checkbox")
      .collapse-title Dataset
      .collapse-content.flex.flex-col.space-y-2
        .card.card-side(v-for="item in datasetSelectedData" :key="item.id")
          figure.p-2
            img.w-48(:src="item.preview512")
          .card-body
            .card-title {{ item.id }}
            .stats
              .stat
                .stat-title Strength
                .stat-value {{ item.strength }}
              .stat
                .stat-title Toughness
                .stat-value {{ item.toughness }}
            .card-actions
              a.btn(:href="item.raw512" target="_blank" download) .npy
    .flex.overflow-x-auto.w-full.space-x-2
      img.w-48.border(v-for="item in datasetSelectedData" :key="item.id" :src="item.preview512")
    router-view
</template>
<script setup lang="ts">
import { computed, onMounted, provide, reactive, ref, toRef, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStorage } from '@vueuse/core';
import { ShareIcon, HomeIcon } from '@heroicons/vue/solid'
import { ScatterChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
import * as chroma from 'chroma.ts'
import { NacreDB, Run } from '@/types/api';
import { getRuns, getDBTable } from '@/utils/api';
import * as providers from '@/providers';
import { mogaKey } from '@/providers';

Chart.register(...registerables)

// https://www.npmjs.com/package/chroma.ts
const baseColor = ref<string>('OrRd')

const router = useRouter()
const route = useRoute()
const runId = computed(() => Array.isArray(route.params.runId) ? route.params.runId[0] : route.params.runId)

const loading = ref(false)
const vf = useStorage('vf', [0, 1])
const dataset = ref<NacreDB[]>([])
const experimentName = ref<string>('moga(test)')
const runs = ref<Run[]>([])
const gens = reactive<{ [key: number]: providers.ChartDataset }>({})
const gensLength = computed(() => Object.keys(gens).length)
const colorscheme = computed(() => chroma.scale(baseColor.value).colors(gensLength.value))
const addGen = (key: number, data: providers.ChartDataset) => {
  gens[key] = data
}
const removeGens = () => {
  Object.keys(gens).forEach(key => { delete gens[key as unknown as number] })
}
const selectRun = (event: Event) => {
  const target = event.target as HTMLSelectElement
  router.push({ path: `/moga/${target.value}` })
}
watchEffect(async () => {
  loading.value = true
  runs.value = await getRuns(experimentName.value) ?? []
  loading.value = false
})
watchEffect(async () => {
  loading.value = true
  dataset.value = await getDBTable('nacre', ['id', 'ultraStress', 'total_area', 'preview_512', 'raw_512'], undefined, vf.value) ?? []
  loading.value = false
})
const scatterRef = ref()
const selectedPoints = ref<{ datasetIndex: Number, index: Number }[]>([])
const datasetSelectedData = ref<NacreDB[]>()
const data = computed(() => ({
  datasets: [
    {
      label: "Dataset",
      order: gensLength.value,
      data: (dataset.value ?? []).filter(e => e.strength && e.toughness).map(e => ({ x: e.strength!, y: e.toughness! })),
      pointRadius: 6,
    },
    ...Object.values(gens).map((e, idx) => ({ ...e, order: gensLength.value - idx - 1, backgroundColor: colorscheme.value[idx], pointRadius: 6 }))
  ]
}))
const options = reactive({
  responsive: true,
  animation: false,
  plugins: {
    legend: {
      position: 'bottom',
    },
    title: {
      display: true,
      text: '',
    },
  },
  onHover: (evt: any) => {
    const instance = scatterRef.value.chartInstance
    const points = instance.getElementsAtEventForMode(evt, 'point', { intersect: false }, true);
    instance.setActiveElements(points.map((e: { datasetIndex: any; index: any; }) => ({ datasetIndex: e.datasetIndex, index: e.index })))
    instance.update()
  },
  onClick: (evt: any) => {
    const instance = scatterRef.value.chartInstance
    const points = instance.getElementsAtEventForMode(evt, 'point', { intersect: false }, true);
    selectedPoints.value = [...points]
  }
});
watchEffect(() => {
  if (dataset && selectedPoints.value.length > 0)
    datasetSelectedData.value = selectedPoints.value.filter((e) => e.datasetIndex === 0).map(e => dataset.value[e.index as number])
})
const exportChart = () => {
  const dataImage = scatterRef.value.chartInstance.toBase64Image()
  const a = document.createElement("a")
  a.href = dataImage
  a.download = `${runId.value ?? 'dataset_vf_' + vf.value.join('-')}.png`
  a.click()
}
provide(mogaKey, {
  vf,
  selectedPoints: computed(() => selectedPoints.value.filter(e => e.datasetIndex !== 0).map(e => ({ datasetIndex: e.datasetIndex as number - 1, index: e.index }))),
  addGen,
  removeGens
})
</script>
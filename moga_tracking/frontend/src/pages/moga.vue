<template lang="pug">
ScatterChart(ref="scatterRef" :chart-data="data" :options="options")
.card.bg-base-100.shadow-xl.fixed.right-4.bottom-4.h-96.overflow-auto(v-show="selectedPoints.length > 0")
  .card-body
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
    router-view
</template>
<script setup lang="ts">
import { computed, onMounted, provide, reactive, ref, toRef, watchEffect } from 'vue';
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
const dataset = ref<NacreDB[]>([])
const gens = reactive<{ [key: number]: providers.ChartDataset }>({})
const gensLength = computed(() => Object.keys(gens).length)
const colorscheme = computed(() => chroma.scale(baseColor.value).colors(gensLength.value))
const addGen = (key: number, data: providers.ChartDataset) => {
  gens[key] = data
}
watchEffect(async () => {
  loading.value = true
  dataset.value = await getDBTable('nacre', ['id', 'ultraStress', 'total_area', 'preview_512'], undefined, vf.value) ?? []
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
provide(mogaKey, { vf, selectedPoints: computed(() => selectedPoints.value.filter(e => e.datasetIndex !== 0).map(e => ({ datasetIndex: e.datasetIndex as number - 1, index: e.index }))), addGen })
</script>
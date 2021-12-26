<template lang="pug">
div {{ volumeFractionLower }} - {{ volumeFractionUpper }}
apexchart.full(type="scatter" :options="options" :series="series" v-if='series')
div {{ JSON.stringify(series) }}
</template>
<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRoute } from 'vue-router';
import { NacreDB } from '@/types/api';
import { getDBTable, getGen, getRunInfo } from '@/utils/api';

export interface Nacre {
  id: string;
  strength: number;
  toughness: number;
}

const route = useRoute()
const runId = Array.isArray(route.params.runId) ? route.params.runId[0] : route.params.runId
const volumeFractionUpper = ref<number>()
const volumeFractionLower = ref<number>()
const dataset = ref<NacreDB[]>()
const gens = reactive<{[gen:number]: Nacre[]}>({})
onMounted(async () => {
  const volumeFraction = parseFloat(await getRunInfo(runId, 'volume_fraction'))
  const volumeFractionMomentum = parseFloat(await getRunInfo(runId, 'volume_fraction_momentum'))
  volumeFractionUpper.value = volumeFraction + volumeFractionMomentum
  volumeFractionLower.value = volumeFraction - volumeFractionMomentum
  dataset.value = await getDBTable('nacre', ['id', 'ultraStress', 'total_area'], [volumeFractionLower.value, volumeFractionUpper.value])
  Array.from({length: 10}, (x, i) => i).forEach(async idx => gens[(idx+1) * 10] = [...await getGen(runId, (idx+1) * 10) || []])
  console.log(gens)
})

const series = computed(() => [
  {
    name: 'Dataset',
    data: dataset.value ? dataset.value.map(e => [e.strength, e.toughness]) : []
  },
  ...Object.entries(gens).map(([k, v]) => ({name: `gen ${k}`, data: v.map((e: Nacre) => [e.strength, e.toughness])}))
])
console.log(series.value)
const options = {
  chart: {
    height: 350,
    type: 'scatter',
    zoom: {
      enabled: true,
      type: 'xy'
    }
  },
  xaxis: {
    tickAmount: 10,
    labels: {
      formatter: function(val: string) {
        return parseFloat(val).toFixed(3)
      }
    }
  },
  yaxis: {
    tickAmount: 10,
    labels: {
      formatter: function(val: string) {
        return parseFloat(val).toFixed(3)
      }
    }
  },
}
</script>
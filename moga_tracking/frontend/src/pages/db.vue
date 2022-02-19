<template lang="pug">
.card.glass.fixed.top-4.right-4
  .card-content
    .collapse.collapse-arrow(tabindex="0")
      input(type="checkbox")
      .collapse-title.bg-transparent Filters ({{ loading ? 'Loading...' : `${filtered?.length} of ${dataset?.length} Found` }})
      .collapse-content.bg-transparent
        .w-64.h-min.flex.flex-col.px-4.space-y-8
          span Volume Fraction
          Slider.w-full(v-model="vf" :max="1" :step="-1" :merge="0.2")
          span Brittle Threshold
          .flex.items-center.space-x-2
            Slider.w-full(v-model="brittleThreshold" :max="1" :step="-1")
            input.toggle(type="checkbox" v-model="isBrittleFilterEnabled")
          span Total Area
          .flex.items-center
            Slider.w-full(v-model="totalAreaThreshold" :max="1" :step="-1")
.grid.grid-cols-10.gap-4
  router-link(v-for="item in filtered" :key="item.id" :to="`/db/${item.id}`" :class="[item.id === id && 'border-8 border-info']")
    img.aspect-square.border(v-lazy="item.preview512")
.fixed.bottom-4.right-4.p-4.w-96.shadow-xl.border.card.glass
  router-view
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watchEffect } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStorage } from "@vueuse/core";
import Slider from '@vueform/slider'
import { NacreDB } from '@/types/api';
import { getDBTable } from '@/utils/api';

const loading = ref(false)
const vf = useStorage('vf', [0, 1])
const brittleThreshold = useStorage('brittleThreshold', 0)
const isBrittleFilterEnabled = useStorage('isBrittleFilterEnabled', false)
const totalAreaThreshold = useStorage('totalAreaThreshold', 0.25)

const router = useRouter()
const route = useRoute()
const id = computed(() => Array.isArray(route.params.id) ? route.params.id[0] : route.params.id)

const dataset = ref<NacreDB[]>()
watchEffect(async () => {
  loading.value = true
  dataset.value = await getDBTable('nacre', ['id', 'preview_512', 'toughness_index'], undefined, vf.value, totalAreaThreshold.value)
  loading.value = false
})

const filtered = ref<NacreDB[]>([])
watchEffect(() => {
  if (isBrittleFilterEnabled.value) {
    console.log(isBrittleFilterEnabled.value, brittleThreshold.value, dataset.value?.filter(e => !e.isBrittle(brittleThreshold.value)).length)
    filtered.value = (dataset.value ?? []).filter(e => !e.isBrittle(brittleThreshold.value))
    return
  }
  filtered.value = dataset.value ?? []
})

watchEffect(() => {
  if (dataset.value && !dataset.value?.find(e => e.id === id.value)) router.replace({ path: '/db' })
})
</script>
<style src="@vueform/slider/themes/default.css"></style>
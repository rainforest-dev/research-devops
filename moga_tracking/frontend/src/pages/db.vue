<template lang="pug">
.card.glass.fixed.top-4.right-4
  .card-content
    .collapse.collapse-arrow(tabindex="0")
      input(type="checkbox")
      .collapse-title.bg-transparent Volume Fraction ({{ loading ? 'Loading...' : `${dataset?.length} Found` }})
      .collapse-content.bg-transparent
        .w-64.h-36.flex-center.p-4
          Slider.w-full(v-model="vf" :max="1" :step="-1")
.grid.grid-cols-10.full.gap-4
  router-link(v-for="item in dataset" :key="item.id" :to="`/db/${item.id}`" :class="[item.id === id && 'border-8 border-info']")
    img.aspect-square.border(:src="item.preview512")
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

const router = useRouter()
const route = useRoute()
const id = computed(() => Array.isArray(route.params.id) ? route.params.id[0] : route.params.id)

const dataset = ref<NacreDB[]>()
watchEffect(async () => {
  loading.value = true
  dataset.value = await getDBTable('nacre', ['*'], undefined, vf.value)
  loading.value = false
})

watchEffect(() => {
  if (!dataset.value?.find(e => e.id === id.value)) router.replace({ path: '/db' })
})
</script>
<style src="@vueform/slider/themes/default.css"></style>
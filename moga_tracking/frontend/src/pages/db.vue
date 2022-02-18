<template lang="pug">
.grid.grid-cols-10.full.gap-4
  router-link(v-for="item in dataset" :key="item.id" :to="`/db/${item.id}`" :class="[item.id === id && 'border-8 border-info']")
    img.aspect-square.border(:src="item.preview512")
.fixed.bottom-4.right-4.p-4.w-96.shadow-xl.border.card.glass
  router-view
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { NacreDB } from '@/types/api';
import { getDBTable } from '@/utils/api';

const route = useRoute()
const id = computed(() => Array.isArray(route.params.id) ? route.params.id[0] : route.params.id)

const dataset = ref<NacreDB[]>()
onMounted(async () => {
  dataset.value = await getDBTable('nacre', ['*'])
})
</script>
<template lang="pug">
.collapse.collapse-arrow(tabindex="0")
  input(type="checkbox")
  .collapse-title.bg-transparent {{ id }}
  .collapse-content.bg-transparent
    .max-h-96.overflow-auto
      table.table
        tbody(v-if="minorData")
          tr(v-for="([key, value], index) in Object.entries(minorData)" :key="key")
            td(:class="[index % 2 ? 'bg-base-100/15' : 'bg-transparent']") {{ key }}
            td(:class="[index % 2 ? 'bg-base-100/15' : 'bg-transparent']") {{ value }}
.grid.grid-cols-3.gap-2(v-if="data")
  img.border(:src="data.previewUnitCell")
  .image-links.full.relative
    img.border(:src="data.preview128")
    .absolute-full
      a(class="w-full h-max glass btn" :href="data.preview128" target="_blank" download) .jpg
      a(class="w-full h-max glass btn" :href="data.raw128"  target="_blank" download) .npy
  .image-links.full.relative
    img.border(:src="data.preview512")
    .absolute-full
      a(class="w-full h-max glass btn" :href="data.preview512" target="_blank" download) .jpg
      a(class="w-full h-max glass btn" :href="data.raw512"  target="_blank" download) .npy
</template>
<script setup lang="ts">
import { computed, onMounted, ref, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { classToPlain } from 'class-transformer';
import { omit } from 'lodash'
import { getDBItem } from '@/utils/api';
import { NacreDB } from '@/types/api';

const route = useRoute()
const id = computed(() => Array.isArray(route.params.id) ? route.params.id[0] : route.params.id)

const data = ref<NacreDB>()
watchEffect(async () => {
  if (id.value)
    data.value = await getDBItem('nacre', id.value, ['*'])
})
const minorData = computed(() => omit(classToPlain(data.value), ['id', 'preview_unit_cell', 'raw_unit_cell', 'preview_128', 'raw_128', 'preview_512', 'raw_512', 'old_id']))
</script>
<style lang="postcss" scoped>
.image-links .absolute-full {
  @apply invisible p-2 bg-black/80;
}
.image-links:hover .absolute-full {
  @apply visible;
}
</style>
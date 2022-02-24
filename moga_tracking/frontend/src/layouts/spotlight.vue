<template lang="pug">
div(:class="[file && 'dropdown dropdown-open']" @drop="handleDrop" @dragover="handleDragOver" @dragenter="handleDragEnter" @dragleave="handleDragLeave")
  button.btn.btn-link.full.shadow-inner.shadow-gray-500(:class="[isDragging && 'border-primary']" @click="reset")
    FingerPrintIcon.w-5.h-5.pointer-events-none
  .dropdown-content.card.bg-base-100.shadow(v-if="file")
    figure
      img(:src="url(`/nacre/${file.name.split('.')[0]}`)")
    .card-body
      .card-title.text-xs {{ file?.name }}
      table.table.table-compact.table-zebra
        tbody
          tr
            th Strength
            td {{ data.strength?.value?.toFixed(3) }} ({{ data.strength?.inverse?.toFixed(3) }})
          tr
            th Toughness
            td {{ data.toughness?.value?.toFixed(3) }} ({{ data.toughness?.inverse?.toFixed(3) }})
          tr
            th isBrittle
            td {{ data.isBrittle }}
</template>
<script setup lang="ts">
import { reactive, ref, watch } from "vue";
import { FingerPrintIcon } from "@heroicons/vue/solid"
import { urlToFile } from "@/utils";
import { url } from "@/utils/api"
import { classify, toughness, strength } from "@/utils/api/models";

interface ModelData {
  toughness?: {
    value?: number
    inverse?: number
  }
  strength?: {
    value?: number
    inverse?: number
  }
  isBrittle?: boolean
}

const isDragging = ref(false)
const handleDragEnter = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = true
}
const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
}
const handleDragLeave = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = false
}

const file = ref<File>()
const data = reactive<ModelData>({})

const reset = () => {
  file.value = undefined
  delete data.isBrittle
  delete data.strength
  delete data.toughness
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  event.stopPropagation()
  isDragging.value = false
  if (event.dataTransfer?.items[0].kind === 'file')
    file.value = event.dataTransfer?.items[0].getAsFile() ?? undefined
  else if (event.dataTransfer?.items[0].kind === 'string') {
    event.dataTransfer?.items[0].getAsString(async url => {
      file.value = await urlToFile(url)
    })
  }
}

watch(file, async () => {
  if (file.value) {
    let res = await strength(file.value)
    if (res && res.length) data.strength = { ...data.strength, inverse: res[0] }
    res = await strength(file.value, false)
    if (res && res.length) data.strength = { ...data.strength, value: res[0] }
  }
})

watch(file, async () => {
  if (file.value) {
    let res = await toughness(file.value)
    if (res && res.length) data.toughness = { ...data.toughness, inverse: res[0] }
    res = await toughness(file.value, false)
    if (res && res.length) data.toughness = { ...data.toughness, value: res[0] }
  }
})

watch(file, async () => {
  if (file.value) {
    const res = await classify(file.value)
    if (res && res.length) data.isBrittle = !res[0]
  }
})
</script>
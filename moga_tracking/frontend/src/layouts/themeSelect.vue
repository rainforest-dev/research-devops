<template lang="pug">
.dropdown.dropdown-end.space-y-2
  label.btn.btn-ghost.flex-nowrap(tabindex="0") {{ theme }}
    ColorSwatchIcon.w-5.h-5.ml-1
  ul.dropdown-content.bg-base-100.menu.rounded-box.shadow.max-h-96.overflow-auto.uppercase(tabindex="0")
    li(v-for="item in themes" :key="item" @click="() => selectTheme(item)")
      a {{ item }}
</template>
<script setup lang="ts">
import { onMounted, watch } from "vue";
import { themeChange } from "theme-change";
import { ColorSwatchIcon } from "@heroicons/vue/solid"
import { useLocalStorage } from "@vueuse/core";
import * as themesUtils from "@/utils/themes";

const { themes } = defineProps({
  themes: {
    type: Object,
    default: () => themesUtils.themes
  }
})

const theme = useLocalStorage('theme', themes[0])

watch(theme, () => {
  console.log(theme.value)
  if (theme.value) document.documentElement.setAttribute("data-theme", theme.value);
})

const selectTheme = (value: themesUtils.Theme) => { theme.value = value }

onMounted(() => {
  themeChange(false)
})
</script>


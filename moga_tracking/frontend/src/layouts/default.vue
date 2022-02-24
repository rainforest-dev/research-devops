<template lang="pug">
.flex.flex-col.full
  .navbar(v-if="!fullscreen")
    .navbar-start
      router-link.btn.btn-ghost(to="/") Research DevOps
    .navbar-end
      Spotlight
      a.btn.btn-ghost(href="http://rainforest80256.synology.me/" target="_blank") MLflow
        ExternalLinkIcon.w-5.h-5.ml-1
      .dropdown
        label.btn.btn-ghost.flex-nowrap(tabindex="0") Docs
          DocumentTextIcon.w-5.h-5.ml-1
        ul.menu.dropdown-content.w-60.bg-base-100.shadow.rounded-box(tabindex="0")
          li
            router-link(:to="`/docs?url=${url('/docs')}`") MOGA Tracking
          li
            router-link(:to="`/docs?url=http://localhost:8000/docs`") MLflow Model Serve
      router-link.btn.btn-ghost(to="/design_space") Design Space
        CubeTransparentIcon.w-5.h-5.ml-1
      router-link.btn.btn-ghost(to="/db") Database
        DatabaseIcon.w-5.h-5.ml-1
      router-link.btn.btn-ghost(to="/moga") MOGA
        BeakerIcon.w-5.h-5.ml-1
      ThemeSelect
  .flex-grow.full.overflow-auto
    router-view
</template>
<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router"
import { ExternalLinkIcon, DocumentTextIcon, CubeTransparentIcon, DatabaseIcon, BeakerIcon } from "@heroicons/vue/solid"
import { url } from "@/utils/api"
import Spotlight from "./spotlight.vue";
import ThemeSelect from "./themeSelect.vue";
const route = useRoute()
const fullscreen = computed(() => route.query.fullscreen === 'true')
</script>
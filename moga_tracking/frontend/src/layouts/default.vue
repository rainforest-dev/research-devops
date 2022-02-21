<template lang="pug">
.flex.flex-col.full
  .navbar
    .navbar-start
      router-link.btn.btn-ghost(to="/") Research DevOps
    .navbar-end
      .dropdown
        label.btn.btn-ghost(tabindex="0") Docs
        ul.menu.dropdown-content.w-60.bg-base-100.shadow.rounded-box(tabindex="0")
          li
            router-link(:to="`/docs?url=${url('/docs')}`") MOGA Tracking
          li
            router-link(:to="`/docs?url=http://localhost:8000/docs`") MLflow Model Serve
      router-link.btn.btn-ghost(to="/design_space") Design Space
      router-link.btn.btn-ghost(to="/db") Database
      router-link.btn.btn-ghost(to="/moga") MOGA
  .flex-grow.full.overflow-auto
    router-view
</template>
<script setup lang="ts">
import { url } from "@/utils/api"
</script>
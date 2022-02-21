<template lang="pug">
.full.overflow-auto
  iframe.full.border(:src="url")
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const url = computed(() => (Array.isArray(route.query.url) ? route.query.url[0] : route.query.url) as string)
</script>
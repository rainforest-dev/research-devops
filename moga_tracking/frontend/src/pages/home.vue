<template lang="pug">
.container.mx-auto.flex-center.full
  .flex-shrink
    NacrePreview
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
import NacrePreview from "@/components/NacrePreview.vue";

export default defineComponent({
  setup() {
    const data = ref<MessageEvent>();
    const connection = new WebSocket("ws://localhost:3000/ws");
    connection.onmessage = (event) => {
      console.log(event);
      data.value = event.data;
    };
    return { data };
  },
  components: { NacrePreview },
});
</script>
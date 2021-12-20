<template>
  <div>{{ JSON.stringify(data) }}</div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";

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
});
</script>

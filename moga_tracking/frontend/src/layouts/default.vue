<template lang="pug">
.navbar
  .navbar-start
    router-link.btn.btn-ghost(to="/") Research DevOps
  .navbar-end
    router-link.btn.btn-ghost(to="/design_space") Design Space
    router-link.btn.btn-ghost(to="/db") Database
    router-link.btn.btn-ghost(to="/moga") MOGA

router-view
</template>
<script setup lang="ts">

</script>
<template lang="pug">
.grid.grid-cols-10.full.gap-4
  .dropdown.dropdown-hover(v-for="item in items" :key="item.id" @click="handleClick(item.id)" :class="[item.disabled && 'brightness-50']")
    .grid.grid-cols-3.cursor-pointer
      .aspect-square.border.border-neutral(v-for="cell, index in item.parameters" :key="`${item.id}-${index}`" :class="[cell === 0 ? 'bg-black' : 'bg-white']")
    .dropdown-content.bg-base-100.p-4.w-96.shadow-xl.border.card
      img.aspect-square.border(:src="item.src")
</template>
<script setup lang="ts">
import { ref } from "vue";
import { Expose, plainToClass } from "class-transformer";
import "lodash.product"
// @ts-ignore
import {product} from "lodash"
import { designSpace } from "@/utils/constants"
import { id } from "@/utils"

class Item {
  parameters!: number[]
  disabled: boolean = false

  @Expose()
  get id() {
    return id(this.parameters)
  }
  @Expose()
  get src() {
    const paramsPart = this.parameters.join("_");
    return `http://localhost:3000/nacre/${paramsPart}_32_64_32_32_64_32`;
  }
}

const items = ref<Item[]>((product(...Object.values(designSpace)) as number[][]).map(parameters => plainToClass(Item, {parameters})))

const handleClick = (id: string) => {
  items.value = [...items.value.map(e => {
    if (e.id === id) {
      e.disabled = !e.disabled 
      return e
    }
    return e 
  })]
}
</script>
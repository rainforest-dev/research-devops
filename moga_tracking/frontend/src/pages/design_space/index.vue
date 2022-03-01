<template lang="pug">
.grid.grid-cols-10.gap-4
  .dropdown.dropdown-hover(v-for="item in items" :key="item.id" @click="handleClick(item.id)")
    .grid.grid-cols-3.cursor-pointer(:class="[!item.disabled && 'border-8 border-primary']")
      .aspect-square.border.border-neutral(v-for="cell, index in item.parameters" :key="`${item.id}-${index}`" :class="[cell === 0 ? 'bg-black' : 'bg-white']")
    .dropdown-content.bg-base-100.p-4.w-96.shadow-xl.border.card.delay-500
      span {{item.id}}
      img.aspect-square.border(:src="item.src")
.fixed.right-0.bottom-0.card
  .card-body
    .card-actions
      button.btn.btn-primary(v-if="runId" @click="loadRunData") {{ runId }}
      label.btn Import
        input.hidden(type="file" @change="importYAML"  accept="yaml")
      button.btn.btn-primary(@click="exportYAML") Export
</template>
<script setup lang="ts">
import {
  classToPlain,
  deserializeArray,
  Expose,
  plainToClass,
} from "class-transformer";
import "lodash.product";
// @ts-ignore
import { product, sortBy } from "lodash";
import { parse, stringify } from "yaml";
import { useStorage } from "@vueuse/core";
import { designSpace } from "@/utils/constants";
import { download, id, readFile } from "@/utils";
import { url } from "@/utils/api";

class Item {
  parameters!: number[];
  disabled: boolean = false;

  @Expose({ name: "id" })
  get id() {
    return id(this.parameters);
  }
  @Expose()
  get src() {
    const paramsPart = this.parameters.join("_");
    return `http://localhost:3000/nacre/${paramsPart}_32_64_32_32_64_32`;
  }
}

const parseItems = (text: string) => {
  const data = parse(text) as { S: { [key: string]: number[] } };
  const ids = Object.keys(data.S);
  items.value = [
    ...sortBy(
      items.value.map((e) => {
        e.disabled = !ids.includes(e.id);
        return e;
      }),
      ["disabled"]
    ),
  ];
};

const runId = useStorage("runId", undefined);
const loadRunData = async () => {
  if (runId.value) {
    const res = await fetch(url(`/mlflow/${runId.value}//search_spaces.yaml`));
    const blob = await res.blob();
    const text = await blob.text();
    parseItems(text);
  }
};

const items = useStorage(
  "items",
  (product(...Object.values(designSpace)) as number[][]).map((parameters) =>
    plainToClass(Item, { parameters })
  ),
  undefined,
  {
    serializer: {
      read: (v: any) => (v ? deserializeArray(Item, v) : []),
      write: (items: Item[]) =>
        JSON.stringify(items.map((v) => classToPlain(v))),
    },
  }
);

const handleClick = (id: string) => {
  items.value = [
    ...items.value.map((e) => {
      if (e.id === id) {
        e.disabled = !e.disabled;
        return e;
      }
      return e;
    }),
  ];
};

const importYAML = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (!files || !files[0]) return;
  readFile(files[0], parseItems);
};

const exportYAML = () => {
  download(
    stringify({
      S: Object.fromEntries(
        items.value.filter((e) => !e.disabled).map((e) => [e.id, e.parameters])
      ),
    }),
    "export.yaml",
    "text/yaml"
  );
};
</script>

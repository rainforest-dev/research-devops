<template lang="pug">
.flex.flex-col-reverse
  .flex.flex-col(v-for="([gen, items]) in Object.entries(selectedData)" :key="gen")
    .collapse.collapse-arrow(:tabindex="gen")
      input(type="checkbox")
      .collapse-title {{ gen }}
      .collapse-content.flex.flex-col.space-y-2
        .card.card-side(v-for="item in items" :key="item.id")
          figure.p-2
            img.w-48(:src="url(`/nacre/${item.id}`)")
          .card-body
            .card-title {{ item.id }}
            .stats
              .stat
                .stat-title Strength
                .stat-value {{ item.strength.toFixed(2) }}
              .stat
                .stat-title Toughness
                .stat-value {{ item.toughness.toFixed(2) }}
            .card-actions
              a.btn(:href="url(`/nacre/${item.id}?format=npy`)" target="_blank" download draggable="true") .npy
    .flex.overflow-x-auto.w-full.space-x-2
      img.w-48.border(v-for="item in items" :key="item.id" :src="url(`/nacre/${item.id}`)")
</template>
<script setup lang="ts">
import {
  computed,
  inject,
  onMounted,
  reactive,
  ref,
  watch,
  watchEffect,
} from "vue";
import { useRoute } from "vue-router";
import { groupBy, mapValues } from "lodash";
import { mogaKey } from "@/providers";
import { getGen, getRunInfo, url } from "@/utils/api";

export interface Nacre {
  id: string;
  strength: number;
  toughness: number;
}

const route = useRoute();
const runId = computed(() =>
  Array.isArray(route.params.runId) ? route.params.runId[0] : route.params.runId
);
const gens = ref<{ [gen: number]: Nacre[] }>({});

const { vf, selectedPoints, addGen, removeGens } = inject(mogaKey) ?? {};
const selectedData = computed(() => {
  const grouped = groupBy(
    selectedPoints?.value,
    (e) => Object.keys(gens.value)[e.datasetIndex - 1]
  );
  return mapValues(grouped, (points) =>
    points.map(
      (point) =>
        gens.value[
          Object.keys(gens.value)[point.datasetIndex - 1] as unknown as number
        ][point.index]
    )
  );
});
watchEffect(async () => {
  const volumeFraction = parseFloat(
    await getRunInfo(runId.value, "volume_fraction")
  );
  const volumeFractionMomentum = parseFloat(
    await getRunInfo(runId.value, "volume_fraction_momentum")
  );
  if (vf && volumeFraction && volumeFractionMomentum) {
    vf.value = [
      volumeFraction - volumeFractionMomentum,
      volumeFraction + volumeFractionMomentum,
    ];
  }
});
watchEffect(async () => {
  var idx = 10;
  const id = runId.value;
  while (true) {
    if (id !== runId.value) break;
    try {
      const gen = (await getGen(runId.value, idx)) || [];
      gens.value = { ...gens.value, [idx]: gen };
      if (addGen)
        addGen(idx, {
          label: idx.toString(),
          data: gen.map((e) => ({ x: e.strength, y: e.toughness })),
        });
      idx += 10;
    } catch (error) {
      console.log(error);
      break;
    }
  }
});
watch(
  () => runId.value,
  () => {
    // reset gens when run id is changed
    gens.value = {};
    removeGens && removeGens();
  }
);
</script>

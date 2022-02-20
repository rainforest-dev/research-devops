<template lang="pug">
.card.card-side.bordered.glass.px-2.py-3
  .card-body
    .form-control.grid.grid-cols-3.gap-2.mb-3
      template(v-for="designSpace in designSpaces", :key="designSpace.name")
        label.cursor-pointer.input-group.input-group-sm.flex-center(
          v-if="designSpace.type === form.FieldType.String || designSpace.type === form.FieldType.Number",
          :for="designSpace.name"
        )
          span {{ designSpace.name }}
          input.input.input-bordered.input-sm.min-w-auto.w-24(
            v-if="designSpace.type === form.FieldType.String",
            type="text",
            :value="S[designSpace.name]",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
          input.input.input-bordered.input-sm.min-w-auto.max-w-24.w-16(
            v-if="designSpace.type === form.FieldType.Number",
            type="number",
            :value="S[designSpace.name]",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
        label.label.cursor-pointer.flex-center(v-else, :for="designSpace.name")
          .label-text {{ designSpace.name }}
          input.toggle(
            v-if="designSpace.type === form.FieldType.Boolean",
            type="checkbox",
            :checked="S[designSpace.name] === true",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
    .tabs.tabs-boxed
      .tab(v-for="item in sizeOptions" :key="item" :class="[item === height && 'tab-active']" @click="height = item") {{ item }}
    Slider.mt-12.mb-2(v-model="hSlider" :max="height")
    .tabs.tabs-boxed
      .tab(v-for="item in sizeOptions" :key="item" :class="[item === length && 'tab-active']" @click="length = item") {{ item }}
    Slider.mt-12.mb-2(v-model="lSlider" :max="length")
    .card-actions
      button.btn.btn-sm.rounded-full(@click="clear") Clear

  figure
    img.full.object-cover(:src="url", :alt="url")
</template>
<script setup lang="ts">
import { computed, defineComponent, reactive, ref } from "vue";
import Slider from '@vueform/slider'
import * as form from "@/types/form";
import * as nacre from "@/types/nacre"

const a = typeof defineComponent;

const sizeOptions = [32, 64, 128]

const designSpaces: form.Field<nacre.Field>[] = [
  { name: "s1", type: form.FieldType.Boolean },
  { name: "s2", type: form.FieldType.Boolean },
  { name: "s3", type: form.FieldType.Boolean },
  { name: "s4", type: form.FieldType.Boolean },
  { name: "s5", type: form.FieldType.Boolean },
  { name: "s6", type: form.FieldType.Boolean },
  { name: "s7", type: form.FieldType.Boolean },
  { name: "s8", type: form.FieldType.Boolean },
  { name: "s9", type: form.FieldType.Boolean },
];

const defaultParams: { [key in nacre.Field]: boolean | number | string } = {
  s1: 1,
  s2: 0,
  s3: 1,
  s4: 0,
  s5: 1,
  s6: 1,
  s7: 0,
  s8: 0,
  s9: 0,
  Ha: 28,
  Hb: 29,
  Hc: 71,
  La: 33,
  Lb: 36,
  Lc: 59,
};

const _defaultValue = (field: form.Field<nacre.Field>, params = defaultParams) => {
  const value = params[field.name];
  switch (field.type) {
    case form.FieldType.Boolean:
      return Boolean(value);
    case form.FieldType.Number:
      return value;
    default:
      return undefined;
  }
};

var S = reactive<{ [key: string]: boolean | number | string }>(
  designSpaces.reduce(
    (a, x) => ({
      ...a,
      [x.name]: _defaultValue(x),
    }),
    {}
  )
);
const height = ref<number>(sizeOptions[0])
const length = ref<number>(sizeOptions[0])

const hSlider = ref<number[]>([16, 24])
const lSlider = ref<number[]>([16, 24])

const H = computed(() => [
  hSlider.value[0], hSlider.value[1] - hSlider.value[0], height.value - hSlider.value[1]
])
const L = computed(() => [
  lSlider.value[0], lSlider.value[1] - lSlider.value[0], length.value - lSlider.value[1]
])

const onChange = (designSpace: form.Field, e: Event) => {
  const target = <HTMLInputElement>e.target;
  switch (designSpace.type) {
    case form.FieldType.Boolean:
      S[designSpace.name] = target.checked;
      break;
    case form.FieldType.Number:
    case form.FieldType.String:
      S[designSpace.name] = target.value;
      break;
    default:
      break;
  }
};

const url = computed(() => {
  // "http://localhost:3000/nacre/1_0_1_0_1_1_0_0_0_28_29_71_33_36_59?img_size=512&format=jpg&unit_cell=false"
  const _params = [...Object.values(S).map((e) => Number(e)), ...H.value, ...L.value];
  const paramsPart = _params.join("_");
  return `http://localhost:3000/nacre/${paramsPart}`;
});

const clear = () => {
  designSpaces.forEach((e) => {
    const defaultValue = _defaultValue(e);
    if (defaultValue) S[e.name] = defaultValue;
  });
};
</script>
<style src="@vueform/slider/themes/default.css"></style>

<template lang="pug">
.card.card-side.bordered.glass.px-2.py-3
  .card-body
    .form-control.grid.grid-cols-2.gap-2
      template(v-for="designSpace in designSpaces", :key="designSpace.name")
        label.cursor-pointer.input-group.input-group-sm.flex-center(
          v-if="designSpace.type === FieldType.String || designSpace.type === FieldType.Number",
          :for="designSpace.name"
        )
          span {{ designSpace.name }}
          input.input.input-bordered.input-sm.min-w-auto.w-24(
            v-if="designSpace.type === FieldType.String",
            type="text",
            :value="params[designSpace.name]",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
          input.input.input-bordered.input-sm.min-w-auto.max-w-24.w-16(
            v-if="designSpace.type === FieldType.Number",
            type="number",
            :value="params[designSpace.name]",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
        label.label.cursor-pointer.flex-center(v-else, :for="designSpace.name")
          .label-text {{ designSpace.name }}
          input.toggle(
            v-if="designSpace.type === FieldType.Boolean",
            type="checkbox",
            :checked="params[designSpace.name] === true",
            @change="(e) => onChange(designSpace, e)",
            :id="designSpace.name"
          )
    .card-actions
      button.btn.btn-sm.glass.rounded-full(@click="clear") Clear

  figure
    img.full.object-cover(:src="url", :alt="url")
</template>
<script lang="ts">
import { computed, defineComponent, reactive } from "vue";
import { Field, FieldType } from "@/types/form";
import { Field as NacreField } from "@/types/nacre"

const a = typeof defineComponent;

const designSpaces: Field<NacreField>[] = [
  { name: "s1", type: FieldType.Boolean },
  { name: "s2", type: FieldType.Boolean },
  { name: "s3", type: FieldType.Boolean },
  { name: "s4", type: FieldType.Boolean },
  { name: "s5", type: FieldType.Boolean },
  { name: "s6", type: FieldType.Boolean },
  { name: "s7", type: FieldType.Boolean },
  { name: "s8", type: FieldType.Boolean },
  { name: "s9", type: FieldType.Boolean },
  { name: "Ha", type: FieldType.Number },
  { name: "Hb", type: FieldType.Number },
  { name: "Hc", type: FieldType.Number },
  { name: "La", type: FieldType.Number },
  { name: "Lb", type: FieldType.Number },
  { name: "Lc", type: FieldType.Number },
];

const defaultParams: { [key in NacreField]: boolean | number | string } = {
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

const _defaultValue = (field: Field<NacreField>, params = defaultParams) => {
  const value = params[field.name];
  switch (field.type) {
    case FieldType.Boolean:
      return Boolean(value);
    case FieldType.Number:
      return value;
    default:
      return undefined;
  }
};

export default defineComponent({
  setup() {
    var params = reactive<{ [key: string]: boolean | number | string }>(
      designSpaces.reduce(
        (a, x) => ({
          ...a,
          [x.name]: _defaultValue(x),
        }),
        {}
      )
    );

    const onChange = (designSpace: Field, e: Event) => {
      const target = <HTMLInputElement>e.target;
      switch (designSpace.type) {
        case FieldType.Boolean:
          params[designSpace.name] = target.checked;
          break;
        case FieldType.Number:
        case FieldType.String:
          params[designSpace.name] = target.value;
          break;
        default:
          break;
      }
    };

    const url = computed(() => {
      // "http://localhost:3000/nacre/1_0_1_0_1_1_0_0_0_28_29_71_33_36_59?img_size=512&format=jpg&unit_cell=false"
      const _params = Object.values(params).map((e) => Number(e));
      const paramsPart = _params.join("_");
      return `http://localhost:3000/nacre/${paramsPart}`;
    });

    const clear = () => {
      designSpaces.forEach((e) => {
        const defaultValue = _defaultValue(e);
        if (defaultValue) params[e.name] = defaultValue;
      });
    };

    return { params, designSpaces, FieldType, onChange, url, clear };
  },
});
</script>

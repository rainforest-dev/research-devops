import { InjectionKey, Ref, reactive, ComputedRef } from "vue";

interface ChartDataset {
  label: string;
  data: { x: number; y: number }[];
}

interface MogaProvide {
  vf: Ref<number[]>;
  selectedPoints: ComputedRef<{ datasetIndex: number; index: number }[]>;
  addGen: (key: number, data: ChartDataset) => {};
  removeGens: () => {};
}

export const mogaKey = Symbol() as InjectionKey<MogaProvide>;
export type { ChartDataset };

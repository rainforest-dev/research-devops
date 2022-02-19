import { InjectionKey, Ref, reactive } from "vue";

interface ChartDataset {
  label: string;
  data: { x: number; y: number }[];
}

interface MogaProvide {
  vf: Ref<number[]>;
  addGen: (key: number, data: ChartDataset) => {};
}

export const mogaKey = Symbol() as InjectionKey<MogaProvide>;
export type { ChartDataset };

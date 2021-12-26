import { Expose } from "class-transformer";

export enum RunInfoType {
  Params = "params",
}

export interface Nacre {
  id: string;
  strength: number;
  toughness: number;
}

export class NacreDB {
  @Expose()
  id?: string;
  @Expose({ name: "ultraStress" })
  strength?: number;
  @Expose({ name: "total_area" })
  toughness?: number;
}

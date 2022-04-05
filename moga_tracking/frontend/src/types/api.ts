import { Expose, Transform } from "class-transformer";
import { url } from "@/utils/api";

export interface ApiEndpoint {
  url: string;
  version?: number;
}

export interface ApiEndpoints {
  strength: ApiEndpoint;
  toughness: ApiEndpoint;
  classification: ApiEndpoint;
}

export enum RunStatus {
  Finished = "FINISHED",
}

export class Run {
  id!: string;
  status!: RunStatus;
  @Expose({ name: "start_time" })
  @Transform(({ value }) => new Date(value))
  startAt!: Date;
  @Transform(({ value }) => new Date(value))
  @Expose({ name: "end_time" })
  endAt!: Date;
}

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
  @Expose({ name: "toughness_index" })
  toughnessIndex?: number;
  @Expose({ name: "preview_unit_cell" })
  @Transform(({ value }) => url(`/${value}`))
  previewUnitCell?: string;
  @Expose({ name: "raw_unit_cell" })
  @Transform(({ value }) => url(`/${value}`))
  rawUnitCell?: string;
  @Expose({ name: "preview_128" })
  @Transform(({ value }) => url(`/${value}`))
  preview128?: string;
  @Expose({ name: "raw_128" })
  @Transform(({ value }) => url(`/${value}`))
  raw128?: string;
  @Expose({ name: "preview_512" })
  @Transform(({ value }) => url(`/${value}`))
  preview512?: string;
  @Expose({ name: "raw_512" })
  @Transform(({ value }) => url(`/${value}`))
  raw512?: string;

  isBrittle(threshold: number) {
    return (this.toughnessIndex ?? 0) <= threshold;
  }
}

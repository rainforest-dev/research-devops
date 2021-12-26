import { RunInfoType, NacreDB, Nacre } from "@/types/api";
import { plainToClass } from "class-transformer";

const _url = (url: string) => `${import.meta.env.VITE_API_ENDPOINT}${url}`;

export const getRunInfo = async (
  runId: string,
  infoKey: string,
  infoType: RunInfoType = RunInfoType.Params
) => {
  try {
    const res = await fetch(_url(`/mlflow/${runId}/${infoType}/${infoKey}`));
    return await res.json();
  } catch (error) {
    console.warn(error);
  }
};

export const getDBTable = async (
  table: string,
  fields: string[],
  volumeFraction: number[] = [0, 1],
  num: number = 300
) => {
  try {
    const params: { [key: string]: string } = {
      fields: fields.join("-"),
      num: num.toString(),
    };
    if (volumeFraction.length > 0)
      params["vf"] = volumeFraction.map((e) => (e ? e : "")).join("-");
    const res = await fetch(
      _url(`/db/${table}?`) + new URLSearchParams(params)
    );
    const json = (await res.json()) as Array<object>;
    const data = json.map((e) => plainToClass(NacreDB, e));
    return data;
  } catch (error) {
    console.warn(error);
  }
};

export const getGen = async (
  runId: string,
  genId: number,
  num: number = 30
) => {
  try {
    const res = await fetch(
      _url(`/mlflow/${runId}/moga/gens/${genId}?num=${num}`)
    );
    return (await res.json()) as Nacre[];
  } catch (error) {
    console.warn(error);
  }
};

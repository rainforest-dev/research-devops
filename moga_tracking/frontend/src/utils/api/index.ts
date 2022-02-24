import { RunInfoType, NacreDB, Nacre, Run } from "@/types/api";
import { plainToClass } from "class-transformer";

const _url = (url: string) =>
  `${import.meta.env.VITE_API_ENDPOINT ?? ""}${url}`;

export const url = _url;

export const getRuns = async (experimentName: string) => {
  try {
    const res = await fetch(_url(`/mlflow/${experimentName}`));
    const data = (await res.json()) as Array<Record<string, any>>;
    return data.map((e) => plainToClass(Run, e));
  } catch (error) {
    console.warn(error);
  }
};

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
  num?: number,
  volumeFraction: number[] = [0, 1],
  totalArea: number = 0.25
) => {
  try {
    const params: { [key: string]: string } = {
      fields: fields.join("-"),
    };
    if (num) params["num"] = num.toString();
    if (volumeFraction.length > 0) params["vf"] = volumeFraction.join("-");
    if (totalArea) params["total_area"] = totalArea.toString();
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

export const getDBItem = async (
  table: string,
  id: string,
  fields: string[]
) => {
  try {
    const params: { [key: string]: string } = {
      fields: fields.join("-"),
    };
    const res = await fetch(
      _url(`/db/${table}/${id}?`) + new URLSearchParams(params)
    );
    return plainToClass(NacreDB, await res.json());
  } catch (error) {
    console.warn(error);
  }
};

export const getGen = async (runId: string, genId: number, num?: number) => {
  try {
    const params: { [key: string]: string } = {};
    if (num) params["num"] = num.toString();
    const res = await fetch(
      _url(`/mlflow/${runId}/moga/gens/${genId}?`) + new URLSearchParams(params)
    );
    return (await res.json()) as Nacre[];
  } catch (error) {
    throw error;
  }
};

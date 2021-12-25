import { RunInfoType } from "@/types/api";

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

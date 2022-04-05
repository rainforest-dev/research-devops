const {
  VITE_MODEL_API_ENDPOINT,
  VITE_STRENGTH_RUN_ID,
  VITE_TOUGHNESS_RUN_ID,
  VITE_CLASSIFICATION_RUN_ID,
} = import.meta.env;

const _url = (url: string) =>
  `${
    `${window.location.protocol}//${window.location.hostname}${VITE_MODEL_API_ENDPOINT}` ??
    ""
  }${url}`;
export const model_url = _url;

export const strength = async (file: File, inverse = true) => {
  try {
    const data = new FormData();
    data.append("file", file);
    const res = await fetch(
      _url(`/predict/${VITE_STRENGTH_RUN_ID}?inverse=${inverse}`),
      {
        method: "POST",
        body: data,
      }
    );
    return (await res.json())["data"] as number[];
  } catch (error) {
    console.warn(error);
  }
};

export const toughness = async (file: File, inverse = true) => {
  try {
    const data = new FormData();
    data.append("file", file);
    const res = await fetch(
      _url(`/predict/${VITE_TOUGHNESS_RUN_ID}?inverse=${inverse}`),
      {
        method: "POST",
        body: data,
      }
    );
    return (await res.json())["data"] as number[];
  } catch (error) {
    console.warn(error);
  }
};

export const classify = async (file: File, threshold = 0.5) => {
  try {
    const data = new FormData();
    data.append("file", file);
    const res = await fetch(
      _url(`/classify/${VITE_CLASSIFICATION_RUN_ID}?threshold=${threshold}`),
      {
        method: "POST",
        body: data,
      }
    );
    return (await res.json())["data"] as boolean[];
  } catch (error) {
    console.warn(error);
  }
};

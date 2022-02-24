export const id = (list: number[]) => list.join("_");

export function readFile(file: File, callback: (text: string) => void) {
  const reader = new FileReader();
  reader.onload = async (e) => {
    const text = e.target?.result;
    try {
      callback(text?.toString()!);
    } catch (error) {}
  };
  reader.readAsText(file);
}

export function download(
  content: BlobPart,
  fileName: string,
  contentType: string
) {
  var a = document.createElement("a");
  var file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

export const urlToFilename = (url: string) =>
  url.substring(url.lastIndexOf("/") + 1);

export const urlToFile = async (url: string) => {
  const res = await fetch(url);
  const filename = urlToFilename(url).replace("?format=", ".");
  const type = res.headers.get("content-type") ?? undefined;
  const blob = await res.blob();
  return new File([blob], filename, { type });
};

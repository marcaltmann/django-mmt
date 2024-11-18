const baseUrl = `${import.meta.env.VITE_API_URL}`;

export default function addFile(options) {
  const { fileId, file, filename, onProgress, onEnd, onAbort } = options;

  const uploadEndPoint = `/de/uploaded-files/${fileId}/upload/`;

  const request = new XMLHttpRequest();
  request.withCredentials = true;

  request.addEventListener("loadend", () => {
    if (typeof onEnd === "function") {
      onEnd();
    }
  });

  request.addEventListener("abort", () => {
    if (typeof onAbort === "function") {
      onAbort();
    }
  });

  request.open("POST", uploadEndPoint);

  const formData = new FormData();
  formData.append("file", file, filename);

  const uploadObject = request.upload;
  uploadObject.addEventListener("progress", event => {
    if (event.lengthComputable && typeof onProgress === "function") {
      onProgress(event.loaded);
    }
  });

  request.send(formData);

  return request;
}

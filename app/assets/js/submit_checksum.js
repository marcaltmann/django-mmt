import { fetchWrapper } from "./fetch_wrapper"

const baseUrl = import.meta.env.VITE_API_URL;

export default async function submitChecksum(uploadedFileId, checksum) {
  const resultPromise = fetchWrapper
    .post(`${baseUrl}/uploaded-files/${uploadedFileId}/update/`, {
      checksum_client: checksum
    })
    .catch(err => {
      console.log(err); // TODO: Associate error with upload.
      return null;
    })
  return resultPromise;
}

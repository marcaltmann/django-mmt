import { fetchWrapper } from '@/helpers/fetch-wrapper'

const baseUrl = import.meta.env.VITE_API_URL

export default async function submitChecksum(uploadedFileId: number, checksum: string) {
  const resultPromise = fetchWrapper
    .post(`${baseUrl}/uploaded-files/${uploadedFileId}/update/`, { checksum_client: checksum })
    .catch((err) => {
      console.log(err) // TODO: Associate error with upload.
      return null
    })
  return resultPromise
}

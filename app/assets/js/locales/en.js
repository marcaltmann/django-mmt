export default {
  components: {
    CurrentUpload: {
      upload: 'Upload',
      checksum: 'Checksum'
    },
    UploadButton: {
      label: 'Select files to upload'
    },
    UploadForm: {
      title: 'Title',
      description: 'Description',
      language: 'Language',
      makeAvailableOnPlatform: 'Make available on platform',
      transcribe: 'Transcribe',
      checkMediaFiles: 'Check media files',
      replaceExistingFiles: 'Replace existing files',
      submit: 'Submit and upload',
      reset: 'Reset'
    },
    UploadQueue: {
      cancel: 'Cancel',
      noJobs: 'Currently, there are no jobs pending in the upload queue.',
    },
  },
  no_downloads_directory: 'Downloads directory does not exist for the user.',
  'TypeError: NetworkError when attempting to fetch resource.':
    'NetworkError when attempting to fetch resource.',
  'TypeError: Failed to fetch': 'NetworkError when attempting to fetch resource.',
  'Not logged in': 'Not logged in.'
}

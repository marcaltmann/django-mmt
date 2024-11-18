export default {
  components: {
    CurrentUpload: {
      upload: 'Upload',
      checksum: 'Prüfsumme'
    },
    UploadButton: {
      label: 'Dateien zum Hochladen auswählen'
    },
    UploadForm: {
      title: 'Titel',
      description: 'Beschreibung',
      language: 'Sprache',
      makeAvailableOnPlatform: 'Auf der Plattform bereitstellen',
      transcribe: 'Transkribieren',
      checkMediaFiles: 'Mediendateien überprüfen',
      replaceExistingFiles: 'Vorhandene Dateien austauschen',
      submit: 'Absenden und hochladen',
      reset: 'Zurücksetzen'
    },
    UploadQueue: {
      cancel: 'Abbrechen',
      noJobs: 'Derzeit befinden sich keine Aufträge in der Upload-Warteschlange.',
    },
  },
  no_downloads_directory: 'Das Downloads-Verzeichnis existiert nicht für den Benutzer.',
  'TypeError: NetworkError when attempting to fetch resource.':
    'Netzwerkfehler beim Versuch, die Ressource abzurufen.',
  'TypeError: Failed to fetch': 'Netzwerkfehler beim Versuch, die Ressource abzurufen.',
  'Not logged in': 'Nicht angemeldet.'
}

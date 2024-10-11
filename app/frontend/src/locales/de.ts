export default {
  components: {
    CurrentUpload: {
      upload: 'Upload',
      checksum: 'Prüfsumme'
    },
    DownloadsTable: {
      filename: 'Dateiname',
      type: 'Typ',
      size: 'Größe',
      modified: 'Zuletzt geändert',
      actions: 'Aktionen',
      download: 'Datei herunterladen'
    },
    LoginForm: {
      username: 'Benutzername',
      usernamePlaceholder: 'Benutzername eingeben',
      password: 'Passwort',
      passwordPlaceholder: 'Passwort eingeben',
      submit: 'Anmelden'
    },
    RegistrationComplete: {
      title: 'Registrierung abgeschlossen',
      message: 'Danke {username}, Sie sind jetzt registriert.',
      activation:
        'Bitte warten Sie, bis unsere Administratoren Ihre Registrierung überprüft und Ihr Konto aktiviert haben.'
    },
    RegistrationForm: {
      title: 'Registrieren',
      username: 'Benutzername',
      usernamePlaceholder: 'Benutzername eingeben',
      usernameHelp:
        'Ihr Benutzername muss zwischen 4 und 12 Zeichen lang sein und kann aus Buchstaben, Ziffern und den Zeichen - und _ bestehen.',
      email: 'E-Mail-Adresse',
      emailPlaceholder: 'E-Mail-Adresse eingeben',
      password: 'Passwort',
      passwordPlaceholder: 'Passwort eingeben',
      repeatPassword: 'Passwort wiederholen',
      repeatPasswordPlaceholder: 'Passwort erneut eingeben',
      submit: 'Registrieren'
    },
    SiteFooter: {
      legalNotice: 'Impressum',
      privacy: 'Datenschutz',
      accessibility: 'Barrierefreiheit',
      contact: 'Kontakt'
    },
    SiteHeader: {
      admin: 'Admin',
      downloads: 'Downloads',
      logIn: 'Anmelden',
      logOut: 'Abmelden',
      newUpload: 'Neuer Upload',
      register: 'Registrieren',
      uploads: 'Uploads'
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
    UploadsTable: {
      id: 'Id',
      filename: 'Dateiname',
      mediaType: 'Medientyp',
      size: 'Größe',
      state: 'Status',
      uploaded: 'Hochgeladen',
      actions: 'Aktionen',
      delete: 'Löschen',
      created: 'erstellt',
      ok: 'OK?',
      checksumMatch: 'Prüfsumme: {checksum}',
      checksumMismatch: 'Server: {checksumServer}\nBrowser: {checksumClient}',
    },
    UploadTray: {
      title: 'Upload-Warteschlange',
      toggle: 'Upload-Warteschlange umschalten'
    },
    UserProfile: {
      username: 'Benutzername',
      email: 'E-Mail',
      locale: 'Gebietsschema',
      admin: 'Administrator-Rechte',
      can_upload: 'Upload-Rechte',
    },
    UsersTable: {
      id: 'Id',
      username: 'Benutzername',
      email: 'E-Mail',
      locale: 'Gebietsschema',
      uploadCount: 'Uploads',
      activated: 'Aktiviert?',
      admin: 'Admin?',
      canUpload: 'Upload-Berechtigung?',
      actions: 'Aktionen',
      activate: 'Benutzer aktivieren'
    },
  },
  general: {
    booleans: {
      true: 'ja',
      false: 'nein'
    },
    locales: {
      en: 'Englisch',
      de: 'Deutsch'
    },
  },
  views: {
    AccessibilityView: {
      title: 'Barrierefreiheit'
    },
    AdminView: {
      title: 'Administration',
      confirmActivation: 'Möchten Sie den Benutzer {username} aktivieren?'
    },
    ContactView: {
      title: 'Kontakt'
    },
    DownloadsView: {
      title: 'Downloads'
    },
    HomeView: {
      title: 'Willkommen bei MMT'
    },
    LegalNoticeView: {
      title: 'Impressum'
    },
    LoginView: {
      title: 'Anmelden'
    },
    NewUploadView: {
      title: 'Neuer Upload'
    },
    NotFoundView: {
      message: 'Entschuldigung, wir konnten diese Seite nicht finden.',
      back: 'Zurück zur Startseite'
    },
    PrivacyView: {
      title: 'Datenschutz'
    },
    ProfileView: {
      title: 'Profil'
    },
    UploadsView: {
      confirmDelete: 'Möchten Sie die Datei {filename} wirklich löschen?',
      title: 'Uploads'
    }
  },
  password_mismatch: 'Die Passwörter stimmen nicht überein.',
  username_password_mismatch: 'Benutzername und Passwort stimmen nicht überein.',
  user_not_activated: 'Der Benutzer wurde noch nicht aktiviert.',
  no_downloads_directory: 'Das Downloads-Verzeichnis existiert nicht für den Benutzer.',
  'TypeError: NetworkError when attempting to fetch resource.':
    'Netzwerkfehler beim Versuch, die Ressource abzurufen.',
  'TypeError: Failed to fetch': 'Netzwerkfehler beim Versuch, die Ressource abzurufen.',
  'Not logged in': 'Nicht angemeldet.'
}

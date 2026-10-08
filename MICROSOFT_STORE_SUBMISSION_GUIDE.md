# 🛍️ Microsoft Store Partner Center — Fresh Submission Kit

This guide contains **all copy-paste text fields, URLs, metadata, and asset paths** needed to submit **Sortify** for a fresh approval on the Microsoft Store Partner Center.

---

## 📋 1. App Overview & Category

| Field | Partner Center Input |
|---|---|
| **App Name** | `Sortify — Smart File Organizer & Utility Engine` (or `Sortify`) |
| **Category** | **Utilities & tools** |
| **Subcategory** | **File management** |
| **Pricing** | **Free** |
| **Markets** | All 240+ markets worldwide |

---

## 📝 2. Store Listing Text Fields

### 📌 Product Title
```text
Sortify — Smart File Organizer & Utility Engine
```

### 📌 Short Description (Max 258 characters)
```text
Automatically organize cluttered Downloads, Desktop & Documents into clean category folders. Detect duplicate files with SHA-256, create password-protected AES ZIPs, analyze large files, and safely manage files with 100% offline privacy and 1-click Undo.
```

### 📌 Full Description
```text
Sortify is a powerful, 100% local desktop assistant designed to bring order to your files without compromising data safety or privacy.

Whether your Downloads folder is filled with hundreds of unorganized PDFs, lecture slides, ZIP archives, photos, and installers, or your desktop needs a clean triage, Sortify automates file organization into structured category folders with zero risk of file overwrites.

✨ CORE FEATURES:

• 📁 AUTOMATIC FILE TRIAGE: Instantly sort files into clean category folders (Images, PDFs, Documents, Spreadsheets, Presentations, Videos, Audio, Archives, Code, Applications, Fonts) based on extension rules.
• 🛡️ ZERO-RISK COLLISION RESOLUTION: Guarantees zero file loss by generating collision-free filenames (e.g. photo_1.jpg) if duplicate filenames exist.
• 📂 INTEGRATED FILES MANAGER: Browse files, copy/move, rename, toggle hidden file attributes, and perform operations seamlessly.
• ♻️ WINDOWS RECYCLE BIN INTEGRATION: Deletions use the native Windows Recycle Bin (SHFileOperationW), preventing accidental permanent file loss.
• 🔒 AES-256 ENCRYPTED ZIP ARCHIVES: Compress files into standard ZIPs or create password-encrypted archives using AES-256 for maximum privacy.
• 🔍 CRYPTOGRAPHIC DUPLICATE FINDER: Uses a 2-stage SHA-256 hashing engine to pinpoint byte-for-byte duplicate downloads and recover disk space.
• 📈 STORAGE ANALYTICS: Instantly scan any folder to list the Top 25 Largest Files and visualize category space distribution.
• 📜 ACTIVITY JOURNAL & 1-CLICK UNDO: Every batch operation is recorded in a persistent journal, allowing instant 1-click restoration to original locations.
• 🔒 100% LOCAL & PRIVATE: Operates entirely offline on your computer. Zero cloud telemetry, zero data tracking, and zero hidden network requests.
```

### 📌 Release Notes (What's New in Version 1.0)
```text
Initial Release of Sortify Version 1.0 — Featuring Smart Triage, Cryptographic Duplicate Finder, AES Encrypted ZIP creation, Windows Recycle Bin safety, Storage Analytics, and 1-Click Batch Undo.
```

### 📌 App Features (Bullet Points)
```text
Automated file sorting by extension rules
Dry-run preview before committing file moves
Zero-overwrite collision-free renaming
Windows Recycle Bin non-destructive deletion
AES-256 password-protected ZIP archive creation
2-Stage SHA-256 duplicate file detector
Top 25 largest files storage analyzer
1-Click Undo activity journal
Dark and Light visual themes
100% offline local privacy
```

### 📌 Search Keywords (Up to 7 keywords)
```text
file organizer
sort downloads
duplicate finder
recycle bin
zip password
disk space analyzer
file management
```

### 📌 Copyright & Legal
```text
Copyright Notice: © 2026 Francis Kusi / Brainiac Web Tech. All rights reserved.
```

### 📌 Web Links
- **Privacy Policy URL**: `https://github.com/brainiacweb-tech/sortify/blob/main/PRIVACY_POLICY.md`
- **Terms of Service URL**: `https://github.com/brainiacweb-tech/sortify/blob/main/TERMS_OF_SERVICE.md`
- **Support Contact URL**: `https://github.com/brainiacweb-tech/sortify/issues`

---

## 🎨 3. Visual Assets (Ready in `assets/`)

All images are pre-formatted to exact Microsoft Store specification pixel dimensions:

| Asset Description | File Location in Workspace | Dimension |
|---|---|---|
| **App Tile / Logo (1:1)** | [`assets/store_logo_1080.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/store_logo_1080.png) | 1080 x 1080 px |
| **Poster Art (2:3)** | [`assets/store_poster_720x1080.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/store_poster_720x1080.png) | 720 x 1080 px |
| **Hero Showcase Banner** | [`assets/store_hero_laptop.jpg`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/store_hero_laptop.jpg) | High-Res Laptop Banner |
| **Screenshot 1 — Dashboard** | [`assets/screenshot_1_dashboard.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/screenshot_1_dashboard.png) | 1080p High Contrast |
| **Screenshot 2 — Organize** | [`assets/screenshot_2_organize.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/screenshot_2_organize.png) | 1080p High Contrast |
| **Screenshot 3 — Duplicates** | [`assets/screenshot_3_duplicates.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/screenshot_3_duplicates.png) | 1080p High Contrast |
| **Screenshot 4 — History & Undo** | [`assets/screenshot_4_history.png`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/screenshot_4_history.png) | 1080p High Contrast |
| **App Icon** | [`assets/logo.ico`](file:///c:/Users/USER/OneDrive/Desktop/Sortify/assets/logo.ico) | Multi-size ICO |

---

## 🛡️ 4. IARC Age Rating Questionnaire Answers

When filling out the **IARC Age Rating** questionnaire in Partner Center:

1. **Category**: Select **Utility / Tool**.
2. **Violence**: Select **No**.
3. **Profanity / Explicit Content**: Select **No**.
4. **Controlled Substances / Gambling**: Select **No**.
5. **User Interactions / Online Features**: Select **No** (App does not allow users to communicate or share data online).
6. **Result**: Your app will be rated **Everyone / 3+** globally across all regions.

---

## 📦 5. Submitting Your Package (.msix)

1. Open PowerShell in the project directory and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install_for_msix.ps1
   ```
2. Launch the **Microsoft MSIX Packaging Tool** (installable from Microsoft Store).
3. Select **Application Package** -> point to `SORTIFY.exe`.
4. Upload the generated `.msix` file under the **Packages** section in Partner Center.
5. Click **Submit to the Store**!

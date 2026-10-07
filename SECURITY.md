# Security Policy for SORTIFY

## 🛡️ Security Overview & Architecture

**SORTIFY** is built from the ground up as a **privacy-first, zero-telemetry, local desktop utility**. It is designed to run entirely offline on Microsoft Windows without communicating with external web services or telemetry endpoints.

### Key Security Safeguards:
1. **Zero Data Collection & Telemetry:**
   - No tracking, no user profiling, no remote logging, and no external API requests.
   - Operates 100% locally on your machine.

2. **System Directory Boundaries:**
   - Built-in path validators prevent accidental operation on critical Windows system directories (`C:\Windows`, `C:\Program Files`, `C:\Program Files (x86)`, `SystemRoot`, and root system drives).

3. **Data Loss Prevention & Atomic Move Safety:**
   - **Dry-Run Preview:** Every organization step calculates a full preview before any filesystem modifications occur.
   - **Collision Protection:** Automatically detects existing target filenames and applies safe sequence numbering (e.g. `file (1).ext`) to eliminate data overwrites.
   - **SHA-256 Duplicate Hashing:** Incremental chunk-based hashing avoids loading huge files into memory while ensuring exact cryptographic duplicate matching.
   - **Action Journaling & Undo:** Complete history logging in `%USERPROFILE%\.smart_file_organizer\history.json` enables instant, 100% reversible batch undos.

4. **Path Traversal & Injection Immunity:**
   - Strict `pathlib.Path.resolve()` canonicalization neutralizes relative path manipulation attacks (`../`, symlink loops, or invalid environment strings).

---

## 🔒 Supported Versions

Only the latest release of **SORTIFY** receives security updates and compliance enhancements:

| Version | Supported          |
| ------- | ------------------ |
| `1.0.x` | :white_check_mark: |
| `< 1.0` | :x:                |

---

## 📩 Reporting a Vulnerability

We take the security and integrity of **SORTIFY** very seriously. If you discover a security vulnerability or potential issue:

1. **Private Disclosure:** Please report security vulnerabilities directly to the developer by opening an issue or contacting **Francis Kusi** via [GitHub Profile](https://github.com/brainiacweb-tech).
2. **Response SLA:** We acknowledge all security reports within **24 hours** and aim to release a patch within **7 days**.
3. **Public Disclosure:** Please refrain from publicly disclosing the vulnerability until a security patch has been published.

---

## 📄 License & Compliance

SORTIFY is open-source software licensed under the [MIT License](LICENSE).

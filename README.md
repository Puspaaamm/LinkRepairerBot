<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/Wikipedia-logo-v2-hi.svg" width="120" alt="Hindi Wikipedia Logo" />
</p>

<h1 align="center">LinkRepairerBot (कड़ियाँ सुधारक बॉट)</h1>

<p align="center">
  <strong>An automated Pywikibot framework for Hindi Wikipedia (hi.wikipedia.org)</strong> <br />
  Designed to detect dead external links and automatically replace them with Wayback Machine archive links.
</p>

<p align="center">
  <a href="https://hi.wikipedia.org"><img src="https://img.shields.io/badge/Platform-Hindi%20Wikipedia-9C27B0?style=flat-square" alt="Hindi Wiki" /></a>
  <a href="https://www.mediawiki.org/wiki/Manual:Pywikibot"><img src="https://img.shields.io/badge/Framework-Pywikibot-007ACC?style=flat-square" alt="Pywikibot" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-4CAF50?style=flat-square" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/Status-In%20Development-FF9800?style=flat-square" alt="Status" />
</p>

---

## Overview

**LinkRepairerBot** is a maintenance bot designed to preserve the integrity of citations on Hindi Wikipedia. Over time, external reference URLs cited in articles go offline (link rot). This bot scans reference sections, checks the HTTP status of external URLs, and replaces dead links with their archived counterparts retrieved from the **Wayback Machine (Archive.org)**.

### Core Functions

*   **Dead Link Verification:** Scans outgoing HTTP/HTTPS references within articles and flags links that return 404, 410, or DNS resolution failures.
*   **Wayback Machine Sync:** Queries the Internet Archive API to find the closest historical snapshot of the broken URL.
*   **Syntax Preservation:** Preserves existing templates (like `{{cite web}}` or standard wiki-markup) while safely injecting `|archive-url=` and `|archive-date=` parameters in Hindi.

---

## System Architecture

```text
hi-wiki-link-repairer/
├── .gitignore             # Shields local credentials and password files
├── requirements.txt       # Project dependencies
├── README.md              # Documentation
├── user-config.py         # Local Pywikibot configuration
├── user-password.py       # Secure BotPassword storage
└── link_repairer_bot.py   # Main engine performing reference scanning

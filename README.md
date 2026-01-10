# GitHub.io
# BPL74 Website

Static website for **bpl74.com**, hosted via GitHub Pages and served from the repository root using `index.html`.

This repository intentionally uses **plain HTML, CSS, and JavaScript** with no build step or framework.

---

## Project Structure

├── index.html # Main entry point
├── assets/ # CSS, JS, images, fonts
├── .vscode/ # VS Code tasks for local preview
├── .gitignore
└── README.md


---

## Local Development (Recommended)

### Requirements
- macOS
- Python 3 (preinstalled on macOS)
- Visual Studio Code

### Start Local Preview
From VS Code:

1. Press `Cmd + Shift + P`
2. Select **Tasks: Run Task**
3. Choose **Open preview in browser**

This starts a local server at:
http://localhost:8000/


Edit files and refresh the browser to see changes.

### Stop Local Preview
From VS Code:
1. `Cmd + Shift + P`
2. **Tasks: Run Task**
3. **Stop server on port 8000**

---

## Path Rules (Important)

Use **relative paths** so the site works both locally and when deployed via GitHub Pages.

✅ Correct:
```html
<link rel="stylesheet" href="assets/styles.css">
<script src="assets/main.js" defer></script>
<img src="assets/logo.png">

❌ Avoid root-relative paths:
<link rel="stylesheet" href="/assets/styles.css">

Root-relative paths can break depending on how the site is hosted.

Deployment

Deployment is automatic via GitHub Pages.

Deploy Steps
1.Stage your changes
2. Commit with a clear message
3. Push to the main branch

GitHub Pages publishes automatically after each push.

Repo Hygiene
1. macOS .DS_Store files are ignored
2. No build tools or package managers are used
3. Keep the repository clean and minimal

Contribution Guidelines
1. Keep changes simple and readable
2. Prefer plain HTML/CSS/JS
3. Avoid introducing frameworks or build steps unless explicitly required
4. Verify changes locally before pushing

Notes
This repo is designed to stay lightweight and easy to maintain.

If complexity increases, document any structural or tooling changes here.
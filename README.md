# SlopeScout Snowboarding Website

SlopeScout is a web application designed to provide snowboarders and skiers with real-time snow conditions, lift statuses, trail maps, and a personalized experience for various mountain resorts.

**Live Website:** www.slopescout.org (Note: This README helps you run a local instance, not deploy to this domain.)

## Features

* **Real-Time Resort Data:** Get up-to-the-minute snow reports, weather forecasts, and lift statuses.
* **Interactive Maps:** View detailed resort maps (external iframe).
* **Personalized Experience:** User account creation, login, and bookmarking favorite resorts.
* **Resort Exploration:** Discover different mountain resorts like Big Bear and Mammoth Mountain.
* **User Profile Management:** Update email, password, and delete account.
* **Automated Data Updates:** Firebase Cloud Functions periodically fetch and update resort data.

## Tech Stack

* **Frontend:**
    * HTML5
    * CSS3 (inline styles and global variables)
    * JavaScript (ES Modules)
    * Font Awesome (for icons, via CDN)
    * Firebase JS SDK (for Authentication, Firestore client-side)
* **Backend (Firebase):**
    * Firebase Authentication (Email/Password)
    * Firebase Firestore (NoSQL Database)
    * Firebase Cloud Functions (Python 3.11 runtime)
* **Python (Cloud Functions):**
    * `firebase-admin`: For server-side Firebase access.
    * `firebase_functions`: For defining Cloud Functions.
    * `requests`: For fetching data from external resort APIs.
    * `tzdata`: For timezone support.
* **Development & Build (Potential):**
    * Node.js & npm: For managing frontend packages and running scripts.
    * `framer-motion`: (Listed in `package.json`, usage not apparent in provided HTML)
    * `tailwindcss`, `postcss`, `autoprefixer`: (Listed in `devDependencies`, suggesting a potential CSS build step not fully detailed in the provided files. The current HTML primarily uses inline styles).
* **Deployment (Hinted):**
    * Vercel (suggested by `scripts/generate-firebase-config.js`)
    * Firebase Hosting (typically used with Firebase projects)

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

* **Git:** For cloning the repository.
* **Node.js and npm:** (Node.js version 16.x or higher recommended). Download from [nodejs.org](https://nodejs.org/).
* **Python 3.11 and pip:** Ensure Python 3.11 is installed and added to your PATH. Download from [python.org](https://www.python.org/downloads/release/python-3110/).
* **Firebase CLI:** Install globally using npm:
    ```bash
    npm install -g firebase-tools
    ```
    After installation, log in to Firebase:
    ```bash
    firebase login
    ```

## Project Setup

Follow these steps to set up the project locally:

**1. Clone the Repository:**

```bash
git clone <repository_url>
cd <repository_directory_name>

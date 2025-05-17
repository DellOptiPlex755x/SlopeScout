# SlopeScout Snowboarding Website

SlopeScout is a web application designed to provide snowboarders and skiers with real-time snow conditions, lift statuses, trail maps, and a personalized experience for various mountain resorts.

**Live Website:** www.slopescout.org (Note: We highly encourage anyone checking out our project to check out our live deployed website here. Installing and setting up all the packages and code dependecies will most likely take hours. Thank you!)

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
* **Development & Build:**
    * Node.js & npm: For managing frontend packages and running scripts.
    * `framer-motion`: For animations and transitions.
    * `tailwindcss`, `postcss`, `autoprefixer`: For CSS processing and utility-first styling.
* **Deployment:**
    * Vercel
    * Firebase Hosting

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

* **Git:** For cloning the repository. ([Download Git](https://git-scm.com/downloads))
* **Node.js and npm:** (Node.js version 16.x or higher recommended). This includes npm (Node Package Manager). ([Download Node.js](https://nodejs.org/))
* **Python 3.11 and pip:** Ensure Python 3.11 is installed and added to your system's PATH. pip (Python package installer) usually comes with Python. ([Download Python 3.11](https://www.python.org/downloads/release/python-3110/))
* **Firebase CLI:** Install globally using npm:
    ```bash
    npm install -g firebase-tools
    ```
    After installation, log in to Firebase using your Google account:
    ```bash
    firebase login
    ```

## Project Setup

Follow these steps to set up the project locally:

### 1. Clone the Repository:

If you haven't already, clone the repository to your local machine:
```bash
git clone <repository_url>
cd <repository_directory_name>
```
Replace `<repository_url>` with the actual URL of your GitHub repository and `<repository_directory_name>` with the name of the folder created by cloning.

### 2. Frontend Dependencies:

The project uses Node.js for managing frontend packages, primarily the Firebase client SDK and potentially some development tools. Navigate to the root directory of the cloned project (if you're not already there) and install the dependencies:
```bash
npm install
```
This command reads the package.json file and installs the libraries listed under dependencies (like firebase and framer-motion) and devDependencies (like tailwindcss). While firebase-admin is also listed and typically a backend dependency, npm install will handle it if it's in the root package.json.

### 3. Firebase Project Setup:

To run this application, you need to create your own Firebase project to handle authentication, database, and cloud functions.

#### Create a Firebase Project:
1. Go to the Firebase Console.
2. Click on "Add project".
3. Follow the on-screen instructions to create a new project (e.g., name it slopescout-local-dev).
4. You can choose to enable or disable Google Analytics for this project.

#### Register a Web App:
1. Once your project is created, you'll be taken to the project overview page.
2. In the center of the page, or in the Project Settings (gear icon near "Project Overview" > Your apps), click on the Web icon (</>) to add a web app.
3. Enter an "App nickname" (e.g., "SlopeScout Web Local").
4. Important: For now, do NOT check the box for "Also set up Firebase Hosting for this app" unless you specifically plan to deploy the frontend to Firebase Hosting later. You can always set it up later.
5. Click "Register app".
6. Firebase will then display an firebaseConfig object. Copy these configuration values carefully. You will need them in the next step. It will look something like this:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abcdef123456",
  measurementId: "G-XXXXXXXXXX" // This might be optional
};
```
7. Click "Continue to console" after copying the config.

#### Enable Authentication:
1. In the Firebase console, navigate to Build > Authentication from the left sidebar.
2. Click the "Get started" button.
3. Under the "Sign-in method" tab, select "Email/Password" from the list of providers.
4. Enable the "Email/Password" provider and click "Save".

#### Enable Firestore Database:
1. Navigate to Build > Firestore Database from the left sidebar.
2. Click the "Create database" button.
3. Choose "Start in test mode". This allows open read/write access for initial local development. Important: For a production application, you MUST configure proper security rules. The project includes assets/firebase/firestore.rules which will be deployed later.
4. Select a Cloud Firestore location. Choose a region that is geographically close to you or your intended users. This cannot be changed later.
5. Click "Enable".

### 4. Client-Side Firebase Configuration:

The project includes a script (scripts/generate-firebase-config.js) for dynamically creating the Firebase config during a Vercel build. For local development, create this configuration file manually.

1. Create a new file named config.js inside the assets/firebase/ directory.
2. Open assets/firebase/config.js and paste the following JavaScript code. Replace the placeholder values ("YOUR_API_KEY", "YOUR_PROJECT_ID", etc.) with the actual values from the firebaseConfig object you copied when you registered your web app in the Firebase console.

```javascript
// assets/firebase/config.js
// This file will be populated with actual values during the Vercel build process.
// For local development, manually insert your Firebase project's configuration.

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";

// Placeholder for Firebase configuration.
// The actual values will be injected by the Vercel build script
// using environment variables set in Vercel project settings.
// FOR LOCAL DEVELOPMENT: Replace these with your actual Firebase config values.
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID" // Include if you have it, otherwise remove or comment out
};

// Initialize Firebase
// This will cause an error if the placeholders above are not replaced during build.
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Export Firebase services
export { app, auth, db };
```

Ensure all placeholder values are correctly replaced. If you don't have a measurementId from Firebase, you can comment out or remove that line.

### 5. Firebase Backend (Cloud Functions & Rules):

This section involves setting up the backend components that run on Firebase servers.

#### Configure Firebase CLI for Your Project:
In your terminal, from the root directory of the cloned project, run:
```bash
firebase use --add
```
This command will list the Firebase projects associated with your logged-in Google account. Select the Firebase project you created in step 3. This will update the .firebaserc file (or create one if it doesn't exist) to link your local project directory with your Firebase project.

#### Set up Python Virtual Environment for Functions:
The Cloud Functions for this project are written in Python. It's best practice to use a virtual environment.

1. Navigate to the functions directory:
```bash
cd functions
```

2. Create a Python virtual environment (ensure you are using Python 3.11 as specified in firebase.json):
```bash
python3.11 -m venv venv
```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows (Git Bash or similar):
     ```bash
     source venv/Scripts/activate
     ```
   - On Windows (Command Prompt/PowerShell):
     ```bash
     .\venv\Scripts\activate
     ```
   You should see (venv) prefixed to your terminal prompt.

4. Install the Python dependencies listed in functions/requirements.txt:
```bash
pip install -r requirements.txt
```

5. Once the dependencies are installed, navigate back to the root project directory:
```bash
cd ..
```

You can deactivate the virtual environment later if needed (`deactivate`), but it's often useful to keep it active if you plan to work more with the functions locally.

#### Deploy Firestore Rules and Indexes:
The project defines Firestore security rules in assets/firebase/firestore.rules and index configurations in assets/firebase/firestore.indexes.json. To deploy these to your Firebase project:

From the root project directory, run:
```bash
firebase deploy --only firestore:rules,firestore:indexes
```

#### Deploy Firebase Cloud Functions:
The Cloud Function defined in functions/main.py is responsible for periodically fetching resort data and updating Firestore. This function is scheduled to run automatically. To deploy it:

From the root project directory, run:
```bash
firebase deploy --only functions
```

This process might take a few minutes. It will upload your function code and configure its trigger (a scheduled task to run every 5 minutes, as defined in functions/main.py and firebase.json).

## Running the Application Locally (Client-Side)

Once the setup is complete, you can run the website's frontend. Because this project primarily consists of static HTML, CSS (inline), and client-side JavaScript files, you have a couple of options:

### Option 1: Open index.html Directly in Browser
1. Navigate to the root of your project directory in your computer's file explorer.
2. Double-click on the index.html file. This will open the main page in your default web browser.

### Option 2: Use a Local Development Server (Recommended)
Using a local development server can provide a more robust experience, including features like live reloading.

**VS Code Live Server Extension:** If you are using Visual Studio Code, a popular choice is the "Live Server" extension by Ritwick Dey.
1. Install the extension from the VS Code Marketplace.
2. Open your project folder in VS Code.
3. Right-click on index.html in the VS Code explorer and select "Open with Live Server".

**Other HTTP Servers:** You can use any simple HTTP server. For example, if you have Python installed, you can run:
```bash
# Make sure you are in the root project directory
python -m http.server
```
Then open http://localhost:8000 (or the port specified) in your browser. If you have Node.js, you can use `npx serve`.

### Important Notes on Local Functionality:
- **Authentication and Bookmarking:** User signup, login, profile management, and bookmarking features should work correctly as they interact directly with the Firebase Authentication and Firestore services you configured.
- **Resort Data (Weather, Lifts):**
  - When you first run the application, the sections displaying resort-specific data (like weather and lift statuses on the Big Bear or Mammoth pages) might show "Loading..." or be empty.
  - This data is populated by the `update_resort_data_in_firestore` Firebase Cloud Function. This function needs to be deployed (as per step 5) and then run at least once.
  - It is scheduled to run every 5 minutes. You can either wait for its scheduled execution or manually trigger it:
    1. Go to the Firebase Console.
    2. Navigate to Build > Functions.
    3. Find the `update_resort_data_in_firestore` function (or a similar name based on your deployment) in the list.
    4. You might be able to trigger it from the "Testing" tab within the function's details, or you might need to wait for the scheduler. The optional `manually_trigger_data_update` HTTP function in functions/main.py (currently commented out) could also be deployed and used for this if uncommented.
  - Once the function runs successfully, it will populate the `resort_conditions` collection in your Firestore database, and the website will display the data.

## Project Structure Overview
```
├── README.md                   # This file
├── default.html                # Redirects to index.html
├── firebase.json               # Firebase deployment configuration
├── index.html                  # Main landing page of the website
├── package.json                # Node.js project metadata and dependencies
├── .firebaserc                 # Firebase project association
├── assets/
│   ├── css/
│   │   └── styles.css          # Global CSS file (currently not linked in HTML)
│   ├── firebase/
│   │   ├── config.js           # Firebase client configuration
│   │   ├── firestore.indexes.json # Firestore index definitions
│   │   └── firestore.rules     # Firestore security rules
│   ├── images/                 # Contains logos, background images, etc.
│   │   ├── bigBearLogo.svg
│   │   ├── mammothMountainLogo.svg
│   │   ├── mountainImage.jpg
│   │   └── slopelift.png
│   └── pages/                  # Contains other HTML pages for different sections
│       ├── bigbear.html
│       ├── bookmarks.html
│       ├── explore.html
│       ├── mammoth.html
│       ├── profile.html
│       └── sign-up_login.html
├── functions/                  # Backend Firebase Cloud Functions
│   ├── .gitignore              # Specifies files to be ignored by Git in functions
│   ├── main.py                 # Main Python Cloud Function for data updates
│   ├── pyResort.py             # Helper Python script for API interaction
│   └── requirements.txt        # Python dependencies for Cloud Functions
└── scripts/                    # Helper scripts (e.g., for deployment)
    └── generate-firebase-config.js # Script for Vercel Firebase config generation
```

## Important Considerations

### API Keys in pyResort.py:
The pyResort.py file contains bearer_token values for the BIGBEAR_API_URL and MAMMOTH_API_URL. These tokens are used to authenticate with the external resort data API.
- These tokens might be rate-limited or specific to a certain account/period.
- If the data fetching fails (e.g., resort data not updating), these tokens could be a reason (expired, invalid, or rate-limited).
- For production, consider storing sensitive API keys securely as environment variables for Cloud Functions or using a secret manager.

### Environment Variables for Client Config (Vercel):
The scripts/generate-firebase-config.js file is designed for a CI/CD environment like Vercel, where Firebase client configuration keys are set as Vercel environment variables (e.g., FIREBASE_API_KEY, FIREBASE_PROJECT_ID). For local development, manually create the assets/firebase/config.js file as outlined in the setup instructions.

### Tailwind CSS & Build Process:
The package.json lists tailwindcss, postcss, and autoprefixer as devDependencies. To use or expand upon Tailwind CSS styling, you would typically need to:
1. Create a Tailwind configuration file (tailwind.config.js).
2. Have a main CSS input file (e.g., src/input.css) where you import Tailwind directives.
3. Run a Tailwind build process (e.g., npx tailwindcss -i ./src/input.css -o ./assets/css/tailwind-output.css --watch) to generate an output CSS file.
4. Link this generated output CSS file in your HTML <head> sections.

The assets/css/styles.css file exists for global styling.

### Firestore Data Structure:
The application relies on a specific structure in the Firestore database. The update_resort_data_in_firestore Cloud Function populates the resort_conditions collection. Each document in this collection corresponds to a resort or lodge (e.g., a document named snow-valley, another named bear-mountain, main-lodge for Mammoth's Main Lodge, etc.), and these documents contain the lift status and weather data.

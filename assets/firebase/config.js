// assets/firebase/config.js
// This file will be populated with actual values during the Vercel build process.

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-firestore.js";

// Placeholder for Firebase configuration.
// The actual values will be injected by the Vercel build script
// using environment variables set in Vercel project settings.
const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID
    // measurementId: process.env.FIREBASE_MEASUREMENT_ID // Uncomment if you use it
};

// Initialize Firebase
// This will cause an error if the placeholders above are not replaced during build.
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Export Firebase services
export { app, auth, db };

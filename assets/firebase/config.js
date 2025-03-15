// assets/firebase/config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";

// Your Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDtab2UItTMNgJPk42z7MlbkoR2x-7ovmE",
    authDomain: "slopescout-f317c.firebaseapp.com",
    projectId: "slopescout-f317c",
    storageBucket: "slopescout-f317c.appspot.com",
    messagingSenderId: "207517239405",
    appId: "1:207517239405:web:b83a8b6acef55ff7d29764"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { app, auth };

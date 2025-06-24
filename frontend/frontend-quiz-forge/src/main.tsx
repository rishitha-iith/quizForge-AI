import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { Toaster } from "@/components/ui/sonner"; // 👈 Import this (after step 3 setup below)
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
    <Toaster position="bottom-right" richColors closeButton /> {/* 👈 Add this line */}
  </React.StrictMode>
);

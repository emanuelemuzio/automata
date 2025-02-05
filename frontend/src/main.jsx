import React from "react";
import ReactDOM from "react-dom/client";
import AppRoutes from "./routes";
import "./styles/variables.css"; // Import del tema chiaro/scuro
import "./styles/index.css"; // Import degli stili globali

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AppRoutes />
  </React.StrictMode>
);

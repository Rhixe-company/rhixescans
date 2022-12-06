import React from "react";
import { Provider } from "react-redux";
import store from "./store";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./assets/main.css";
import App from "./App";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
  <Provider store={store}>
    <main>
      <App />
    </main>
  </Provider>
);

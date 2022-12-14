import React from "react";
import { Provider } from "react-redux";
import store from "./store";
import { createRoot } from "react-dom/client";

import "./assets/main.css";
import "./index.css";
import "./custom.scss";
import App from "./App";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);

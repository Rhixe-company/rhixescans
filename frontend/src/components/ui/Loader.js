import React from "react";
import { Spinner } from "react-bootstrap";
import spinner from "../../img/spinner.gif";
function Loader() {
  return (
    <Spinner
      animation="border"
      role="status"
      style={{
        height: "100px",
        width: "100px",
        margin: "auto",
        display: "block",
      }}
    >
      <img src={spinner} className="w-full" alt="Loading" />
    </Spinner>
  );
}

export default Loader;

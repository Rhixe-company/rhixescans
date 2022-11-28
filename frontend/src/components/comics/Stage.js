import React, { Fragment } from "react";
import Comics from "./Comics";
import ComicsForm from "./ComicsForm";

export default function Stage() {
  return (
    <Fragment>
      <ComicsForm />
      <Comics />
    </Fragment>
  );
}

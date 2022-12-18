import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";
import { useHistory } from "react-router-dom";

function SearchBox() {
  const [keyword, setKeyword] = useState("");

  let history = useHistory();

  const submitHandler = (e) => {
    e.preventDefault();
    if (keyword) {
      history.push(`?keyword=${keyword}&page=1`);
    } else {
      history.push(history.push(history.location.pathname));
    }
  };
  return (
    <Form onSubmit={submitHandler} inline>
      <Form.Control
        type="text"
        name="q"
        onChange={(e) => setKeyword(e.target.value)}
        className="border-none w-full mr-3 py-1 px-2 "
      ></Form.Control>

      <Button
        type="submit"
        variant="outline-success"
        className="text-sm border-4 text-white py-1px-2 rounded"
      >
        Search
      </Button>
    </Form>
  );
}

export default SearchBox;

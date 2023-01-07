import React, { useState } from "react";
import { Form, Button } from "react-bootstrap";
import FormContainer from "../ui/FormContainer";

const ChapterForm = ({ createChapterHandler }) => {
  const [name, setName] = useState("");
  const [number, setNumber] = useState(0);
  return (
    <div>
      <FormContainer>
        <Form onSubmit={createChapterHandler}>
          <Form.Group controlId="name">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            ></Form.Control>
          </Form.Group>

          <Form.Group controlId="price">
            <Form.Label>Number</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter number"
              value={number}
              onChange={(e) => setNumber(e.target.value)}
            ></Form.Control>
          </Form.Group>
          <Button type="submit" variant="primary">
            Submit
          </Button>
        </Form>
      </FormContainer>
    </div>
  );
};

export default ChapterForm;

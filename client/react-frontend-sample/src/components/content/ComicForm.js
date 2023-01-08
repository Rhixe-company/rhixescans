import React from "react";
import { Button } from "react-bootstrap";

import { useDispatch } from "react-redux";
import { createComic } from "../../features/comics/comicSlice";
const ComicForm = () => {
  const dispatch = useDispatch();

  const onSubmit = (e) => {
    e.preventDefault();
    dispatch(createComic());
  };

  return (
    <div>
      <Button className="my-3" onClick={onSubmit}>
        <i className="fas fa-plus"></i> Create Comic
      </Button>
    </div>
  );
};

export default ComicForm;

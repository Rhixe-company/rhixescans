import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import { Form, Button } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/ui/Loader";
import Message from "../components/ui/Message";
import FormContainer from "../components/ui/FormContainer";
import { listComicsDetails, updateComic } from "../actions/comicsActions";
import { COMICS_UPDATE_RESET } from "../constants/comicsConstants";

const ComicsEditScreen = ({ match, history }) => {
  const comicId = match.params.id;

  const [title, setTitle] = useState("");
  const [rating, setRating] = useState(0);
  const [image_url, setImage_url] = useState("");
  const [status, setStatus] = useState("");
  const [author, setAuthor] = useState("");
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [uploading, setUploading] = useState(false);

  const dispatch = useDispatch();

  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { error, loading, comic } = comicsDetails;

  const comicUpdate = useSelector((state) => state.comicUpdate);
  const {
    error: errorUpdate,
    loading: loadingUpdate,
    success: successUpdate,
  } = comicUpdate;

  useEffect(() => {
    if (successUpdate) {
      dispatch({ type: COMICS_UPDATE_RESET });
      history.push("/admin/comics");
    } else {
      if (!comic.title || comic.id !== Number(comicId)) {
        dispatch(listComicsDetails(comicId));
      } else {
        setTitle(comic.title);
        setRating(comic.rating);
        setImage_url(comic.image_url);
        setStatus(comic.status);
        setAuthor(comic.author);
        setDescription(comic.description);

        setCategory(comic.category);
      }
    }
  }, [dispatch, comic, comicId, history, successUpdate]);

  const submitHandler = (e) => {
    e.preventDefault();
    dispatch(
      updateComic({
        id: comicId,
        title,
        image_url,
        description,
        rating,
        status,
        category,
        author,
      })
    );
  };
  const uploadFileHandler = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();

    formData.append("image", file);
    formData.append("comicId", comicId);

    setUploading(true);

    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };

      const { data } = await axios.post(
        "/api/comics/upload/",
        formData,
        config
      );

      setImage_url(data);
      setUploading(false);
    } catch (error) {
      setUploading(false);
    }
  };
  return (
    <div>
      <h1>ComicsEditScreen</h1>
      <div>
        <Link to="/admin/comics">
          <Button className="my-3">Go Back</Button>
        </Link>
      </div>
      <div>
        <FormContainer>
          <h1>Edit Comic</h1>
          {loadingUpdate && <Loader />}
          {errorUpdate && <Message variant="danger">{errorUpdate}</Message>}

          {loading ? (
            <Loader />
          ) : error ? (
            <Message variant="danger">{error}</Message>
          ) : (
            <Form onSubmit={submitHandler}>
              <Form.Group controlId="name">
                <Form.Label>Title</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Form.Group controlId="image">
                <Form.Label>Image</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter image"
                  value={image_url}
                  onChange={(e) => setImage_url(e.target.value)}
                ></Form.Control>
                <Form.File
                  id="image-file"
                  label="Choose File"
                  custom
                  onChange={uploadFileHandler}
                ></Form.File>
                {uploading && <Loader />}
              </Form.Group>
              <Form.Group controlId="description">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  type="textarea"
                  placeholder="Enter description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Form.Group controlId="price">
                <Form.Label>Rating</Form.Label>
                <Form.Control
                  type="number"
                  placeholder="Enter rating"
                  value={rating}
                  onChange={(e) => setRating(e.target.value)}
                ></Form.Control>
              </Form.Group>

              <Form.Group controlId="status">
                <Form.Label>status</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter status"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Form.Group controlId="category">
                <Form.Label>category</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Form.Group controlId="author">
                <Form.Label>Author</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter author"
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                ></Form.Control>
              </Form.Group>
              <Button type="submit" variant="primary">
                Update
              </Button>
            </Form>
          )}
        </FormContainer>
      </div>
    </div>
  );
};

export default ComicsEditScreen;

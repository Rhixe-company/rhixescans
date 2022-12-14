import React, { useEffect } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Link } from "react-router-dom";
import { Button, Table, Container, Image } from "react-bootstrap";

import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/ui/Loader";
import Message from "../components/ui/Message";
import Paginate from "../components/ui/Paginate";
import ComicForm from "../components/content/ComicForm";

import {
  listComics,
  deleteComic,
  createComic,
  loadComics,
} from "../actions/comicsActions";
import { COMICS_CREATE_RESET } from "../constants/comicsConstants";

const ComicsListScreen = ({ history }) => {
  const dispatch = useDispatch();

  const comicsList = useSelector((state) => state.comicsList);
  const { loading, error, comics, pages, page, comics_count } = comicsList;

  const comicDelete = useSelector((state) => state.comicDelete);
  const {
    loading: loadingDelete,
    error: errorDelete,
    success: successDelete,
  } = comicDelete;

  const comicCreate = useSelector((state) => state.comicCreate);
  const {
    loading: loadingCreate,
    error: errorCreate,
    success: successCreate,
    comic: createdComic,
  } = comicCreate;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch({ type: COMICS_CREATE_RESET });

    if (!userInfo || !userInfo.isAdmin) {
      history.push("/login");
    }

    if (successCreate) {
      history.push(`/admin/comic/${createdComic.id}/edit`);
    } else {
      dispatch(listComics(keyword));
    }
  }, [
    dispatch,
    history,
    userInfo,
    successDelete,
    successCreate,
    createdComic,
    keyword,
  ]);

  const deleteHandler = (id) => {
    if (window.confirm("Are you sure you want to delete this comic?")) {
      dispatch(deleteComic(id));
    }
  };

  const createComicHandler = () => {
    dispatch(createComic());
  };

  const createComicsHandler = () => {
    dispatch(loadComics());
  };

  return (
    <Container>
      {loadingDelete && <Loader />}
      {errorDelete && <Message variant="danger">{errorDelete}</Message>}

      {loadingCreate && <Loader />}
      {errorCreate && <Message variant="danger">{errorCreate}</Message>}

      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          <Button onClick={createComicsHandler}>Loadcomics</Button>
          <ComicForm createComicHandler={createComicHandler} />
          <strong>{comics_count} comics available</strong>
          <Table striped bordered hover size="sm" responsive="sm">
            <thead>
              <tr>
                <th>TITLE</th>
                <th>IMAGE</th>
                <th>CATEGORY</th>
                <th>RATING</th>
                <th>STATUS</th>
                <th>AUTHOR</th>
                <th />
                <th />
              </tr>
            </thead>

            <tbody>
              {comics.map((comic) => (
                <>
                  <tr key={comic.id}>
                    <td>
                      <Link to={`/comic/${comic.id}/`}>{comic.title}</Link>
                    </td>
                    <td>
                      <Link to={`/comic/${comic.id}/`}>
                        <Image src={comic.image} alt={comic.image_url} />
                      </Link>
                    </td>
                    <td>{comic.rating}</td>
                    <td>{comic.category}</td>
                    <td>{comic.status}</td>
                    <td>{comic.author}</td>
                    <td>
                      <LinkContainer to={`/admin/comic/${comic.id}/edit`}>
                        <Button variant="light" className="btn-sm">
                          <i className="fas fa-edit">Edit</i>
                        </Button>
                      </LinkContainer>
                    </td>
                    <td>
                      <Button
                        variant="danger"
                        className="btn-sm"
                        onClick={() => deleteHandler(comic.id)}
                      >
                        <i className="fas fa-trash">Delete</i>
                      </Button>
                    </td>
                  </tr>
                </>
              ))}
            </tbody>
          </Table>
          <Paginate pages={pages} page={page} isAdmin={true} />
        </div>
      )}
    </Container>
  );
};

export default ComicsListScreen;

import React, { useEffect } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { Table, Button } from "react-bootstrap";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import Loader from "../components/ui/Loader";
import Message from "../components/ui/Message";
import Paginate from "../components/ui/Paginate";
import ChapterForm from "../components/content/ChapterForm";
import {
  listChapters,
  deleteChapter,
  createChapter,
} from "../actions/chaptersActions";
import { CHAPTERS_CREATE_RESET } from "../constants/chaptersConstants";

const ChaptersListScreen = ({ history }) => {
  const dispatch = useDispatch();

  const chaptersList = useSelector((state) => state.chaptersList);
  const { loading, error, chapters, page, pages } = chaptersList;

  const chapterDelete = useSelector((state) => state.chapterDelete);
  const {
    loading: loadingDelete,
    error: errorDelete,
    success: successDelete,
  } = chapterDelete;

  const chapterCreate = useSelector((state) => state.chapterCreate);
  const {
    loading: loadingCreate,
    error: errorCreate,
    success: successCreate,
    comic: createdChapter,
  } = chapterCreate;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch({ type: CHAPTERS_CREATE_RESET });

    if (!userInfo.isAdmin) {
      history.push("/login");
    }

    if (successCreate) {
      history.push(`/admin/chapters/${createdChapter.id}/edit`);
    } else {
      dispatch(listChapters(keyword));
    }
  }, [
    dispatch,
    history,
    userInfo,
    successDelete,
    successCreate,
    createdChapter,
    keyword,
  ]);

  const deleteHandler = (id) => {
    if (window.confirm("Are you sure you want to delete this chapter?")) {
      dispatch(deleteChapter(id));
    }
  };

  const createChapterHandler = () => {
    dispatch(createChapter());
  };

  return (
    <div>
      <div>
        <ChapterForm createChapterHandler={createChapterHandler} />
      </div>
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
          <Table striped bordered hover responsive className="table-sm">
            <thead>
              <tr>
                <th>Name</th>

                <th></th>
              </tr>
            </thead>

            <tbody>
              {chapters.map((chapter) => (
                <tr key={chapter.id}>
                  <td>
                    <Link to={`/comics/chapter/${chapter.id}/`}>
                      <span>{chapter.name}</span>
                    </Link>
                  </td>

                  <td>
                    <LinkContainer to={`/admin/chapter/${chapter.id}/edit`}>
                      <Button variant="light" className="btn-sm">
                        <i className="fas fa-edit">Edit</i>
                      </Button>
                    </LinkContainer>

                    <Button
                      variant="danger"
                      className="btn-sm"
                      onClick={() => deleteHandler(chapter.id)}
                    >
                      <i className="fas fa-trash">Delete</i>
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
          <Paginate pages={pages} page={page} />
        </div>
      )}
    </div>
  );
};

export default ChaptersListScreen;

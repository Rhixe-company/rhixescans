import React, { useEffect } from "react";
import { LinkContainer } from "react-router-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Button, Nav } from "react-bootstrap";
import { Link } from "react-router-dom";
import Loader from "../ui/Loader";
import Message from "../ui/Message";

import { listChaptersDetails } from "../../actions/chaptersActions";

const Chapters = ({ match }) => {
  const chapterId = match.params.id;
  const dispatch = useDispatch();
  const chaptersDetails = useSelector((state) => state.chaptersDetails);
  const { error, loading, chapter } = chaptersDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    if (!chapter.name || chapter.id !== Number(chapterId)) {
      dispatch(listChaptersDetails(chapterId));
    }
  }, [dispatch, chapter, chapterId]);
  return (
    <div>
      <div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <div>
            <Link to="/">
              <Button>Go Back </Button>
            </Link>

            <div>
              <div>
                {userInfo ? (
                  <div>{chapter.name}</div>
                ) : (
                  <LinkContainer to="/login">
                    <Nav.Link>
                      <i className="fas fa-user"></i>Login
                    </Nav.Link>
                  </LinkContainer>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Chapters;

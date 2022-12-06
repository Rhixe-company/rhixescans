import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { listComicsDetails } from "../actions/comicsActions";
import Comicgrid from "../components/content/Comicgrid";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";
import { Link } from "react-router-dom";
import { Button, Container } from "react-bootstrap";

export const ComicScreen = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic, error, loading } = comicsDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  useEffect(() => {
    dispatch(listComicsDetails(comicId));
  }, [dispatch, comicId]);
  return (
    <Container>
      <div>
        {loading ? (
          <Loader />
        ) : error ? (
          <Message variant="danger">{error}</Message>
        ) : (
          <div>
            {userInfo ? (
              <div>
                <Comicgrid comic={comic} />
                <Link to="/">
                  <Button>Go Back Home</Button>
                </Link>
              </div>
            ) : (
              <Link to="/login">
                <Button>Please Login To Read Comic</Button>
              </Link>
            )}
          </div>
        )}
      </div>
    </Container>
  );
};

const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
});

export default connect(mapStateToProps, {
  listComicsDetails,
})(ComicScreen);

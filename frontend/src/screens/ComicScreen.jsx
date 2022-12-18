import React, { useEffect } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import PropTypes from "prop-types";
import { listComicsDetails } from "../actions/comicsActions";
import Comicgrid from "../components/content/Comicgrid";
import Message from "../components/ui/Message";
import Loader from "../components/ui/Loader";

import { Container } from "react-bootstrap";

export const ComicScreen = ({ history, match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { comic, chapters, error, loading } = comicsDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  useEffect(() => {
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(listComicsDetails(comicId));
  }, [history, userInfo, dispatch, comicId]);
  return (
    <section>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <Container>
          <Comicgrid comic={comic} chapters={chapters} />
        </Container>
      )}
    </section>
  );
};

ComicScreen.propTypes = {
  listComicsDetails: PropTypes.func.isRequired,
};
const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
  chapters: state.comicsDetails.chapters,
});

export default connect(mapStateToProps, {
  listComicsDetails,
})(ComicScreen);

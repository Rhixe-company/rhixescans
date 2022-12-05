import PropTypes from "prop-types";
import React, { useEffect, useState } from "react";
import { connect, useDispatch, useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { listComicsDetails } from "../actions/comicsActions";
import Loader from "../components/ui/Loader";
import Comicgrid from "../components/ui/Comicgrid";
import { Button } from "react-bootstrap";
import Message from "../components/ui/Message";

export const Comic = ({ match }) => {
  const comicId = match.params.id;
  const dispatch = useDispatch();
  const comicsDetails = useSelector((state) => state.comicsDetails);
  const { error, loading, comic } = comicsDetails;
  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;
  const [chapters, setChapters] = useState([]);
  const [isloading, setisLoading] = useState(true);

  useEffect(() => {
    dispatch(listComicsDetails(comicId));
    fetch(`api/comics/${comicId}/chapters/`)
      .then((res) => res.json())
      .then((data) => {
        setChapters(data.chapters);
        setisLoading(false);
      })
      .catch((err) => console.log(err));
  }, [dispatch, comicId]);
  return (
    <div>
      {loading ? (
        <Loader />
      ) : error ? (
        <Message variant="danger">{error}</Message>
      ) : (
        <div>
          {userInfo ? (
            <div>
              <Link to="/">
                <Button>Go Back </Button>
              </Link>
              <div>
                <Comicgrid comic={comic} />
              </div>
              <br />
              {!isloading && chapters.length === 0 && (
                <small>No Chapters Found</small>
              )}
              {isloading ? (
                <Loader />
              ) : (
                <div>
                  <h3>Recent Chapters</h3>
                  {chapters.map((chapter) => (
                    <ul key={chapter.id}>
                      <li>
                        <Link to={`/comics/chapter/${chapter.id}/`}>
                          <span>{chapter?.name}</span>
                        </Link>
                        <hr />
                      </li>
                    </ul>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div>
              <Link to="/login">
                <Button>Please Login To Read Comic</Button>
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

Comic.propTypes = {
  listComicsDetails: PropTypes.func.isRequired,
};

const mapStateToProps = (state) => ({
  comic: state.comicsDetails.comic,
});

export default connect(mapStateToProps, {
  listComicsDetails,
})(Comic);

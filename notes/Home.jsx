import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import ComicForm from "../components/content/ComicForm";
import Loader from "../components/ui/Loader";
import { getComics, reset } from "../features/comics/comicSlice";
import ComicItem from "../components/ComicItem";
const Home = ({ history }) => {
  const dispatch = useDispatch();
  const { userInfo } = useSelector((state) => state.userLogin);
  const { comics, count, page, pages, isError, isLoading, message } =
    useSelector((state) => state.comics);
  useEffect(() => {
    if (isError) {
      console.log(message);
    }
    if (!userInfo) {
      history.push("/login");
    }
    dispatch(getComics());
    return () => {
      dispatch(reset());
    };
  }, [dispatch, history, isError, message, userInfo]);
  if (isLoading) {
    return <Loader />;
  }
  return (
    <>
      <section className="heading">
        <h1>Welcome {userInfo && userInfo.name}</h1>
        <p>{count} comics available</p>

        <ComicForm />
      </section>

      <section className="content">
        {comics.length > 0 ? (
          <div className="comics">
            {comics.map((comic) => (
              <ComicItem key={comic.id} comic={comic} />
            ))}
          </div>
        ) : (
          <h3>You Have No Comics</h3>
        )}
      </section>
    </>
  );
};

export default Home;

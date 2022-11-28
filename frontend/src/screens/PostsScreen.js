import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Posts from "../components/content/Posts";

import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics } from "../actions/comicsActions";

function PostsScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { page, pages } = comicsList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <div className="container mx-auto">
      <br />
      {!keyword && <ComicsCarousel />}

      <div>
        <div>
          <Posts />
          <hr />
        </div>

        <Paginate page={page} pages={pages} keyword={keyword} />
      </div>
    </div>
  );
}

export default PostsScreen;

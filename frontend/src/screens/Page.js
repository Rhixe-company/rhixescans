import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Posts from "../components/Posts";
import Pagination from "../components/Pagination";
import { listComics } from "../actions/comicsActions";
const Page = () => {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { loading, error, comics } = comicsList;
  const [currentPage, setCurrentPage] = useState(1);
  const [postsPerPage] = useState(10);
  useEffect(() => {
    dispatch(listComics());
  }, [dispatch]);

  // Get current posts
  const indexOfLastPost = currentPage * postsPerPage;
  const indexOfFirstPost = indexOfLastPost - postsPerPage;
  const currentPosts = comics.slice(indexOfFirstPost, indexOfLastPost);
  // Chage page
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  return (
    <div>
      <Posts posts={currentPosts} loading={loading} error={error} />
      <Pagination
        postsPerPage={postsPerPage}
        totalPosts={comics.length}
        paginate={paginate}
      />
    </div>
  );
};

export default Page;

import React from "react";
import Loader from "./ui/Loader";
const Posts = ({ posts, loading }) => {
  if (loading) {
    return <Loader />;
  }
  return (
    <ul className="list-group mb-4">
      {posts.map((post) => (
        <li key={post.id} className="list-group-item">
          <img src={post.image} alt="" />
          {post.title}
        </li>
      ))}
    </ul>
  );
};

export default Posts;

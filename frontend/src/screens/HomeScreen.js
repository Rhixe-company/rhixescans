import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Rating from "../components/ui/Rating";
import { Link } from "react-router-dom";
import { Card } from "react-bootstrap";
import Paginate from "../components/ui/Paginate";
import ComicsCarousel from "../components/content/ComicsCarousel";
import { listComics } from "../actions/comicsActions";

function PostsScreen({ history }) {
  const dispatch = useDispatch();
  const comicsList = useSelector((state) => state.comicsList);
  const { comics, page, pages } = comicsList;

  let keyword = history.location.search;

  useEffect(() => {
    dispatch(listComics(keyword));
  }, [dispatch, keyword]);
  return (
    <section className="container mx-auto">
      {!keyword && <ComicsCarousel />}
      <br />
      <h1>Latest Comics</h1>
      <div>
        {comics.map((comic) => (
          <div key={comic.id}>
            <Card className="my-3 p-3 rounded">
              <Card.Body className="px-6 py-4">
                <Link to={`/comic/${comic.id}/`}>
                  <Card.Title
                    as="div"
                    className="font-bold text-black-500 text-xl mb-2"
                  >
                    <h5>{comic.title}</h5>
                  </Card.Title>
                </Link>
                <Link to={`/comic/${comic.id}/`}>
                  <Card.Img src={comic.image} alt="" className="w-full" />
                </Link>

                <Card.Text as="div">
                  <div className="my-3">
                    <Rating
                      value={comic.rating}
                      text={`${comic.rating} `}
                      color={"#f8e825"}
                    />
                  </div>
                </Card.Text>
                <Card.Text as="span">{comic.status}</Card.Text>
                <br />
                <Card.Text as="span">{comic.category}</Card.Text>
                <br />
                {comic.genres.map((genre) => (
                  <Card.Text
                    as="span"
                    key={genre.id}
                    className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
                  >
                    {genre.name}
                  </Card.Text>
                ))}
              </Card.Body>
              <br />

              {comic.chapters.map((chapter) => (
                <div key={chapter.id}>
                  <Link to={`/comics/chapter/${chapter.id}/`}>
                    <small>{chapter?.name}</small>
                  </Link>
                </div>
              ))}
            </Card>
          </div>
        ))}

        <Paginate page={page} pages={pages} keyword={keyword} />
      </div>
    </section>
  );
}

export default PostsScreen;

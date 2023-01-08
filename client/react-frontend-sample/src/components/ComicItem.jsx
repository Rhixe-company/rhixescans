import { useDispatch } from "react-redux";
import { deleteComic } from "../features/comics/comicSlice";

function ComicItem({ comic }) {
  const dispatch = useDispatch();
  return (
    <div className="comic">
      <div className="">
        <h2>{comic.title}</h2>
        <img src={comic.image} alt={comic.image_url} />
        {new Date(comic.created).toLocaleString("en-us")}
        <button
          className="close"
          onClick={() => dispatch(deleteComic(comic.id))}
        >
          <i className="fas fa-trash">Delete</i>
        </button>
      </div>
    </div>
  );
}

export default ComicItem;

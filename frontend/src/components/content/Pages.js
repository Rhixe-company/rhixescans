import { Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";
const Pages = ({ page }) => {
  return (
    <InfiniteScroll dataLength={page} key={page.id}>
      <Image src={page.images} alt={page.images_url} />
    </InfiniteScroll>
  );
};

export default Pages;

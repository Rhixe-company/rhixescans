import { Image } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";
const Pages = ({ page }) => {
  return (
    <InfiniteScroll dataLength={page}>
      <Image src={page.images} alt={page.images} />
    </InfiniteScroll>
  );
};

export default Pages;

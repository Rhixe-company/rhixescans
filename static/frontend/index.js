console.log('working');
const comicDisplay = document.querySelector("#comics-area");
const pageDisplay = document.querySelector("#pagg");
fetch("http://127.0.0.1:8000/api/comics/")
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    // Get Comics And Display Them
    data.comics.forEach((article) => {
      const articleItem = `<div class="card mb-4 box-shadow">
        <img class="card-img-top" src=${article.image} alt=${article.image}/>
        <div class="card-body">
          <h2>
            ${article.title}
          </h2>
          <p class="card-text">${article.description}</p>
        </div>
      </div>`;
      comicDisplay.insertAdjacentHTML("beforeend", articleItem);
    });
    // Get Pages And Display Them
    for (i = 0; i < data.pages; i++) {
      const pages = [i];
      pageItem = `<a class="page-link" href='/?page=${pages}'">
        ${pages}
      </a>`;
      pageDisplay.insertAdjacentHTML("beforeend", pageItem);
    }
  })
  .catch((err) => console.log(err));

//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}


// Anime Smooth Scroll
$("#view-chapter").on('click', function () {
  const images = $('#images').position().top
  $('html, body').animate({
    screenTop: images
  }, 900)
});

$(document).on("keyup", "#id_q", function (e) {
  e.preventDefault();

  var minlength = 4;
  var results = [];

  if ($("#id_q").val().length >= minlength) {
    $.ajax({
      type: "POST",
      url: "/search/",
      data: {
        ss: $("#id_q").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        action: "post",
      },
      success: function (json) {
        $.each(JSON.parse(json.search_string), (i, item) => {
          results.push(
            `
            <li role="presentation" class="list-group-item bg-white">
            <a class='text-white' href='/comic/ ${item.pk} /'>
            <img width="100"
                height="100" class="img-thumbnail rounded d-block" src='/media/${item.fields.image}' alt='/media/${item.fields.image}'/>
                </a>
            <div class='text-white'><a href='/comic/ ${item.pk} /'>
            
            <h2 class="comic-title text-white">${item.fields.title}</h2>
            
            </a></div>
             <small class='text-white'>${item.fields.status}</small>
            <span class='text-white'>${item.fields.category}</span>
            </li>
            `
          );
        });

        if (!$(".show")[0]) {
          $(".menudd").trigger("click");
        }
        document.getElementById("list").className = "show";
        document.getElementById("list").innerHTML = !results.length
          ? "No comics match your query"
          : results.join("");
      },
      error: function (xhr, errmsg, err) {},
    });
  }
});

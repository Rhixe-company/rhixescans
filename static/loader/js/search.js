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
            <li role="presentation" class="list-group-item text-dark">
            <a href='/comic/ ${item.pk} /'>
            <img width="100"
                height="100" class="img-thumbnail rounded d-block" src='/media/${item.fields.image}' alt='/media/${item.fields.image}'/>
                </a>
            <div><a href='/comic/ ${item.pk} /'>
            
            <h4 class="comic-title">${item.fields.title}</h4>
            
            </a></div>
             <small>${item.fields.status}</small>
            <span>${item.fields.category}</span>
            </li>
            `
          );
          
        });

        if (!$(".show")[0]) {
          
          $('.menudd').trigger('click')
          
        }
        document.getElementById("list").className = "show";
        document.getElementById("list").innerHTML = (!results.length) ? ("No comics match your query") : (results.join(""));
      },
      error: function (xhr, errmsg, err) {},
    });
  }
});

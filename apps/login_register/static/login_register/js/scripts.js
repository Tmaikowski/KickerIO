// $(document).ready(function(){
$(window).on("load", function() {
  console.log("Loaded");
  $('.carousel').carousel();
  $('.modal').modal();

  $(".like_article").on("click", function(event) { //switch back to .like_article
    event.preventDefault();
    var $t = $(this);
    var articleId = $(this).attr("a-id");
    console.log($t.text());
    if ($t.text() == "Like") {
      $.ajax({
        url: "/news/like_article/" + articleId,
        method: "GET",
        success: function(json) {
          console.log("Success! Like!");
          console.log(json);
          // $t.attr('href', '/news/like_article/' + articleId);
          $t.text('Unlike');
          $t.parent().siblings("h6").text(json + " Likes");

          // $(document.body).html(serverResponse);
        }
      }, "json");
    } else {
      $.ajax({
        url: "/news/unlike/" + articleId,
        method: "GET",
        success: function(json) {
          console.log("Success! Unlike!");
          console.log(json);
          // $t.attr('href', '/news/unlike/' + articleId);
          $t.text('Like');
          $t.parent().siblings("h6").text(json + " Likes");
          // $(document.body).html(serverResponse);
        }
      }, "json");
    }
  });

  $("#help-link").on("click", function(e) {
    e.preventDefault();
    var msg1 = "Type a search term in the search box"
    var msg2 = "A max of 5 recent news stories will appear in a few short seconds."
    var msg3 = "Like a story? Share it with your network!"
    Materialize.toast(msg1, 5000);
    Materialize.toast(msg2, 5000);
    Materialize.toast(msg3, 5000);
  })
  $('.news-row').masonry({
    itemSelector: '.card-panel'
  });

});

$(document).ready(function () {
  $("img").on('error', function() {
    $(this).hide();
  });
  $("#search_form").on("submit", function(e) {
    e.preventDefault();
    $.ajax({
      url: "/search/",
      method: "POST",
      data: $(this).serialize(),
      success: function(json) {
        $("input[name='find_friends']").val("");
        console.log(json);
        console.log("Success");
        console.log(json.search_results);
        htmlStr = "";
        for (var result in json.search_results) {
          person = json.search_results[result];
          htmlStr += "<li><a href=" + "/profile/" + person[0] + ">" + person[1] + " " + person[2] + "</a></li>";
        }
        $("#dropdown1").html(htmlStr);
          // for (var person in result) {
          // console.log(person[0])
          //
          // $("#dropdown1").append(htmlStr);
          // }

        $('.dropdown-button').dropdown('open');

      }
    })
  })
});

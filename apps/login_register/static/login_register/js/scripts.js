// $(document).ready(function(){
$(window).on("load", function() {
  console.log("Loaded");
  $('.carousel').carousel();
  $('.modal').modal();
  $("#like_article").on("click", function(event) {
    event.preventDefault();
    var articleId = $(this).attr("a-id");
    $.ajax({
      url: "/news/like_article/" + articleId,
      method: "GET",
      success: function(serverResponse) {
        $(document.body).html(serverResponse);
      }
    }, "json");
  });
  //code below works for now but refreshes page...
  $("#unlike_article").on("click", function(event) {
    event.preventDefault();
    var articleId = $(this).attr("a-id");
    console.log(articleId);
    $.ajax({
      url: "/news/unlike/" + articleId,
      method: "GET",
      success: function(serverResponse) {
        console.log(serverResponse);
        $(document.body).html(serverResponse);
      }
    }, "json");
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

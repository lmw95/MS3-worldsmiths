 $(document).ready(function () {

  // Activate MaterializeCSS sidenav
  $('.sidenav').sidenav();

  // MaterializeCSS character counter
  $('input#input_text, textarea#textarea1').characterCounter();

  // MaterializeCSS collapsable accordians
  $('.collapsible').collapsible({
    accordion : false
  })

  // MaterializeCSS modal
  $('.modal').modal({
    dismissible: true,
  });

  // Refreshes page to clear flash message on profile
  $('#refresh-page').click(function() {
    location.reload();
});

//https://www.w3schools.com/howto/howto_js_toggle_password.asp
$(".toggle-password").click(function () {
  id = $(this).attr("data-target");
  if ($(`#${id}`).attr("type") === "password") {
    $(`#${id}`).attr("type", "text");
    $(this).removeClass("fa-lock").addClass("fa-lock-open");
  } else if ($(`#${id}`).attr("type") === "text") {
    $(`#${id}`).attr("type", "password");
    $(this).removeClass("fa-lock-open").addClass("fa-lock");
  }
});

});

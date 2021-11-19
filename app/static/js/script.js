 $(document).ready(function () {

  // MaterializeCSS sidenav
  $('.sidenav').sidenav();

  // MaterializeCSS character counter
  $('input#input_text, textarea#textarea1, input#interests').characterCounter();

  // MaterializeCSS collapsable accordians
  $('.collapsible').collapsible({
    accordion : false
  });

  // MaterializeCSS modal
  $('.modal').modal({
    dismissible: true,
  });

  // Refreshes page to clear flash message on profile
  $('#refresh-page').click(function() {
    location.reload();
  });

// Toggle password visibility - see Credits
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

// MaterializeCSS tooltips
$('.tooltipped').tooltip();

// Force modal open - see Credits
const elem = document.getElementById('new-member');
const instance = M.Modal.init(elem, {dismissible: false});
instance.open();

});

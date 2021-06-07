function openModelWithContext(event) {
  var target = $(this).data("target");
  var url = $(this).data("url");
  $.ajax({
    url: url,
    success: function (data) {
      console.log(data);
      console.log(target + ".modal-content");
      $(target + " .modal-content").html(data);
    },
  });
}

$(document).on("click", ".use-modal", openModelWithContext);

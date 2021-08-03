function openModelWithContext(event) {
  var target = $(this).data("target");
  var url = $(this).data("url");
  var action = $(this).data("action");
  var success = $(this).data("success");
  $.ajax({
    url: url,
    data: {
      action: action,
      success: success,
    },
    success: function (data) {
      $(target + " .modal-content").html(data);
    },
  });
}

$(document).on("click", ".use-modal", openModelWithContext);

function upload_img(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $("#img-id").attr("src", e.target.result);
      $("#img-cont").removeClass("d-none");
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    $("#img-cont").addClass("d-none");
  }
}

$(document).ready(function (e) {
  $("input[type=file]").change(function () {
    upload_img(this);
  });
});

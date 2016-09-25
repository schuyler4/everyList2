$("#like").submit(function(e) {
  console.log("submiting")
  e.preventDefault();
  $.ajax({
    type: "POST",
    url: '/like',
    data: {id: $("#likeidInput").val()},
  });
  let text = $('#popularity').text().toString();
  let number = parseInt(text);
  $("#popularity").text(number + 1)
});

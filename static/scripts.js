$(document).ready(function(){
    // click on button submit
    $("#brightness-submit").on('click', function(){
        // send ajax
        var value = parseFloat($('#displayBrightness').val())
        var formData = JSON.stringify( { "level": value} )
        console.log(formData)
        $.ajax({
            url: 'api/v1/display/brightness', // url where to submit the request
            type : "PATCH", // type of action POST || GET
            contentType: 'application/json;charset=UTF-8',
            data : formData,
            success : function(result) {
                console.log(result);
            },
            error: function(xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })
    });

    $("#youtube-submit").on('click', function(){
        // send ajax
        console.log("Button pressed for youtube!")
        var value = $('#addYouTube').val()
        var formData = JSON.stringify( { "url": value} )
        console.log(formData)
        $.ajax({
            url: 'api/v1/sources/youtube', // url where to submit the request
            type : "PUT", // type of action POST || GET
            contentType: 'application/json;charset=UTF-8',
            data : formData,
            success : function(result) {
                console.log(result);
            },
            error: function(xhr, resp, text) {
                console.log(xhr, resp, text);
            }
        })
    });

});

function getFormData($form)
{
  var unindexed_array = $form.serializeArray();
  var indexed_array = {};

  $.map(unindexed_array, function(n, i){
      indexed_array[n['name']] = n['value'];
  });

  return indexed_array;
}
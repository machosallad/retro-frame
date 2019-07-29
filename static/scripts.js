$(document).ready(function(){

    //$(".alert").hide()

    // Load "stuff"
    $.ajax({
        url: 'api/v1/display/brightness', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'json',
        success : function(data) {
            console.log(data);
            $('#displayBrightness').val(data.level)
        },
        error: function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    })
    
    // Submit of brightness
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

    // Submit Youtube video
    $("#youtube-submit").on('click', function(){
        // send ajax
        var value = $('#addYouTube').val()
        var formData = JSON.stringify( { "url": value} )
        console.log(formData)
        $.ajax({
            url: 'api/v1/sources/youtube', // url where to submit the request
            type : "PUT", // type of action POST || GET
            contentType: 'application/json;charset=UTF-8',
            data : formData,
            success : function(result) {
                alert("Success! Hang on tight, loading may take a while...")
                console.log(result);
            },
            error: function(xhr, resp, text) {
                alert("Failure! Failed to load provided video, please try again...")
                console.log(xhr, resp, text);
            }
        })
    });

    // Submit Giphy search
    $("#giphy-submit").on('click', function(){
        // send ajax
        var count = parseInt($('#giphyCount').val())
        var tag = $('#giphyTag').val()
        var formData = JSON.stringify( { "tag": tag, "count" : count} )
        console.log(formData)
        $.ajax({
            url: 'api/v1/sources/giphy/random', // url where to submit the request
            type : "PUT", // type of action POST || GET
            contentType: 'application/json;charset=UTF-8',
            data : formData,
            success : function(result) {
                alert("Success! Hang on tight, loading may take a while...")
                console.log(result);
            },
            error: function(xhr, resp, text) {
                alert("Failure! Failed to load provided video, please try again...")
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
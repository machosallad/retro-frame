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

    $.ajax({
        url: 'api/v1/sources/status', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'json',
        success : function(data) {
            console.log(data);
            $('#imagesCheck').prop('checked', data.images[1])
            $('#animationsCheck').prop('checked', data.animations[1])
            $('#videosCheck').prop('checked', data.videos[1])
            $('#giphyCheck').prop('checked', data.giphy[1])
            $('#youtubeCheck').prop('checked', data.youtube[1])
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

    // Submit of slideshow command
    $("#command-form button").on('click', function(){
        var id = $(this).attr('id');
        var formData = null
        if (id == "slideshow-play")
            formData = JSON.stringify( { "command": "play"} )
        else if (id == "slideshow-pause")
            formData = JSON.stringify( { "command": "pause"} )
        else if (id == "slideshow-previous")
            formData = JSON.stringify( { "command": "previous"} )
        else if (id == "slideshow-next")
            formData = JSON.stringify( { "command": "next"} )

        // send ajax
        console.log(formData)
        $.ajax({
            url: 'api/v1/slideshow', // url where to submit the request
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

    // Update content filter
    $("#enable-content-submit").on('click', function(){
        // send ajax
        var imagesCheck = $('#imagesCheck').is(":checked")
        var animationsCheck = $('#animationsCheck').is(":checked")
        var videosCheck = $('#videosCheck').is(":checked")
        var giphyCheck = $('#giphyCheck').is(":checked")
        var youtubeCheck = $('#youtubeCheck').is(":checked")
        
        var formData = JSON.stringify( {"images" : { "status": imagesCheck}, "animations" : { "status": animationsCheck},"videos" : { "status": videosCheck},"giphy" : { "status": giphyCheck},"youtube" : { "status": youtubeCheck}})
        console.log(formData)
        $.ajax({
            url: 'api/v1/sources/status', // url where to submit the request
            type : "PUT", // type of action POST || GET
            contentType: 'application/json;charset=UTF-8',
            data : formData,
            success : function(result) {
                console.log(result);
            },
            error: function(xhr, resp, text) {
                alert("Failure! Failed to update content filters...")
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
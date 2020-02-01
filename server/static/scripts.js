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
        url: 'api/v1/settings/length', // url where to submit the request
        type : "GET", // type of action POST || GET
        dataType : 'json',
        success : function(data) {
            console.log(data);
            $('#slideshowLength').val(data.level)
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
            $('#imagesToggle').prop('checked', data.images[1]).change()
            $('#animationsToggle').prop('checked', data.animations[1]).change()
            $('#videosToggle').prop('checked', data.videos[1]).change()
            $('#giphyToggle').prop('checked', data.giphy[1]).change()
            $('#youtubeToggle').prop('checked', data.youtube[1]).change()
        },
        error: function(xhr, resp, text) {
            console.log(xhr, resp, text);
        }
    })

    // Submit of brightness
    $("#displayBrightness").on('input', function(){
        console.log("Range changed")
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

    // Submit of view length
    $("#slideshowLength").on('input', function(){
        console.log("View length changed")
        // send ajax
        var value = parseInt($('#slideshowLength').val())
        var formData = JSON.stringify( { "length": value} )
        console.log(formData)
        $.ajax({
            url: 'api/v1/settings/length', // url where to submit the request
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
        var command = $(this).attr('data-id');
        formData = JSON.stringify( { "command": command} )

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

    // Submit of refresh command
    $("#refresh-form button").on('click', function(){
        var command = $(this).attr('data-id');
        address = 'api/v1/sources/' + command + "/refresh"
        // send ajax
        $.ajax({
            url: address, // url where to submit the request
            type : "GET", // type of action POST || GET
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
    $("#allowance-form input:checkbox").on('change', function(){
        var data_id = $(this).attr('data-id');
        var checked = $(this).prop('checked')
        var call = "api/v1/sources/" + data_id + "/status"
        var formData = JSON.stringify( {"status" : checked})
        $.ajax({
            url: call, // url where to submit the request
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

    // Upload image
    $("#upload-image-submit").on('click', function(event){
        event.preventDefault();
        var form = $('#uploadImageForm')[0]
        var formData = new FormData(form);
        var call = "api/v1/sources/upload"
        $.ajax({
            url: call, // url where to submit the request
            type : "POST",
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,
            cache: false,
            data : formData,
            success : function(result) {
                console.log(result);
                alert("Success! Content uploaded")
                $('#uploadImageForm')[0].reset();
            },
            error: function(xhr, resp, text) {
                alert("Failure! Failed to upload")
                console.log(xhr, resp, text);
                $('#uploadImageForm')[0].reset();
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
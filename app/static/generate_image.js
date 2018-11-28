
function generate_image(){

    domtoimage.toBlob(document.getElementById('capture'))
    .then(function (blob) {
        uplaod_image(blob);
    });
}

function uplaod_image(blob){
        var form = new FormData();
        form.append('file', blob, "new_timetable");
        //Chrome inspector shows that the post data includes a file and a title.                                                                                                                                           
        $.ajax({
          type: 'POST',
          url: $SCRIPT_ROOT + '/save_timetable',
          data: form,
          cache: false,
          processData: false,
          contentType: false
        }).done(function(data) {
          console.log(data);
          location.reload();
        });
}


$("body").on("click", "a#get_image", function(){
    generate_image();
    
});

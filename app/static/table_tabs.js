function show_current(){
    $("div#div_ver_html").show();
    $("div#div_ver_png").hide();
}

function show_saved(){
    $("div#div_ver_html").hide();
    $("div#div_ver_png").show();
}

$( document ).ready(function(){
    show_current()
});

$('a#ver_html').click(function() {
    show_current()
});

$('a#ver_png').click(function() {
    show_saved()
});
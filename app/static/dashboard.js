var section_template = "<div class='form-group form-inline section'> \
<label for=''>Day</label> \
<select class='form-control' name='courses'> \
    <option value='M'>Monday</option> \
    <option value='Tu'>Tuesday</option> \
    <option value='W'>Wednesday</option> \
    <option value='Th'>Thursday</option> \
    <option value='F'>Friday</option> \
</select> \
<label for=''>Start time:</label> \
<select class='form-control' name='courses'> \
    <option value='9'>9:00</option> \
    <option value='10'>10:00</option> \
    <option value='11'>11:00</option> \
    <option value='12'>12:00</option> \
    <option value='13'>13:00</option> \
    <option value='14'>14:00</option> \
    <option value='15'>15:00</option> \
    <option value='16'>16:00</option> \
    <option value='17'>17:00</option> \
    <option value='18'>18:00</option> \
    <option value='19'>19:00</option> \
    <option value='20'>20:00</option> \
</select> \
<label for='sel1'>End time:</label> \
<select class='form-control' name='courses'> \
    <option value='9'>9:00</option> \
    <option value='10'>10:00</option> \
    <option value='11'>11:00</option> \
    <option value='12'>12:00</option> \
    <option value='13'>13:00</option> \
    <option value='14'>14:00</option> \
    <option value='15'>15:00</option> \
    <option value='16'>16:00</option> \
    <option value='17'>17:00</option> \
    <option value='18'>18:00</option> \
    <option value='19'>19:00</option> \
    <option value='20'>20:00</option> \
</select> \
<a class='remove_section' id='' href='#'>(Remove)</a> \
</div>   <!-- section -->";

var course_template = "<div class='course'> \
            <div class='form-group form-inline'> \
                <label for='course_name'>Course Name: </label> \
                <input type='text' name='courses'> \
                <a class='remove_course' id='' href='#'>(Remove)</a> \
            </div>"

var add_section_template  = "<a class='add_section' id='' href='#'>Add Section</a> \
<input type='hidden' name='courses'>"

$('a.add_course').click(function() {
    console.log("add course")
    var new_course = $(course_template)
    //default: insert 2 section per course
    $(section_template).insertAfter(new_course.children().last())
    $(section_template).insertAfter(new_course.children().last())

    //insert add section button
    $(add_section_template).insertAfter(new_course.children().last())

    new_course.insertAfter($(this).parents().find("div.course").last())
});


$("form").on("click", "a.add_section", function(){
    $(section_template).insertBefore($(this));
    return false;
});

$("form").on("click", "a.remove_section", function(){
    
    $(this).parent().remove();
    return false;
});

$("form").on("click", "a.remove_course", function(){

    $(this).parent().parent().remove();
    return false;
});

$("div.form-check-inline").click(function(){
    //console.log($(this).children()[0].id);
    if($(this).children()[0].checked){
        check($(this).children()[0].id)
    }
    else{
        uncheck($(this).children()[0].id)
    }
});

function check(id){    
    //console.log("check");
    //console.log("add course")

    //find add_course button

    var new_course = $(course_template)
    new_course.find("input").attr("value", id)

    //get section info from remote
    $.ajax({
        type: 'GET',
        url: $SCRIPT_ROOT + '/get_sections/' + id
      }).done(function(sections_str) {
        //console.log(sections_str);

        sections = JSON.parse(sections_str);

        sections.forEach(function(section) {
            //console.log(section)
            var section_html = $(section_template)

            //set day
            var options = section_html.children("select")[0].options;
            for (var i=0; i< options.length; i++){
                //console.log(section.split("_")[0])
                if (options[i].value == section.split("_")[0]){
                    //console.log(options[i].value)
                    options[i].selected = true
                }
            }

            //set time
            var start_options = section_html.children("select")[1].options
            var end_options = section_html.children("select")[2].options

            for (var i=0; i< start_options.length; i++){
                //console.log(section.split("_")[0])
                var start = section.split(",")[0]
                var start_time = start.split("_")[1]
                var end = section.split(",")[1]
                var end_time = end.split("_")[1]

                if (start_options[i].value == start_time){
                    //console.log(start_options[i].value)
                    start_options[i].selected = true
                }
                if (end_options[i].value == end_time){
                    //console.log(end_options[i].value)
                    end_options[i].selected = true
                }
            }

            section_html.insertAfter(new_course.children().last())

        })
        //insert add section button
        $(add_section_template).insertAfter(new_course.children().last())


        //set course_id
        new_course.attr("id", id)

        new_course.insertAfter($("a.add_course").parents().find("div.course").last())

        
        return false;

      });

    

}

function uncheck(id){
    console.log("uncheck")

    //find div with same id
    $("div#"+id).remove();


}


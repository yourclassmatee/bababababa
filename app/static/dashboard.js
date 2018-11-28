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

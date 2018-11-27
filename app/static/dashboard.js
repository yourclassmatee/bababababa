$('a#add_course').click(function() {
    var courses = $("div[id*='course']"); 
    //console.log(courses);
    //console.log(courses.length);
    var i=0;

    //find largest course_id
    courses.each(function(){
        if (parseInt($(this).attr("id").split("_")[1]) > i){
            i = parseInt($(this).attr("id").split("_")[1]);
        }
    });
    //i is now largest course id

    var new_div = $("#course_" + i).clone();
    
    //replace id of new course div
    new_div.attr("id", "course_"+ (i+1));

    //count num of sections
    var sec_num = new_div.find("div[id*='section']").length
    console.log("number of sec " + sec_num);
    // > default sec num
    var default_sec_num = 2;
    if (sec_num > default_sec_num){
        for (var j=0; j< sec_num - default_sec_num; j++){
            console.log("div#section_" + i + "_" + (sec_num - j));
            console.log(new_div.find("div#section_" + i + "_" + (sec_num - j)));
            new_div.find("div#section_" + i + "_" + (sec_num - j)).remove();
        }
    }

    new_div.find("input").each(function (){
        //console.log($(this).attr("id"))
        if ($(this).attr("id").toString().includes("course")){
            //console.log("here");
            $(this).attr("id", "course_" + (i+1));    
            $(this).val("");
        }
        else if (($(this).attr("id").toString().includes("section"))){
            var sec = $(this).attr("id").toString().split("_")[2];
            $(this).attr("id", "section_" + (i+1) + "_" + sec);
            $(this).attr("name", "course_" + (i+1));
            $(this).val("");
        }
        
    })
    new_div.find("label").each(function (){
        //console.log($(this).attr("id"))
        if ($(this).attr("id").toString().includes("course")){
            //console.log("here");
            $(this).html("Course " + (i+1));
            $(this).attr("id", "course_" + (i+1));    
        }
        else if (($(this).attr("id").toString().includes("section"))){
            var sec = $(this).attr("id").toString().split("_")[2];
            $(this).attr("id", "section_" + (i+1) + "_" + sec);
        }
        
    })
    new_div.find("div").each(function (){
        //console.log($(this).attr("id"))
        if ($(this).attr("id").toString().includes("course")){
            //console.log("here");
            $(this).attr("id", "course_" + (i+1));    
        }
        else if (($(this).attr("id").toString().includes("section"))){
            var sec = $(this).attr("id").toString().split("_")[2];
            $(this).attr("id", "section_" + (i+1) + "_" + sec);
        }
        
    })

    new_div.find("a").each(function (){
        if ($(this).attr("id").toString().includes("remove_course")){
            $(this).attr("id", "remove_course_" + (i+1)); 
        }
        else if (($(this).attr("id").toString().includes("add_section"))){
            $(this).attr("id", "add_section_course" + (i+1)); 
        }
        else if (($(this).attr("id").toString().includes("remove_section"))){
            //console.log($(this).attr("id").toString());
            var sec = $(this).attr("id").toString().split("_")[3];
            //console.log(sec);
            $(this).attr("id", "remove_section_" + (i+1) + "_" + sec);
        }
         
    })

    new_div.insertAfter("#course_"+i);


    return false;
});




$("form").on("click", "a.add_section", function(){
    var course_num = $(this).parent().attr("id").split("_")[1];
    console.log("course " + course_num);
    //find largest section number in course
    var secs = $(this).parent().find("div[id*='section']")

    var sec_num = 0;
    secs.each(function (){
        console.log($(this).attr("id").split("_")[2]);
        if (parseInt($(this).attr("id").split("_")[2]) > sec_num){
            sec_num = parseInt($(this).attr("id").split("_")[2]);
        }
    });
    console.log("section " + sec_num);
    
    //clone largest section
    var new_sec = $("div#section_"+course_num+"_"+sec_num).clone();
    new_sec.attr("id", "section_"+course_num + "_" + (sec_num+1));

    new_sec.find("label").each(function (){
        if (($(this).attr("id").toString().includes("section"))){
            $(this).attr("id", "section_" + course_num + "_" + (sec_num+1));
            $(this).html("Section " + (sec_num+1));
        }  
    })
    new_sec.find("input").each(function (){
        if (($(this).attr("id").toString().includes("section"))){
            $(this).attr("id", "section_" + course_num + "_" + (sec_num+1));
            $(this).attr("name", "course_" + course_num);
            $(this).val("")

        }  
    })

    new_sec.find("a").each(function (){
        if (($(this).attr("id").toString().includes("remove_section"))){
            $(this).attr("id", "remove_section_" + course_num + "_" + (sec_num+1));
        } 
    })
    //append to largest section of the same course
    new_sec.insertAfter("#section_"+course_num + "_" + sec_num);
    return false;
});

$("form").on("click", "a.remove_section", function(){
    var course_num = $(this).attr("id").split("_")[2];
    console.log(course_num);
    var sec_num = $(this).attr("id").split("_")[3];
    console.log(sec_num);
    if(sec_num <= 1){
        return false;
    }
    $(this).parents().find("div#section_" + course_num + "_" + sec_num).remove();
    return false;
});

$("form").on("click", "a.remove_course", function(){
    console.log($(this).attr("id"));
    var course_num = $(this).attr("id").split("_")[2];
    console.log(course_num);

    if(course_num <= 1){
        return false;
    }
    $(this).parents().find("div#course_"+ course_num).remove();


    //TODO: update lables

    return false;
});

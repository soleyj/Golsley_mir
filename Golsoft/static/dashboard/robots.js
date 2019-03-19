$(document).ready(function(){

    $(document).on('click', '.updateButton',function(){
        var robot_id = $(this).attr('member_id')
        $.ajax({
            type: "GET",
            url: state_url,  // URL to your view that serves new info
            data: {'robot_id': robot_id}
        })
    
    });
});



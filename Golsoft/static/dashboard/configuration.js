$(document).ready(function(){

    $(document).on('click', '.addrobotinfo',function(){
        robot_ip = $('#robot_ip').val();
        robot_auth = $('#robot_auth').val();
        console.log(robot_ip)
        $(this).closest('form').find("input[type=text], textarea").val("");
        $.ajax({
            type: "GET",
            url: enter_robot_data_url,  // URL to your view that serves new info
            data: {'robot_ip': robot_ip,'robot_auth':robot_auth}
        })
        .done(function(response) {
            $('#_appendHere').html(response);
        });
        
    
    });
    $(document).on('click', '.removerobotinfo',function(){
        if (confirm("Are you sure to remove the robot??")) {
            var robot_id = $(this).attr('member_id')
            console.log(robot_id)
            $.ajax({
                type: "GET",
                url: remove_robot_data_url,  // URL to your view that serves new info
                data: {'robot_id': robot_id}
            })
            .done(function(response) {
                $('#_appendHere').html(response);
            });
        }
        
        return false;
        
    
    });
    
});
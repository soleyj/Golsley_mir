$(document).ready(function(){

    $(document).on('click', '.addrobotinfo',function(){
        console.log("yes")
    
    });
    $(document).on('click', '.removerobotinfo',function(){
        if (confirm("Are you sure to remove the robot??")) {
            console.log("yes")
        }
        return false;
        
    
    });
    
});
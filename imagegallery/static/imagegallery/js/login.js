$(function(){
    $("#username").change(function() {
        $.get('/api/checkusername',{user: $(this).val()}, function(data){
            if(data.success){
               $('#username').css("background-color","green");
            }else{
               $('#username').css("background-color","red");
            }
        });
    });
    $("#login-username").change(function() {
        console.log("jou")
        $.get('/api/checkloginusername',{user: $(this).val()}, function(data){
            console.log("changing color")
            if(data.success){
               $('#login-username').css("background-color","green");
            }else{
               $('#login-username').css("background-color","red");
            }
        });
    });
    $("#email").change(function(){
    
    });
});


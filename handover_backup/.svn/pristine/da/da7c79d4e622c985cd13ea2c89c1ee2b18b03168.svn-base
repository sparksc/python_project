$("#username").change(function() {
    var username = $(this).val();
    $.ajax({
        url: '/is_user_exist/',
        type: "POST",
        dataType: 'json',
        data: {
            'username': username
        },
        success: function (data) {
            if (data.is_taken) {
                $("#submit_btn").removeClass("disabled")
            } else if (!data.is_taken) {
                Materialize.toast('用户不存在！请检查输入！', 4000);
                $("#submit_btn").addClass("disabled");
            }
        }
    });
});


$("#login_form").submit(function(){
    var username = $("input[name='username']").val();
    var password = $("input[name='password']").val();
    $(this).ajaxSubmit({
        url: '/is_user_exist/',
        type: "POST",
        dataType: 'json',
        data: {
            'username': username,
            'password': password
        },
        success: function (data) {
            if (data.is_right) {
                window.location = "/index/";
            } else {
                Materialize.toast('用户名密码不匹配！请检查输入！', 4000);
            }
        }
    });
    return false;   //阻止表单默认提交
});

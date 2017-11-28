$("a[href='addTeller']").click(function(evt){
	evt.preventDefault();
	$("input[name='teller_serial']").val("");
	$("input[name='teller_pwd']").val("");
    console.log($("#teller_branch_sel").html())
    $("#teller_branch").html("");
    $.ajax({
        url : '/admin/get_branch_inter/',
        type : 'GET',
        dataType : 'json',
        success : function( data ){
            if ( data.is_success ){
                var branchs = data.branchs;
                console.log(branchs)
                for ( var i = 0; i < branchs.length; i++){
                   var sel_br = "<option value='"+branchs[i][0]+"'>"+branchs[i][1]+"</option>";
                    $("#teller_branch").append(sel_br);
                }
            }
        }
    
    });
	$("#addTeller").modal('open');	
});

$("#teller_add_form").submit(function(){
	$("#loading").show();
	var teller_serial = $("#teller_serial").val();
	var teller_pwd = $("#teller_pwd").val();
	var teller_name = $("#teller_name").val();
	var teller_branch = $("#teller_branch").val();
	var teller_tel = $("#teller_tel").val();
	var teller_status = $("#teller_status").val();
    var teller_remark = $("#teller_remark").val();	
	$(this).ajaxSubmit({
		url : '/admin/addteller/',
		type : 'POST',
		dataType : 'json',
		async:false,
		data : {
			'teller_serial' : teller_serial,
			'teller_pwd' : teller_pwd,
			'teller_name' : teller_name,
			'teller_branch' : teller_branch,
			'teller_tel' : teller_tel,
			'teller_status' : teller_status,
			'teller_remark' : teller_remark
		},
		success : function( data ){
			if (data.is_success){
				Materialize.toast( '添加成功！', 4000 );
			}
			else {
				Materialize.toast( '添加失败！', 4000 );
			}
			$("#loading").hide();
			location.reload();
		},
		error : function( data ){
			alert('错误');
		
		}
	});
});
/*
$("a[href='del_teller']").click(function(){
	var user_id = $(this).attr('id');
	$.ajax({
		url : '/admin/delteller/',
		type : 'GET',
		dataType : 'json',
		async:false,
		data : {
			'user_id' : user_id
		},
		success : function( data ){
			if ( data.is_success ){
				Materialize.toast( '删除成功！', 4000 );
			}
			else{
				Materialize.toast( '删除失败！', 4000 );
			
			}
		
		}
	});
});*/

$("a[href='del_teller']").click(function(evt){
    evt.preventDefault();
    var user_id = $(this).attr('id');
        $.confirm({
                    title : '删除柜员信息！',
                    content : '是否删除柜员信息？',
                    type : 'red',
                    autoClose: 'cancel|10000',
                    buttons :{
                       confirm : {
                           text : '确认删除',
                            btnClass : 'waves-effect waves-light btn red',
                            action : function(){
                               $.ajax({
                                   url : '/admin/delteller/',
                                   type : 'GET',
                                   dataType : 'json',
                                   async:false,
                                   data : {
                                       'user_id' : user_id
                                   },
               success : function(data){
               if ( data.is_success ){
                   Materialize.toast( '删除成功！', 4000 );
               }
               else {
                   Materialize.toast('删除失败！', 4000);
               }
                location.reload();                                                      
           }
       }
   );
   }
},
    cancel : {
         text : '取消',
         action : function(){
             }
         }
        }
    });
});

//回显信息alter_innserstaff
$("a[href='alter_teller']").click(function( evt ){
    console.log("ddddd");
    evt.preventDefault();
    $("#alterstaff_modal").modal('open');
    var staff_id = $(this).attr('id');
    $.ajax({
        url : '/maintenance/show_teller/',
        type : 'POST',
        dataType : 'json',
        data : {
            'staff_id' : staff_id
        },
        success : function( data ){
            console.log( data.name)
            if ( data.is_success ){
                $("#teller_alter_serial").val(data.serial);
                $("#teller_alter_name").val(data.name);
                $("#teller_alter_branch").val(data.branch_name);
                $("#teller_alter_tel").val(data.tel);
                $('#teller_alter_alter').html("");
				$("input[name='staff_id']").val(staff_id);
                if ( data.t_status == "在岗" ){
                    var sel_statuson = "<option value='1' selected>在岗</option>";
                    var sel_statusoff= "<option value='2'>离岗</option>";
                    $('#teller_alter_alter').append(sel_statuson);
                    $('#teller_alter_alter').append(sel_statusoff);
                
                }  else{
                    var sel_statuson = "<option value='1'>在岗</option>";
                    var sel_statusoff= "<option value='2' selected>离岗</option>";
                    $('#teller_alter_alter').append(sel_statuson);
                    $('#teller_alter_alter').append(sel_statusoff);
                }
                $("#teller_alter_remark").text(data.remark);
                
            }
            
        
        }
    
    });

});









$("input[name='teller_serial']").change(function(){
	var teller_serial = $(this).val();
    check_form( teller_serial );
	
});
/*
$("#teller_branch").change(function(){
	var teller_serial = $("input[name='teller_serial']").val();
	var teller_branch = $(this).val();
    var branch_name = $(this).text();
    console.log(teller_branch);
    if ( teller_serial != '' && teller_branch != '' ){
        check_form( teller_serial, teller_branch, branch_name );
					    
	}


});*/

//防止重复添加
function check_form( teller_serial ){
        $("#addteller_btn").addClass('disabled');
		$.ajax({
			url : '/admin/teller_form_check/',
			type : 'POST',
			dataType : 'json',
			data : {
				'teller_serial' : teller_serial
			},
			success : function( data ){
				if (data.user_token) {
					var mes =  '已存在柜员编号：'+teller_serial; 
					Materialize.toast( mes, 4000 );
				}
				else{
					$("#addteller_btn").removeClass('disabled');
				}
			}
		});
}


$("#teller_pwd2").change(function(){
    $("#addteller_btn").addClass('disabled');
    var pwd = $("#teller_pwd").val();
    var pwd2 = $(this).val();
    if ( pwd == ""){
        Materialize.toast( "请输入柜员密码", 4000 );
        return;
    }
    if ( pwd2 != pwd ){
        Materialize.toast( "两次密码不一致", 4000 );
    
    }else{
        $("#addteller_btn").removeClass('disabled');

    }
    
    
});

$("#teller_pwd").change(function(){
    $("#teller_pwd2").val("");
    /*
    var pwd2 = $("#teller_pwd2").val();

    var pwd = $(this).val();
    console.log(pwd2+pwd)
    if ( pwd2 == "")
            return;

    if ( pwd == ""){
        Materialize.toast( "请输入柜员密码", 4000 );
        return;
    }
    if ( pwd2 != pwd ){
        Materialize.toast( "两次密码不一致", 4000 );
    
    }*/
    
    
});




$("#alter_innerstaff").submit(function(){
	var staff_id = $("input[name='staff_id']").val();
	var teller_name = $("input[name='teller_alter_name']").val();
	var tel = $("input[name='teller_alter_tel']").val();
	var tel_status = $("#teller_alter_alter").val();
	var remark = $("#teller_alter_remark").val();
	$(this).ajaxSubmit({
		url : '/maintenance/alterstaff/',
		type : 'POST',
		dataType : 'json',
		async: false,
		data :{
			'staff_id' : staff_id,
			'teller_name' : teller_name,
			'tel' : tel,
			'tel_status':tel_status,
			'remark' : remark 
		},
		success : function(data){
			if ( data.is_success ){
				Materialize.toast( "修改成功", 4000 );
			}
			location.reload();
				
			
		
		}
	
	});

});

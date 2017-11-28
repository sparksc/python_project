$("#person_modify_form").submit(function(){
	var amp_name = $(".amp_add_name").val();
	$(this).ajaxSubmit({
		url : '/admin/addambang/',
		type : 'POST',
		dataType : 'json',
        async: false,
		data : {
			'amp_name': amp_name
		},
		success : function( data ){
			if (data.is_success ){
				Materialize.toast( '添加成功！', 4000 );	
			}else{
				Materialize.toast( '添加失败！', 4000 );
			
			}
            
				location.reload();
				$.cookie('index_page', '#ampangInfo');
		}
	});
});

$(".ambsearch").change(function(){
    var searchname = $("#searchname").val();
    $("div[tag='ambblock']").hide();

});


$("#major_add_form").submit(function(){
    $("#loading").show();
    var major_name = $("input[tag='major_add_name']").val();
    var major_serial = $("input[tag='major_add_serial']").val();
    $(this).ajaxSubmit({
        url : '/admin/addmajor/',
        type : 'POST',
        dataType : 'json',
        async: false,
        data : {
            'major_name': major_name,
            'major_serial':major_serial
        },
        success : function(data){
            if (data.is_success){
                Materialize.toast( '添加成功！', 4000 );
            }
            else{
                Materialize.toast( '添加失败！', 4000 );
            }
            $.cookie('index_page', '#majorInfo');
            location.reload();
        
        }
    
    });

});






$("#assist_add_form").submit(function(){
	$("#loading").show();
	var assist_name = $("input[tag='as_add_name']").val();
	var assist_serial = $("input[tag='as_add_serial']").val();
	$(this).ajaxSubmit({
		url : '/admin/addassist/',
		type : 'POST' ,
		dataType : 'json',
        async: false,
		data : {
			'assist_name' : assist_name,
			'assist_serial' : assist_serial
		},
		success : function( data ){
			if ( data.is_success ){
				Materialize.toast( '添加成功！', 4000 );
			}
			else {
				Materialize.toast( '添加失败！', 4000 );
			}
			$("#loading").hide();
			$.cookie('index_page', '#assistInfo');
			location.reload();
		}
	});
});

//押运人员删除
$(".del_ambang").click(function(evt){
	evt.preventDefault();
	var ambang_id = $(this).attr('id');
	console.log(ambang_id);
	$.confirm({
		title : '删除押运人员信息！',
		content : '是否删除押运人员信息？',
		type : 'red',
		autoClose: 'cancel|10000',
		buttons :{
			confirm : {
				text : '确认删除',
				btnClass : 'waves-effect waves-light btn red',
				action : function(){
					$.ajax({
						url : '/admin/ambangdel/',
						type : 'GET',
						dataType : 'json',
						data : {
							'ambang_id' : ambang_id
						},
						success : function(data){
							if ( data.is_success ){
								Materialize.toast( '删除成功！', 4000 );
							}
							else {
								Materialize.toast('删除失败！', 4000);
							}
							$.cookie('index_page', '#ampangInfo');
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

//回显信息
$('.modify_btn').click(function(evt) {
    evt.preventDefault();
    var ampang_id = $(this).attr('id');
    $.ajax({
    url : '/admin/showambang/',
    type : 'POST',
    dataType : 'json',
    data : {
	'ampang_id' : ampang_id

    },
    success : function (data){
	console.log('返回成功',data.is_success);
	if ( data.is_success ){
		//console.log(data)
		$("label[for='alter_name']").addClass('active');
		$('#alter_amb_id').val(data.ambang_id);
		$('#alter_name').val(data.ambang_name);
		$('#alterambanginfo').modal('open');	
		}
	
	else{
		Materialize.toast('人员信息错误！', 4000);
		$('#alterambanginfo').modal('close');
		}   
	}

})
});
//添加人员信息
/*
$('#add_amb').click(
	function(evt) {
		evt.preventDefault();
		$('#amb_head').html("");
	    $('#amb_head').text("录入押运人员信息");	
		$('#ampanginfo').modal('open');
		}
							
							
);*/
 


$("#ambang_alter_form").submit(function(){
	$("#loading").show();
	var name = $("input[name='name']").val();
	var ambang_id = $("#alter_amb_id").val();
	$(this).ajaxSubmit({
			url : '/admin/alterambang/',
			type : 'POST',
			dataType : 'json',
            async: false,
			data : {
			'ambang_id' : ambang_id,
			'name' : name
			},
			success : function(data) {
			if (data.is_success){
				Materialize.toast('修改成功！', 10000);
			}
			else{
				Materialize.toast('修改失败！', 10000);
			}
			location.reload();
			$("#loading").hide();
			$.cookie('index_page', '#ampangInfo');	
		}
	  }		
	)
		return false;
});


//网点主办人员管理
/*
$(".del_btn").click(function(){
	$("#loading").show();
	var major_id = $(this).attr('id');
	alert(major_id);
	$.ajax({
			url : '/admin/delmajor/',
		    type : 'POST',	   
			dataType : 'json',
			data : {
			'major_id' : major_id
			},
			success : function(data){
			if ( data.is_success ) {
			Materialize.toast( '删除成功！', 10000 );
			}
			else {
			
			Materialize.toast('删除失败！', 10000);
			}
			location.reload()
			$("#loading").hide();
			}
	})	

});*/

$(".del_btn_major").click(function(evt){
	evt.preventDefault();
	var major_id = $(this).attr('id');
	$.confirm({
		title: '删除主办人信息!',
		content: '是否删除主办人员信息？',
		type : 'red',
		autoClose: 'cancel|10000',
		buttons : {
			confirm: {
				text : '确认删除',
				btnClass :'waves-effect waves-light btn red',
				action : function(){
					$.ajax({
						url : '/admin/delmajor/',
						type : 'POST',	   
						dataType : 'json',
						data : {
							'major_id' : major_id
							},
						success : function(data){
						if ( data.is_success ) {
							Materialize.toast( '删除成功！', 10000 );
							}
						else {
							Materialize.toast('删除失败！', 10000);
							}
						location.reload();
						$.cookie('index_page', '#majorInfo');

						}
					})	
				}
				
			},
			cancel : {
				text : '取消',
				action : function(){
				}
		}
		/*
		confirm: function(){
		$.alert('Confirmed!');
		},
		cancel: function(){
		$.alert('Canceled!')
		}*/
    }
	});
});

//回显主办人员信息
$(".modify_btn_major").click(function(evt){
	evt.preventDefault();
	var major_id = $(this).attr("id");
	$.ajax({
		url : '/admin/showmajor/',
		type : 'POST',
		dataType : 'json',
		data : {
			'major_id' : major_id
		},
		success : function(data) {
			if ( data.is_success ) {
				$("#alter_major_id").val(data.major_id);
				$("label[for='alter_name']").addClass('active');
				$("label[for='alter_serial']").addClass('active');
				$("input[name='alter_name']").val(data.major_name);
				$("input[name='alter_serial']").val(data.major_serial);
				$("#altermajorInfo").modal('open');
				
			}
			else{
			Materialize.toast('未知错误！', 10000);
			
			
			}	
		
		}
	})
});

//修改主办人员信息
$("#major_alter_form").submit(function(){
	$("#loading").show();
	var major_name = $( "input[name='alter_name']" ).val();
	var major_serial = $( "input[name='alter_serial']").val();
	var major_id = $( "#alter_major_id" ).val();
	$(this).ajaxSubmit({
		url : '/admin/altermajor/',
		type : 'POST',
		dataType : 'json',
        async: false,
		data : {
			'major_id' : major_id,
			'major_name' : major_name,
			'major_serial' : major_serial
		},
		success : function(data) {
			if ( data.is_success ){
				Materialize.toast('修改成功！', 4000);
			}
			else {
				Materialize.toast('修改失败！', 4000);
			}	
			location.reload();
			$.cookie('index_page', '#majorInfo'); 
		}

	})
	return false;
});



$(".del_btn_assist").click(function(evt){
	evt.preventDefault();
	var assist_id = $(this).attr('id');
	$.confirm({
		title: '删除主办人信息!',
		content: '是否删除主办人员信息？',
		type : 'red',
		autoClose: 'cancel|10000',
		buttons : {
			confirm: {
				text : '确认删除',
				btnClass :'waves-effect waves-light btn red',
				action : function(){
					$.ajax({
						url : '/admin/delassist/',
						type : 'GET',	   
						dataType : 'json',
						data : {
							'assist_id' : assist_id
							},
						success : function(data){
						if ( data.is_success ) {
							Materialize.toast( '删除成功！', 10000 );
							}
						else {
							Materialize.toast('删除失败！', 10000);
							}
							location.reload();
							$.cookie('index_page', '#assistInfo');
						}
					})	
				}
				
			},
			cancel : {
				text : '取消',
				action : function(){
				}
		}
        }
	});
})


//回显信息
$(".modify_btn_assist").click(function(evt){
	 evt.preventDefault();
	 var assist_id = $(this).attr('id');
	 $.ajax({
		url : '/admin/showassist/',
		type : 'POST',
		dataType : 'json',
		data : {
			'assist_id' : assist_id
		},
		success : function( data ) {
			if ( data.is_success ){
				$("label[for='assist_name']").addClass('active');
				$("label[for='assist_serial']").addClass('active');
				$("input[name='assist_name']").val(data.assist_name);
				$("input[name='assist_serial']").val(data.assist_serial);
				$("#alter_assist_id").val(data.assist_id);
				$("#alterassistInfo").modal('open');
			}
			else {
				Materialize.toast('未找到该人员！', 10000);   
			}
		}		
	 }
 )
});

//修改
$("#assist_alter_form").submit(function(){
	var assist_id = $("#alter_assist_id").val();
	var assist_name = $("input[name='assist_name']").val();
	var assist_serial = $("input[name='assist_serial']").val();
	$(this).ajaxSubmit({
		url : '/admin/alterassist/',
		type : 'POST',
		dataType : 'json',
        async: false,
		data : {
		'assist_id' : assist_id,
		'assist_name' : assist_name,
		'assist_serial' : assist_serial
		},
		success : function(data){
			if ( data.is_success ){
				Materialize.toast('修改成功！', 10000);
			}
			else{
				Materialize.toast('修改失败！', 10000);
			}
			location.reload();
			$.cookie('index_page', '#assistInfo');
		}
	}
);
		return false;

});
$(".assist_check_serial").change(function(){
	var serial = $(this).val();
	$.ajax({
		url : '/admin/assist_form_check/',
		type : 'GET',
		dataType : 'json',
		data : {
			'assist_serial' : serial
		
		},
		success : function(data){
			if ( data.assist_serial_token ){
				Materialize.toast('主办人编号已存在，请检查输入！', 4000);
				$("#assistInfoAdd_submit").addClass('disabled');
			}
			else {
				$("#assistInfoAdd_submit").removeClass('disabled');
			}
		}
		
	
	});


});

//验证主办serial是否存在
$(".major_check_serial").change(function() {

	var major_serial = $(this).val();
	//console.log(major_serial);
	$.ajax({
		url : '/admin/major_form_check/',
		type : 'GET',
		dataType : 'json',
		data : {
			'major_serial' : major_serial
		},
		success : function(data){
			if ( data.is_major_serial_exist ){
				Materialize.toast('主办人编号已存在，请检查输入！', 4000);
				$("#majorInfoAdd_submit").addClass("disabled");
			}
			else{
				//alert('dddd');
				$("#majorInfoAdd_submit").removeClass("disabled");
			}
		}
	}
);
	/*
    var serial = $(this).val();

	alert(serial);
    $.ajax({
        url: '/admin/car_form_check/',
        type: "POST",
        dataType: 'json',
        data: {
            'serial': serial
        },
        success: function (data) {
            if (data.is_serial_taken) {
                Materialize.toast('车辆编号已存在，请检查输入！', 4000);
                $("#car_submit").addClass("disabled");
            } else if (!data.is_serial_taken) {
                $("#car_submit").removeClass("disabled");
            }
        }
    });*/
});
//加载后留在原页面
//cookie解决页面跳转
$(window).load(function(){
	var index_page = $.cookie('index_page'); 
	if ( index_page == null )
		return;
	var selector_inx_page = "a[href='"+index_page+"']"; 
	$(selector_inx_page).trigger('click');
	$.cookie('index_page', '#ampangInfo'); 
});




var fileExtension = ['jpeg', 'jpg', 'png'];
//押运添加图片校验
$(".amp_fimg_addinput").change(function(){
	/*
	var amp_fimg_name = $(this).val();
	if ( !is_image( amp_fimg_name ) ){
		$(".add_amp_btn").addClass("disabled");
	}
	else {
		$(".add_amp_btn").removeClass("disabled");
	}*/
	var amp_bimg = $(".amp_bimg_addinput").val();
	if ( amp_bimg != ""){
		if (  !is_image( amp_bimg ) ){
			return;
	}
	}
	var amp_fimg_name = $(this).val();
	var btnClass = ".add_amp_btn";
	img_flag = is_image( amp_fimg_name ) ;
	img_disabled( img_flag, btnClass );

});

$(".amp_bimg_addinput").change(function(){
	/*
	var amp_fimg_name = $(this).val();
	if ( !is_image( amp_fimg_name ) ){
		$(".add_amp_btn").addClass("disabled");
	}
	else {
		$(".add_amp_btn").removeClass("disabled");
		 }*/
	var amp_fimg = $(".amp_fimg_addinput").val();
	if ( amp_fimg != ""){
		if ( !is_image( amp_fimg ) ){
			return;
		}
	}

	var amp_bimg_name = $(this).val();
	var btnClass = ".add_amp_btn";
	img_flag = is_image( amp_bimg_name ) ;
	img_disabled( img_flag, btnClass );
});
//押运修改图片校验
$(".amp_fimg_alterinput").change(function(){
/*	var amp_fimg_name = $(this).val();
	if ( !is_image( amp_fimg_name ) ){
		$(".alter_amp_btn").addClass("disabled");
	}
	else {
		$(".alter_amp_btn").removeClass("disabled");
	}*/
	var amp_bimg = $(".amp_bimg_alterinput").val();
	if ( amp_bimg != ""){
		if (  !is_image( amp_bimg ) ){
			return;
		}
	}
	var amp_fimg_name = $(this).val();
	var btnClass = ".alter_amp_btn";
	img_flag = is_image( amp_fimg_name ) ;
	img_disabled( img_flag, btnClass );


});


$(".amp_bimg_alterinput").change(function(){
	/*
	var amp_fimg_name = $(this).val();
	if ( !is_image( amp_fimg_name ) ){
		$(".alter_amp_btn").addClass("disabled");
	}
	else {
		$(".alter_amp_btn").removeClass("disabled");
	}*/
	var amp_bimg = $(".amp_fimg_alterinput").val();
	if ( amp_bimg != ""){
		if (  !is_image( amp_bimg ) ){
			return;
	}
	}

	var amp_fimg_name = $(this).val();
	var btnClass = ".alter_amp_btn";
	img_flag = is_image( amp_fimg_name ) ;
	img_disabled( img_flag, btnClass );
});


$(".assist_himg_addinput").change(function(){
	var assist_himg_name = $(this).val();
	var btnClass = '.add_assist_btn';
	img_flag = is_image( assist_himg_name);
	img_disabled( img_flag, btnClass);

});

$(".assist_himg_alterinput").change(function(){
	var assist_himg_name = $(this).val();
	var btnClass = '.alter_assist_btn';
	img_flag = is_image( assist_himg_name );
	img_disabled( img_flag, btnClass);

});
$(".major_himg_addinput").change(function(){
	var major_himg_name = $(this).val();
	var btnClass = '.add_major_btn';
	img_flag = is_image( major_himg_name );
	img_disabled( img_flag, btnClass);

});
$(".major_himg_alterinput").change(function(){
	var major_himg_name = $(this).val();
	var btnClass = '.alter_major_btn';
	img_flag = is_image( major_himg_name );
	img_disabled( img_flag, btnClass);
});

//图片格式校验
function is_image(filename){
	var extension = filename.substring( filename.lastIndexOf('.') + 1 );
	if ( extension == filename){
		return false;
	}else{
		extension = extension.toLowerCase();
	}
	if ( $.inArray(extension, fileExtension) == -1 ){
		return false;
	} else{
		return true;
	}
}

//判断格式给按钮添加disabled
function img_disabled( img_flag, btnClass ){
	if ( img_flag ){
		$(btnClass).removeClass('disabled');
	}

	else {
		//console.log('dddd');
		$(btnClass).addClass('disabled');
		Materialize.toast('文件格式错误！请上传JPEG、JPG、PNG格式图片。', 4000);
	}

}








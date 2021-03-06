$("a[href='#addcashbox_modal']").click(function(){
    console.log('qiangixang');
    $.ajax({
        url : '/admin/addcashbox_form/',
        type : 'GET',
        dataType : 'json',
		async : false,
        success :function( data ){
           if ( data.is_success ) {
               
                var branchs = data.branchs;
                $("#add_bran").html("");
                console.log(branchs)
                for ( var i = 0; i < branchs.length; i++ ){
                    var bran_sel = "<option value='"+(branchs[i][0])+"'>"+branchs[i][1]+"</option>";
                    $("#add_bran").append(bran_sel);
                }
           }
            
        }
    
    });
});


$("#add_cashbox_form").submit(function(){
    var cash_serial = $("input[name='cash_serial']").val();
    var cash_kind = $('#cash_kind_sel option:selected').text();;
    var branch_id = $("#add_bran").val();
    var remark = $("#remark").val();
    $(this).ajaxSubmit({
        url : '/admin/addcashbox/',
        type : 'POST',
        dataType : 'json',
		async : false,
        data : {
            'serial' : cash_serial,
            'kind' : cash_kind,
            'branch_id' : branch_id,
            'remark' : remark
        },
        success : function( data ){
            if( data.is_success ){
                Materialize.toast( '添加成功！', 4000 );
            }else{
                Materialize.toast( '添加失败！', 4000 );
            
            }
            
        }
    
    });

});

//钱箱回显
$(".cashb_show").click(function(){
    alert('show');
});
//钱箱删除
$(".cashb_delete").click(function(evt){
    evt.preventDefault();
    var cashbox_id = $(this).attr('href');
    $.confirm({
        title : '删除钱箱信息！',
        content : '是否删除钱箱信息？',
        type : 'red',
        autoClose: 'cancel|10000',
        buttons :{
            confirm : {
                text : '确认删除',
                btnClass : 'waves-effect waves-light btn red',
                action : function(){
                    $.ajax({
                        url : '/admin/cashboxdel/',
                        type : 'GET',
                        dataType : 'json',
						async : false,
                        data : {
                            'cashbox_id' : cashbox_id
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


//cashbox回显
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
        }   
    }

})
});


//查询cashbox
$(".searchbox").click(function(){
	var serial = $(".cashserial").val();
	var branch = $("#sch_branch").val();
	self.location.href = '/maintenance/searchbox/?serial='+serial+'&branch='+branch;
	var branch_name = $("#sch_branch>option:selected").text();
	$.cookie('serial', serial);
	$.cookie('branch', branch_name);
});

$(window).load(function(){
	var serial = $.cookie('serial');
	var branch = $.cookie('branch');
	if (serial == '' && branch == '请选择银行')
		return;
	else if( branch == '请选择银行'){
		var serial_mes = "<span>搜寻编号："+serial+"</span>";
		var branch_mes = "<span>银行：无</span>"
	}
	else if(serial == '' ){
		var serial_mes = "<span>搜寻编号：无</span>";
		var branch_mes = "<span>银行："+branch+"</span>";

	}
	else{
		var serial_mes = "<span>搜寻编号："+serial+"</span>";
		var branch_mes = "<span>银行："+branch+"</span>";
	}
	$('#serach_term').append(serial_mes);
	$('#serach_term').append('<br>')
	$('#serach_term').append(branch_mes);
	$.cookie('serial', null);
	$.cookie('branch', null);

	
})


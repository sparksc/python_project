$("#add_chip").click(function(){
	  $("#branch_selector").slideToggle();
});

$("a[href='addroute']").click(function(evt){
	evt.preventDefault();
    $("#branch_selector").html("");
    $(".branch_token").each(function(){
        var branch_name = $(this).val();
        var branch_id = $(this).attr('id');
        var branch_button = "<a class='waves-effect waves-teal btn-flat branch' id='"+branch_id+"'>"+branch_name+"</a>";
        $("#branch_selector").append( branch_button );
    
    });
	$("#branch_selector").hide();
	$("#addroute_modal").modal('open');
});





$("#branch_selector").on('click','.branch',function(){
	var branch_name = $(this).text();
    var branch_id = $(this).attr('id');
	//$(this).addClass('disabled');
    var chip = "<div class='chip'  index='chip' id='"+branch_id+"' name="+branch_name+" >"+branch_name+"<i class='material-icons close'>close</i> </div>";
    $(".chips-group-setroute").append(chip);
    console.log(chip);

});


$("input[name='route_name']").change(function(){
	$('#addroute').addClass('disabled');
	var route_name = $(this).val();
	$.ajax({
		url : '/maintenance/rname_check/',
		type : 'GET',
		dataType : 'json',
		data : {
			'route_name' : route_name
		},
		success : function( data ){
			if ( data.route_token ){
				Materialize.toast('线路名称已存在，请重命名！', 4000);
				
			}else{
				$('#addroute').removeClass('disabled');
				
			}
			
		}
	
	});
	
});
/*
$("input[name='alter_route_name']").change(function(){

	    $('#alterroute').addClass('disabled');
	    var route_name = $(this).val();
	    $.ajax({
			url : '/maintenance/rname_check/',
			type : 'GET',
			dataType : 'json',
			data : {
			'route_name' : route_name
			},
			success : function( data ){
				if ( data.route_token ){
					Materialize.toast('线路名称已存在，请重命名！', 4000);
					}else{
					$('#alterroute').removeClass('disabled');
									
				}

			}

		});

		
}	);*/

$("#add_route_form").submit(function(evt){
	evt.preventDefault();
	
	var addchips = $("div[name='addchips']").text();
	console.log(addchips);
	if ( addchips.trim() == '' ){
		Materialize.toast('线路不能为空！', 4000);
		return;	
	}

    var route_name = $('#route_name').val();
    var route = "";
    $("div[index='chip']").each(function(){
    if ( route  == "" ){
        route = $(this).attr('id');
    }else {
        route = route + '-' + $(this).attr('id');
    }
});
    $(this).ajaxSubmit({
        url : '/admin/addroute/',
        type :'POST',
        dataType : 'json',
		async : false,
        data : {
            'route_name' : route_name,
            'route' : route
        },
        success : function(data) {
            if ( data.is_success ){
                Materialize.toast('路线设置成功！', 4000);
            }
            else {
                Materialize.toast('路线设置失败！', 4000);
            }
            $.cookie('route_page', '#setroute');
            location.reload();
        }
    });
});

$(".route_delete").click(function(evt){
    evt.preventDefault();
    var route_id = $(this).attr('id');
    
    $.confirm({
        title : '删除路线信息！',
        content : '是否删除路线信息？',
        type : 'red',
        autoClose : 'cancel|10000',
        buttons :{
            confirm : {
                text : '确认删除',
                btnClass : 'waves-effect waves-light btn red',
                action : function(){
                        $.ajax({
                            url : '/admin/delroute/',
                            type : 'GET',
                            dataType : 'json',
							async:false,
                            data : {
                                'route_id' : route_id
                            },
                            success : function(data){
                                if (data.is_success){
                                    Materialize.toast('路线删除成功！', 4000);
                                }else{
                                    Materialize.toast('路线删除成功！', 4000);
                                }
                                $.cookie('route_page', '#setroute');
                                location.reload();
                            }
                        });
                    
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

//回显路径
$(".route_show").click(function(evt){
    evt.preventDefault();
    var route_id = $(this).attr('id');
    var count = $(this).attr('count');
    $("#alter_branch_selector").html("");
    $(".chips-group-alterroute").html("");
    $.ajax({
        url : '/admin/routeshow/',
        type : 'POST',
        dataType : 'json',
        data : {
            'route_id' : route_id
        },
        success : function( data ){
            $("#alter_route_id").val(route_id);
            $("#route_count").val(count);
            $("#alter_route_name").val(data.name);
            $("#add_date").val(data.modify_date);
            var branch_routes = data.branch_routes;
            for( var i = 0; i < branch_routes.length; i++ ) {
               var branch = branch_routes[i];
			   //name属性存储地点id
               var chip = "<div class='chip'  index='chipalter' name="+branch[0]+" >"+branch[1]+"<i class='material-icons close'>close</i> </div>";
                $(".chips-group-alterroute").append(chip);
           }
            $(".branch_token").each(function(){
                var branch_name = $(this).val();
				var branch_id = $(this).attr('id');
                var branch_button = "<a class='waves-effect waves-teal btn-flat alter_branch' name='"+branch_id+"'>"+branch_name+"</a>";
                $("#alter_branch_selector").append( branch_button );
        
    });


        }
    });
    $("label[for='route_count']").addClass('active');
    $("label[for='add_date']").addClass('active');
    $("label[for='alter_route_name']").addClass('active');
    $('#alter_branch_selector').hide();
    $('#alterroute_modal').modal('open');
})


$("#alter_branch_selector").on('click','.alter_branch',function(){
        var branch_name = $(this).text();
        var branch_id = $(this).attr('name');
        //$(this).addClass('disabled');
        var chip = "<div class='chip'  index='chipalter' name="+branch_id+" >"+branch_name+"<i class='material-icons close'>close</i> </div>";
        $(".chips-group-alterroute").append(chip);

})    


$("#alter_chip").click(function(){
    $('#alter_branch_selector').slideToggle();    

});

//修改路线

$("#alter_route_form").submit(function(evt){
	evt.preventDefault();
    var route_name = $("input[name='alter_route_name']").val();
    var route_id = $("#alter_route_id").val();
    var route = "";
    console.log(route_name+route_id);
	//name表示地点id
    $("div[index='chipalter']").each(function(){
            if ( route  == "" ){
                route = $(this).attr('name');
            }else {
                route = route + '--' + $(this).attr('name');
            }
    });
	if (route==""){
		Materialize.toast('路线不能为空！', 4000);	
		return;
	}
	console.log(route)
    $(this).ajaxSubmit({
        url : '/admin/alterroute/',
        type : 'POST',
        dataType : 'json',
		async:false,
        data : {
            'route_id' : route_id,
            'route_name' : route_name,
            'route' : route
        },
        success : function(data){
            if ( data.is_success ){
               Materialize.toast('路线修改成功！', 4000); 
            }else {
                Materialize.toast('路线修改失败！', 4000);
            }
            $.cookie('route_page', '#setroute');
            location.reload();
        }
    });
});

//分配线路
$("#route_select").change(function(){
    var route_id = $(this).val();
    $.ajax({
        url : '/admin/getroute/',
        type : 'GET',
        dataType: 'json',
        data : {
            'route_id' : route_id
        },
        success:function( data ){
            if( data.is_success ){
                var routes = data.routes.split('-');
                $("input[name='route_input']").each(function(index){
                    $(this).val(routes[index]);
                
                });
                
                
            }
        }
    
    });

});


//获取id组以‘-’拼接
function getids(obj){
    var obj_ids="";
    for ( var i=0; i < obj.length; i++ ){
        if (obj_ids =="" ){
            obj_ids = obj[i].id;
        }else{
            obj_ids = obj_ids + '-' + obj[i].id;
        }
    
    }
    return obj_ids;

}
$("#preview").click(function(){
    var route = $("#route_select").val();
    var car = $("#car_select").val();
    var sites = $("#site_sel").select2('data');
    var majors = $("#major_sel").select2('data');
    var assists = $("#assist_sel").select2('data');
    var ambs = $("#amb_sel").select2('data');
    var site_ids = getids(sites);
    var major_ids = getids(majors);
    var assist_ids = getids(assists);
    var amb_ids = getids(ambs);
     
    $.ajax({
        url : '/admin/preview/',
        type : 'POST',
        dataType : 'json',
        async : false,
        data : {
            "route_id" : route,
            "car_id" : car,
            "site_ids" : site_ids,
            "major_ids" : major_ids,
            "assist_ids" : assist_ids,
            "amb_ids" : amb_ids
        },
        success : function(data){
            if ( data.is_success ){
            
                alert("dddd");
            }

            
        }
        
    });



});








///cookie解决页面跳转
$(window).load(function(){
    var index_page = $.cookie('route_page');
    if ( index_page == null )
        return;
    var selector_inx_page = "a[href='"+index_page+"']";
    $(selector_inx_page).trigger('click');
    $.cookie('route_page', '#approvalroute');
});


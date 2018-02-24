
/**
 * pos Controller
 */
ysp.controller('pos_inputController', function($scope,store, $rootScope,pos_inputService,SqsReportService){

    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.date = moment();
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
    };

    $scope.parse_paginfo = function(actions){
        $scope.cur_page =1
        for (var i in actions){
            var action = actions[i];
            var act = action.action;
            var info = action.conversation_id;
            var pairs = info.split("&")
            for(var j in pairs){
                if (pairs[j].indexOf('total_count')!=-1){
                    $scope.total_count = pairs[j].split('=')[1];
                }
                if (pairs[j].indexOf('page')!=-1){
                    var page = pairs[j].split('=')[1];
                    if ( act === "previous"){
                        $scope.cur_page = parseInt(page) + 1;
                    }
                    if ( act === "next"){
                        $scope.cur_page = parseInt(page) - 1;
                    }
                }
            }

        }
    }
    var load = function () {
        params=$scope.cust_search;
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        SqsReportService.info('pos_input', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });

    };

    $scope.cust_search = {};
    var element_edit = angular.element('#pos_input_edit_modal');
    var element_add = angular.element('#pos_input_add_modal');
    

    $scope.search = function () {
        load();
    };

    $scope.upload_excel = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0)
        {
            alert("请先选择对应的文件内容,再导入!");
            return;
        }
        $("div[name='loading']").modal("show");
        var token = store.getSession("token");
        var form = new FormData();
        for(var i = 0 ; i < files.length ; ++i){
            console.log('---',files[i]);
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/pos_input/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                $("div[name='loading']").modal("hide");
                console.log(msg);
                alert(msg.data);
            },
            error:function(msg){
                $("div[name='loading']").modal("hide");
            }
        });  
    }    


    $scope.add_mer_date=moment();
    $scope.add = function(){
    	element_add.modal('show');
		$scope.add_org_no=''
		$scope.add_mer_name=''
		$scope.add_mer_no=''
		$scope.add_pos_no=''
		$scope.add_mer_add=''
		$scope.add_mer_con=''
		$scope.add_mer_tel=''
		$scope.add_mer_mob=''
        $scope.add_status=''
    };

    $scope.add_save = function (){
        if($scope.add_org_no==''||$scope.add_mer_name==''||$scope.add_mer_no==''||$scope.add_pos_no==''||$scope.add_mer_date==''||$scope.add_mer_type==''||$scope.add_status==''){
            alert("输入不能为空！");
        }
	    else{
		    element_add.modal('hide');
            if ($scope.add_mer_date instanceof moment){
                add_date=$scope.add_mer_date.format('YYYYMMDD')
            }else {
                add_date=moment($scope.add_mer_date).format('YYYYMMDD')
            }
		    pos_inputService.add_save({'org_no':$scope.add_org_no,'merchant_name':$scope.add_mer_name,'merchant_no':$scope.add_mer_no,'pos_no':$scope.add_pos_no,'merchant_addr':$scope.add_mer_add,'merchant_contract':$scope.add_mer_con,'merchant_tel':$scope.add_mer_tel,'merchant_mob':$scope.add_mer_mob,'install_date':add_date,'typ':$scope.add_mer_type,'status':$scope.add_status}).success(function (reps){
			    alert(reps.data);
			    load();
		    });
	    };
    };
    $scope.edit_save = function (){
		element_edit.modal('hide');
        var end_date=null
        if ($scope.edit_end_date == null || $scope.edit_end_date == "" ){
            end_date=null;
        }
        else{
            if ($scope.edit_end_date instanceof moment){
            end_date=$scope.edit_end_date.format('YYYYMMDD')
            }else {
            end_date=moment($scope.edit_end_date).format('YYYYMMDD')
            }
        }
        if ($scope.edit_mer_date instanceof moment){
            edit_date=$scope.edit_mer_date.format('YYYYMMDD')
        }else {
            edit_date=moment($scope.edit_mer_date).format('YYYYMMDD')
        }
        pos_inputService.edit_save({'item_id':$scope.item_id,'org_no':$scope.edit_org_no,'merchant_name':$scope.edit_mer_name,'merchant_no':$scope.edit_mer_no,'pos_no':$scope.edit_pos_no,'merchant_addr':$scope.edit_mer_add,'merchant_contract':$scope.edit_mer_con,'merchant_tel':$scope.edit_mer_tel,'merchant_mob':$scope.edit_mer_mob,'install_date':edit_date,'typ':$scope.edit_mer_type,'status':$scope.edit_status,'end_date':end_date}).success(function (reps){
			alert(reps.data);
			load();
		});
    };
    
    $scope.edit = function(item){
		element_edit.modal('show');

		$scope.edit_org_no=item[0]
		$scope.edit_mer_name=item[1]
		$scope.edit_mer_no=item[2]
		$scope.edit_pos_no=item[3]
		$scope.edit_mer_add=item[4]
		$scope.edit_mer_con=item[5]
		$scope.edit_mer_tel=item[6]
		$scope.edit_mer_mob=item[7]
		$scope.edit_mer_date=item[8]
        $scope.edit_mer_type=item[9]
        $scope.edit_status=item[10]
        if (item[11]=="" || item[11]==null){
            $scope.edit_end_date=''
        }
        else{
        $scope.edit_end_date=item[11].toString()
        }
        //$scope.edit_end_date=item[11]
		$scope.item_id=item[12]

    };
    $scope.del = function(item){
		var r=confirm("确定删除？");
		if(r==true){
           pos_inputService.del({'item_id':item[0]}).success(function(resp){
              alert(resp.data);
              load();
           });
        }
        else{alert("取消删除");}
    };

});





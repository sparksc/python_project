
/**
 * atm Controller
 */
ysp.controller('atm_inputController', function($scope,store, $rootScope,atm_inputService,SqsReportService){

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
        SqsReportService.info('atm_input', params).success(function(resp) {
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
    var element_edit = angular.element('#atm_input_edit_modal');
    var element_add = angular.element('#atm_input_add_modal');
  

    $scope.search = function () {
        load();
    };

    $scope.upload_excel = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0)
        {
            alert("请先选择对应的文件内容,再导入!")
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
            url : base_url+"/atm_input/upload/",
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
            }    
        });  
    }    



    $scope.add = function(){
    	element_add.modal('show');
		$scope.add_org_no=''
        $scope.add_atm_no=''
        $scope.add_typ=''
        $scope.add_sub_typ=''
        $scope.add_addr=''
        $scope.add_status=''
    };

    $scope.add_save = function (){
        if($scope.add_org_no==''||$scope.add_atm_no==''||$scope.add_addr==''||$scope.add_typ==''||$scope.add_sub_typ==''||$scope.add_status==''){
            alert("输入不能为空！");
        }
	    else{
		    element_add.modal('hide');
		    atm_inputService.add_save({'org_no':$scope.add_org_no,'atm_no':$scope.add_atm_no,'addr':$scope.add_addr,'typ':$scope.add_typ,'sub_typ':$scope.add_sub_typ,'status':$scope.add_status}).success(function (reps){
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
            }else
            {
                end_date=moment($scope.edit_end_date).format('YYYYMMDD')
            }
        }
	    atm_inputService.edit_save({'item_id':$scope.item_id,'org_no':$scope.edit_org_no,'atm_no':$scope.edit_atm_no,'addr':$scope.edit_addr,'typ':$scope.edit_typ,'sub_typ':$scope.edit_sub_typ,'status':$scope.edit_status,'end_date':end_date}).success(function (reps){
		    alert(reps.data);
			load();
            $scope.edit_end_date=null
		});
    };

    $scope.edit = function(item){
		element_edit.modal('show');
		$scope.item_id=item[7]
		$scope.edit_org_no=item[0]
		$scope.edit_atm_no=item[1]
		$scope.edit_typ=item[2]
		$scope.edit_sub_typ=item[3]
		$scope.edit_addr=item[4]
        $scope.edit_status=item[5]
        //$scope.edit_end_date = item[6].toString()
        if (item[6]=="" || item[6]==null)
        {$scope.edit_end_date = ""}
        else{
            $scope.edit_end_date = item[6].toString()
        }

    };
    $scope.del = function(item){
		var r=confirm("确定删除？");
		if(r==true){
           atm_inputService.del({'item_id':item[5]}).success(function(resp){
              alert(resp.data);
              load();
           });
        }
        else{alert("取消删除");}
    };

});





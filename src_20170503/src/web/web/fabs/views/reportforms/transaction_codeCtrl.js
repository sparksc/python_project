/**
 * transactioncode Controller
 */
function transactioncodeController($scope,store, $filter, $rootScope, SqsReportService,villageinputService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.login_branch_no = $rootScope.user_session.branch_code;
    $scope.cust_search.DATE_ID ;//= moment();
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/transaction_code?export=1"
    $scope.newstaffdata= {};

    $scope.parse_paginfo = function(actions){
        for (var i in actions){
            var action = actions[i];
            var act = action.action;
            var info = action.conversation_id;
            var pairs = info.split("&")
            for(var j in pairs){
                if (pairs[j].indexOf('total_count')!=-1){
                    $scope.total_count = pairs[j].split('=')[1];
                    //console.log(pairs[j]);
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
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
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
            url : base_url+"/villageinput/transaction_upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
             request.setRequestHeader("x-session-token", token);
           },
           success: function(msg){
            console.log(msg);
            alert(msg.data);
            $scope.search(); 
          },
          error: function(msg){
           $("div[name='loading']").modal("hide");
          }
        });
     }



    $scope.search = function() {
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.cur_page = 1;
        $scope.total_count = 0;
        $("div[name='loading']").modal("show");
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/transaction_code?export=1"
        for(var key in $scope.cust_search){
                if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                        params[key]=$scope.cust_search[key];
                        $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
                }
        }
        SqsReportService.info('transaction_code', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";

            } else {
                $scope.tableMessage = "未查询到数据";
            }
         $("div[name='loading']").modal("hide");
        });
    };
    $scope.add = function(){
    $scope.flag_show=false
    console.log($scope.flag_show)
    $scope.newstaffdata={};
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').show();
    $('#villageinput_save_edit_button').hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        if ($scope.newstaffdata[2].length != 8 || isNaN($scope.newstaffdata[2])==true )
        {
            console.log($scope.newstaffdata[2].length)
            console.log(isNaN($scope.newstaffdata[2]))
            alert("开始日期-请填写正确的时间格式")
            return
        }
        if ($scope.newstaffdata[3].length != 8 || isNaN($scope.newstaffdata[3])==true )
        {
            alert("结束日期-请填写正确的时间格式")
            return
        }
        if (isNaN($scope.newstaffdata[4])==true )
        {
            alert("请填写正确的折算率信息")
            return
        }
        if($scope.newstaffdata[0]=="" ||$scope.newstaffdata[1]==""||$scope.newstaffdata[2]==""||$scope.newstaffdata[3]==""||$scope.newstaffdata[4]==""){
            alert("请填写完整的信息")
            return
        }

        nsd["tranid"]=$scope.newstaffdata[0];
        nsd["tranname"]=$scope.newstaffdata[1];
        nsd["begin_dt"]=$scope.newstaffdata[2];
        nsd["end_dt"]=$scope.newstaffdata[3];
        nsd["discount"]=$scope.newstaffdata[4];
        console.log(nsd)
        var nd = {"newdata":nsd};
        $("div[name='loading']").modal("show");
        villageinputService.transaction_save(nd).success(function (reps){
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        }).error(function (reps){
            $("div[name='loading']").modal("hide");
        })
    };
    $scope.to_edit = function(row){
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').hide();
    $scope.flag_show=true
    console.log($scope.flag_show)
    $('#villageinput_save_edit_button').show();
    $scope.newstaffdata[0] = row[0];
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        if ($scope.newstaffdata[2].length != 8 || isNaN($scope.newstaffdata[2])==true )
        {
            alert("开始日期-请填写正确的时间格式")
            return
        }
        if ($scope.newstaffdata[3].length != 8 || isNaN($scope.newstaffdata[3])==true )
        {
            alert("结束日期-请填写正确的时间格式")
            return
        }
        if (isNaN($scope.newstaffdata[4])==true )
        {
            alert("请填写正确的折算率信息")
            return
        }
        if($scope.newstaffdata[0]=="" ||$scope.newstaffdata[1]==""||$scope.newstaffdata[2]==""||$scope.newstaffdata[3]==""||$scope.newstaffdata[4]==""){
            alert("请填写完整的信息")
            return
        }
        nsd["tranid"]=$scope.newstaffdata[0];
        nsd["tranname"]=$scope.newstaffdata[1];
        nsd["begin_dt"]=$scope.newstaffdata[2];
        nsd["end_dt"]=$scope.newstaffdata[3];
        nsd["discount"]=$scope.newstaffdata[4];
        nsd["id"]=$scope.newstaffdata[5];
        var nd = {"newdata":nsd};
        $("div[name='loading']").modal("show");
        villageinputService.transaction_update(nd).success(function (reps){
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        }).error(function (reps){
        $("div[name='loading']").modal("hide");
        });

        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["tranid"]=row[0];
    nsd["id"]=row[5];
    $("div[name='loading']").modal("show");
    var nd = {"newdata":nsd};
        villageinputService.transaction_delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        alert(reps.data)
        });

        }
    };


};

transactioncodeController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','villageinputService','branchmanageService'];

angular.module('YSP').service('transactioncodeController', transactioncodeController);

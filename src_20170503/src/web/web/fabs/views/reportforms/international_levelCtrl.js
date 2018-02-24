/**
 * international_levelController
 */
function international_levelController($scope,$rootScope, $filter, SqsReportService,store,branchmanageService,depappointService,international_levelService) {
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
    $scope.cust_search.login_teller_no = $rootScope.user_session.user_code;
    $scope.cust_search.DATE_ID = moment();
    $scope.newstaffdata = {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.parse_paginfo($scope.data.actions);
            $scope.data = resp;
        });
    };
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/international_level?export=1"+"&DATE_ID="+ $scope.cust_search.SYEAR + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
    $scope.search = function() {
        do_search(); 
    };

    $scope.parse_paginfo = function(actions){

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
    $scope.filterInt = function(value){
        if(/^([0-9]+)$/.test(value))
            return true;
        return false;
    };

    function do_search(){
        $("div[name='loading']").modal("show");
        params = $scope.cust_search;

        if(params["SYEAR"]){
            if(!$scope.filterInt(params["SYEAR"])){
                alert('请输入合法年份,如2016.');
            }
        }

        $scope.data = {};
        params.login_branch_no = $rootScope.user_session.branch_code;
        params.login_teller_no = $rootScope.user_session.user_code;
        $scope.tableMessage = "正在查询";
        $scope.total_count = 0;
        $scope.cur_page = 1;
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/international_level?export=1"+"&DATE_ID="+ $scope.cust_search.SYEAR + "&login_branch_no=" + $rootScope.user_session.branch_code + "&login_teller_no=" + $rootScope.user_session.user_code;
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
                params[key]=$scope.cust_search[key];           
                $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }

        SqsReportService.info('international_level', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    
    $scope.calculate = function(){
        $("div[name='loading']").modal("show");
        international_levelService.calculate({}).success(function(resp){
            $scope.search();
            alert(resp.data);
            $("div[name='loading']").modal("hide");
        });                                                        
    };
   
    $scope.affirm = function(){
        $("div[name='loading']").modal("show");
        international_levelService.affirm({}).success(function(resp){
            $scope.search();
            alert(resp.data);
            $("div[name='loading']").modal("hide");
       }); 
    };
    $scope.change_level = function(row){
         $('#international_level_modal').modal('show');
         $('#international_level_new_add_button').hide();
         $('#international_level_save_edit_button').show();
         console.log(row);
         $scope.newstaffdata[0] = row[6];
         $scope.newstaffdata[1] = row[7];
         console.log($scope.newstaffdata);
    };
    $scope.change_save = function(){
        var nsd = {};
        if($scope.newstaffdata[0] == ''){
            alert("调整等级不能为空!");
            return;
        }
        console.log($scope.newstaffdata);
        nsd["adj_level"]=$scope.newstaffdata[0];
        nsd["item_id"]=$scope.newstaffdata[1];
        console.log(nsd);
        international_levelService.change_save(nsd).success(function (reps){
            $scope.search();
            $('#international_level_modal').modal('hide');
            alert(reps.data)
        });
    };
};

international_levelController.$inject = ['$scope', '$rootScope','$filter', 'SqsReportService','store','branchmanageService','depappointService','international_levelService'];
angular.module('YSP').service('international_levelController', international_levelController);

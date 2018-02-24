/**
 * ckgsplzy Controller
 */
function ckgsplzyController($scope, $attrs, $filter, SqsReportService,branchmanageService,gsgxckService,$rootScope) {

    $scope.init = function (){
        $rootScope.addSubTab(0,'提交','<div ng-include="\'views/report/subMenu/ck.html\'"> </div>',{},false,{'status':'预提交审批'}); 
        $rootScope.addSubTab(1,'存款账号挂钩','<div ng-include="\'views/report/subMenu/ck.html\'"> </div>',{},false,{'status':'正常'}); 
        $rootScope.subTabFocus(1);
    }
    if($attrs.init == 'yes'){
        $scope.init();
        return ;
    }
    $scope.setOrg = function(val){
        $scope.cust_search.org = val

    }
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
   // $scope.cust_search.e_p_OPEN_DATE = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
            $scope.parse_paginfo($scope.data.actions);
        });
    };
    
    $scope.parse_paginfo = function(actions){

        //   console.log(actions);
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

    $scope.search = function() {
        params = $scope.cust_search;
        params['status'] = $scope.status;
        if (params.org){
            params.org_no = params.org.branch_code;
        }
        else{
            params.org_no = null;
        }
        if (params.manager){
            params.manager_no = params.manager.user_name;
        }
        else{
            params.manager_no = null;
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        console.log(params)
        SqsReportService.info('000052', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.parse_paginfo($scope.data.actions);
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
	//}
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
        $scope.model2 =reps.data;
                });
    };
    $scope.find_users2 = function(){
            branchmanageService.users({'branch_id':$scope.top_id}).success(function(reps){
                    $scope.model5 =reps.data;
            });
    };

    function find_branchs(){
	    branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
            $scope.model1=reps.data;
	    })	
    }
    find_branchs();
   
   //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 0;
    $scope.selectall = function(master,data){
        if(master){
            $scope.onefalg =true;
            for(rowvalue in data){
                $scope.choseArr.push(data[rowvalue][prkey]);
            }
        }
        else{
            $scope.onefalg =false;
            $scope.choseArr =[];
        }
    };
    $scope.chkone = function(row,oneflag){
        var hasin = $scope.choseArr.indexOf(row[prkey]);
        if(oneflag&&hasin==-1){
            $scope.choseArr.push(row[prkey])
        }
        if(!oneflag&&hasin>-1){
            $scope.choseArr.pop(row[prkey])
        }
    };
    var element =angular.element(document.getElementById($scope.subTabId)).find('#move_ckgsplzy1');
    //批量移交功能
	$scope.add_start_date = moment().add(1,'days');
	$scope.add_end_date = moment("2099-12-30","YYYY-MM-DD");
    $scope.batch_move = function() {
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择客户信息');
            return;
        }
        console.log($scope.choseArr[0])
        gsgxckService.get_top({'id':$scope.choseArr[0]}).success(function (reps) {
            console.log(reps.data)
            $scope.top_org = reps.data[0].org_no;    
            branchmanageService.branch({'org':$scope.top_org}).success(function (reps) {
                $scope.add_org=reps.data[0].branch_name;
                console.log("element",$rootScope);
                gsgxckService.batch_account_move_sum({'update_key':$scope.choseArr}).success(function (reps) {
                    $scope.total_amount = reps.data.total_amount;
                    $scope.total_count = reps.data.total_count;
                });

                element.modal('show');
                add_start_date = moment().format('YYYY-MM-DD');
                $scope.add_manager = '';
                $scope.top_id = reps.data[0].role_id;
                $scope.find_users2();
            }); 
        });
    };
    $scope.newdata = {};
    $scope.batch_move_before = function(){
        gsgxckService.batch_account_move_before({'update_key':$scope.choseArr}).success(function(resp){
            alert(resp.data);
        });
    };
    $scope.batch_move_delete = function(){
        gsgxckService.batch_account_move_delete({'update_key':$scope.choseArr}).success(function(resp){
            alert(resp.data);
        });
    };

    $scope.do_batch_move = function(){
        $scope.newdata.end_date = moment().format('YYYY-MM-DD');
        $scope.newdata.org_no = $scope.add_org.branch_code;        
        $scope.newdata.manager_no = $scope.add_manager.user_name;
        $scope.newdata.start_date = $scope.add_start_date.format('YYYY-MM-DD');
        $scope.newdata.end_date = $scope.add_end_date.format('YYYY-MM-DD');
        gsgxckService.batch_account_move({'note':$scope.note,'update_key':$scope.choseArr,'from_teller_no':$rootScope.user_session.user_code,'to_teller_no':$scope.add_manager.user_name}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
	        $scope.search();
        });
    };
};

ckgsplzyController.$inject = ['$scope', '$attrs', '$filter', 'SqsReportService','branchmanageService','gsgxckService','$rootScope'];

angular.module('YSP').service('ckgsplzyController', ckgsplzyController);


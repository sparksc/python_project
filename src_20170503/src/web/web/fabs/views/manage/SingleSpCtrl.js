/**
 * SingleSp Controller
 * 单笔分润移交审批
 */
function SingleSpController($scope, $filter, SqsReportService,branchmanageService,accthkService,custHookMagService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.STATUS = '待审批';
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        params = $scope.cust_search;
        console.log(params)
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('SingleSp', params).success(function(resp) {
            $scope.data = resp;
            //$scope.data.header.push("详情");
            console.log($scope.data.header);
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
        $scope.choseArr=[];
    };
    $scope.detail = function(id){
        params ={'BATCH_ID':$scope.data.rows[id][0]}
        SqsReportService.info('accountzy', params).success(function(resp) {
            $scope.detail_data = resp;
            console.log("$scope.detail_data",$scope.detail_data);
            $('#tab_'+ $scope.tabId + '_content').find("#detail_modal").modal("show");
            //if (($scope.detail_data.rows || []).length > 0) {
            //    $scope.tableMessage = "";
            //} else {
            //    $scope.tableMessage = "未查询到数据";
            //}

        });
    };
    $scope.find_users = function(){
        branchmanageService.users({'branch_id':$scope.cust_search.org.role_id}).success(function(reps){
            $scope.model2 =reps.data;
       });
    };
    $scope.find_users2 = function(){
        branchmanageService.users({'branch_id':$scope.add_org.role_id}).success(function(reps){
            $scope.model5 =reps.data;
       });
    };

    var element = angular.element('#custHookBatchMoveModal');
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
    $scope.approve = function() {
        $scope.newdata = {};
        custHookMagService.single_approve({'update_key':$scope.choseArr,'note':$scope.reason,'status':'同意'}).success(function(resp){
            alert(resp.data); 
            add_element.modal('hide');
        });
        //accthkService.approve({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
        //    alert(resp.data);
        //$scope.search();
        //});
    }
    $scope.deny = function() {
        $scope.newdata = {};
        if(!$scope.reason){
            alert('请输入不同意原因!');
            return;
        }
        custHookMagService.single_approve({'update_key':$scope.choseArr,'note':$scope.reason,'status':'不同意'}).success(function(resp){
            alert(resp.data); 
            add_element.modal('hide');
        });

        //accthkService.deny({'newdata':$scope.newdata,'update_key':$scope.choseArr}).success(function(resp){
        //    alert(resp.data);
        //$scope.search();
        //});
    }
    var add_element=angular.element('#branch_add_modal');
    $scope.get=function(){
        if($scope.choseArr.length == 0) 
        {
            alert('请先选择审批信息');
            return;
        }
         add_element.modal('show');
    }
};

SingleSpController.$inject = ['$scope', '$filter', 'SqsReportService','branchmanageService','accthkService','custHookMagService'];
angular.module('YSP').service('SingleSpController', SingleSpController);

/**
 * cdgggxlrck Controller
 */
function cdgggxlrckController($scope, $filter, $rootScope, SqsReportService,cdgggxService,dictdataService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.tableMessage1 = "请输入账号";
    $scope.cust_search = {};
   // $scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        //console.log($rootScope.user_session)
        params = $scope.cust_search;
        //if (params.JGBH){
        //    params.JGBH = params.JGBH.branch_code;
        //}
        //if (params.GLDXBH){
        //    params.GLDXBH = params.GLDXBH.user_name;
        //}
        $scope.data = {};
        $scope.tableMessage = "正在查询";
            params.CHECK_STATUS = 0;
        SqsReportService.info('cdgggxlr1', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    
    $scope.pass = function(row){
        var nsd={};
        nsd["para_id"]=row[13];
        nsd["check_status"]=1;
        nsd["status"]=0;
        var nd = {"newdata":nsd};
    if(confirm("确认通过复核？")){
        cdgggxService.update(nd).success(function (reps){
        $scope.search(); 
        $('#cdgggxlrck_modal').modal('hide');
        });

        }
    };   
    $scope.refuse = function(row){
        var nsd={};
        nsd["para_id"]=row[13];
        nsd["check_status"]=2;
        var nd = {"newdata":nsd};
    if(confirm("确认驳回复核？")){
        cdgggxService.update(nd).success(function (reps){
        $scope.search(); 
        $('#cdgggxlrck_modal').modal('hide');
        });

        }
    };      
    $scope.commit = function(row){
        var nsd={};
        nsd["para_id"]=row[13];
        nsd["check_status"]=0;
        var nd = {"newdata":nsd};
    if(confirm("确认提交？")){
        cdgggxService.update(nd).success(function (reps){
        $scope.search(); 
        $('#cdgggxlrck_modal').modal('hide');
        });

        }
    };
    //全选与单选功能，全选为当前页面,prkey声明主键
    $scope.choseArr=[];
    $scope.oneflag =false;
    $scope.master =false;
    var prkey = 13;
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
    $scope.batch_pass = function(){
        if($scope.choseArr.length == 0) alert('请先选择待复核记录');
        var nd = {"newdata":$scope.choseArr};
        cdgggxService.batch_pass(nd).success(function(reps){
            $scope.search();
        
        });
    }
    $scope.batch_refuse = function(){
        if($scope.choseArr.length == 0) alert('请先选择待复核记录');
        var nd = {"newdata":$scope.choseArr};
        cdgggxService.batch_refuse(nd).success(function(reps){
            $scope.search();
        
        });
    }

    function find_dict(){
    dictdataService.get_dict({'dict_type':'CD_ST'}).success(function (reps) {
        $scope.cd_st=reps.data;
	});
    dictdataService.get_dict({'dict_type':'CD_CK_ST'}).success(function (reps) {
        $scope.cd_ck_st=reps.data;
	});	
    SqsReportService.info('000037',{'staff_code':$rootScope.user_session.user_code}).success(function(resp){
        $scope.user_cms_code = resp.rows[0][3];
    });
    }
    find_dict();

};

cdgggxlrckController.$inject = ['$scope', '$filter', '$rootScope', 'SqsReportService','cdgggxService','dictdataService'];

angular.module('YSP').service('cdgggxlrckController', cdgggxlrckController);

/**
 * large_loss Controller
 */
function staff_relationController($scope, $filter, SqsReportService, staffrelationService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {

        params = {};
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='')params[key]=$scope.cust_search[key]
        }
           // console.log(params);
        SqsReportService.info('000037', params).success(function(resp) {
            $scope.data = resp;
           // console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.to_edit = function(row) {
	$scope.target = row;
	$('#s_r_modal').modal('show');	
    };
    
    $scope.update = function(target) {
        var new_data = {};
        // console.log(target)
        new_data['newdata']=target;
	staffrelationService.update(new_data).success(function(resp) {
         alert(resp.data);
         $('#s_r_modal').modal('hide');
        });                
    };

    $scope.add = function(){
        $scope.newdata = {};
        $scope.ntarget = {};
        $scope.ntarget['is_khjl']='否';
        $scope.ntarget['is_zhgy']='否';
        $scope.ntarget['is_kjzg']='否';
        $scope.ntarget['is_zhhz']='否';
        SqsReportService.info('000038').success(function(resp) {
            $scope.newdata = resp.rows;
       //     console.log($scope.newdata)
	   //if (($scope.data.rows || []).length > 0) {
       //         $scope.tableMessage = "";
       //     } else {
       //         $scope.tableMessage = "未查询到数据";
       //     }
        });
        var modal = $('#s_r_modal1');
        modal.modal('show');
    };
    $scope.add_save = function(ntarget) {
        if(ntarget[0]==null){
            alert('请选择员工！');
        }
        else{
        var t = ntarget[0];
        ntarget['staff_code']=t[0];
       //console.log(ntarget)
	staffrelationService.save(ntarget).success(function(resp) {
         alert(resp.data);
         $('#s_r_modal1').modal('hide');
         $scope.search();
        });                

        }
    };
    $scope.delete = function(row) {
	var del_data={};
    console.log(row)
    del_data['newdata']=row
    staffrelationService.delete(del_data).success(function(resp) {
         alert(resp.data);
         $scope.search();
        });     
    };
};

staff_relationController.$inject = ['$scope', '$filter', 'SqsReportService' ,'staffrelationService'];

angular.module('YSP').service('staff_relationController', staff_relationController);

/**
 * Opindepappoint Controller
 */
function OpindepappointController($scope, $filter, SqsReportService,store,depappointService,gsgxckService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    //$scope.cust_search.d_date = moment().subtract(1,'days');
    $scope.cust_search.d_date = moment();

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    function do_search(){
        params = $scope.cust_search;
        if(params.d_date instanceof moment){
            params.yyrq = params.d_date.format('YYYY-MM-DD');
        }
        else{
            params.yyrq = '';
        }
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        SqsReportService.info('opindepappoint', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };
    $scope.search = function() {
        do_search();
    }

    do_search();

    $scope.pass = function(id,row){
      if(confirm("确认要款项已到？")){
        //todo 增加到t_zjc_gsgx_ck
        newdata={}
        newdata.drrq = moment().format('YYYY-MM-DD');
        newdata.glje1 = 100;
        newdata.ck_type ='1';
        newdata.newflag ='0';
        newdata.glrq2 = '2099-12-31';
        newdata.glrq1 = row[14];
        newdata.jgbh = row[1];
        newdata.dxbh=row[7];
        newdata.dxxh=row[8];
        newdata.gldxbh=row[3];
        newdata.fjdxbh=row[6];
        newdata.dxmc=row[5];
        gsgxckService.save({'newdata':newdata}).success(function(reps1){
            if(reps1.data == 'ok'){
                depappointService.update({'updata':{'para_id':id,'bz':'3'}}).success(function(reps){
                    alert(reps.data);
                    do_search();
                });
            }
            else{
                alert('保存失败');
            }
        });
      } ;
    };
    $scope.notpass = function(id){
      if(confirm("确认款项未到？")){
        depappointService.update({'updata':{'para_id':id,'bz':'1'}}).success(function(reps){
            alert(reps.data);
            do_search();
        });
      } 
    };
};

OpindepappointController.$inject = ['$scope', '$filter', 'SqsReportService','store','depappointService','gsgxckService'];

angular.module('YSP').service('OpindepappointController', OpindepappointController);

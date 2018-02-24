ysp.controller('taskController', function($scope, taskService){
    $scope.customer = $scope.$parent.customer;
    $scope.displayInfo= function(tabName){
        $scope.display_info = tabName;
    };
    $scope.taskList=[],$scope.staskList=[];
    $scope.taskCreditList=[];
    $scope.pend_appList=[];
    $scope.query_task = function(){
        taskService.done_deal().success(function(resp){
            $scope.taskList = resp.data.done_list;
            $scope.taskCreditList=resp.data.credit_table;
        });
    };

    $scope.sutaskList = function(){
        taskService.nodone_deal().success(function(resp){
            $scope.staskList = resp.data.done_list;
            $scope.staskCreditList=resp.data.credit_table;
        });
    };

    $scope.query_pend_app = function(){
        taskService.pend_app().success(function(resp){
            $scope.pend_appList=resp.data;
        });

    }

    $scope.init = function(){
        return;
        //$scope.display_info= "personalInformation";
        //$scope.query_pend_app();
        $scope.query_task();
        $scope.sutaskList();
        window.setInterval(function(){
            //$scope.query_pend_app();
            $scope.query_task();
            $scope.sutaskList();
        },
        9000
        )
    };
    $scope.init();

})
.service('taskService', function($http){
    return {
        done_deal:function(){
            return $http.get(base_url+'/credit/task')
        },
        nodone_deal:function(){
            return $http.get(base_url+'/credit/stask')
        },
        pend_app:function(){
            return $http.post(base_url+'/credit_application/',{'application_status':'暂存'})
        }
    }
});

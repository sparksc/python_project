/**
 * customerInfo Controller
 */
function customerInfoController($scope,$filter,customerInfoService){
    $scope.dict = {
        "first":"首页",
        "next":"下一页",
        "previous":"上一页",
        "last":"末页",
        "release":"释放",
    };
    customerInfoService.info().success(function(resp){
        $scope.data = resp;
    });

    $scope.onAction = function(conversation_id,action){
        customerInfoService.action(conversation_id,action).success(function(resp){
            $scope.data = resp;
        });
    }
};

customerInfoController.$inject = ['$scope','$filter', 'customerInfoService'];

angular.module('YSP').service('customerInfoController', customerInfoController);
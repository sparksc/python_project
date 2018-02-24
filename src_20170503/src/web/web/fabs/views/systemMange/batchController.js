// 跑批
ysp.controller('batchController',function($scope,batchService){

    $scope.batch_begin = function(){
        batchService.batch_begin().success(function(resp){
            alert('跑批成功');
        });
    }
});

ysp.controller('headerController', ['$scope','store', '$rootScope', '$http', function($scope, store, $rootScope, $http) {
    $scope.$on('$includeContentLoaded', function() {
        Layout.initHeader(); // init header
        setTimeout(function(){
            QuickSidebar.init(); // init quick sidebar
        }, 2000)
    });
    $scope.loginOut = function(){
        store.clear();
        $rootScope.is_login=false;
        window.location.reload();
    };


    $scope.password_change = function(){
        $scope.password_change_msg ='';
        if ($scope.new_password_1!=$scope.new_password_2){
            $scope.password_change_msg = "请保持两次密码一致";
            return;
        }
        var data = {'password':$scope.new_password_1};
        $http.post(base_url+'/users/change_password',data).
            success(function(resp) {
                alert(resp);
                angular.element('#logout_modal').modal('hide');
                window.location.reload();
            });
    }
}]);

/**
 * Users Controller
 */

ysp.controller('sysUserController', ['$scope', '$rootScope', 'permissionService', function($scope, $rootScope, permissionService) {
    var load_users = function() {
        permissionService.users({
            'user_name': $scope.user_name
        }).success(function(reps) {
            $scope.users = reps.data;
        });
    };
    $scope.search = function() {
        load_users();
    };

    /** modal process **/
    var element = angular.element('#user_manager_edit_modal');

    $scope.user_groups_selected = [];
    $scope.save = function() {
        permissionService.user_groups_save({
            'user_id': $scope.user_group_role_id,
            'group_ids': $scope.user_groups_selected
        }).success(function(resp) {
            alert(resp.data);
            element.modal('hide');
        });
    };


    $scope.to_edit = function(user) {
        element.modal('show');
        $scope.user_groups_selected = [];
        $scope.modal_user_name = user.name;
        $scope.user_group_role_id = user.role_id;
        permissionService.user_groups(user.role_id).success(function(resp) {
            $scope.modal_user_groups = resp.data;
            angular.forEach($scope.modal_user_groups, function(ug, key) {
                if (ug.user_group_id) {
                    $scope.user_groups_selected.push(ug.user_group_id);
                }
            });
            $scope.search()
        });
    }
}]);
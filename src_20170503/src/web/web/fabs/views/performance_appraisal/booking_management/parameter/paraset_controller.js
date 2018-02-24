/**
 *  *  *  Controller
 *   *   */

ysp.controller('parasetController', ['$scope', '$rootScope', 'parasetService', function($scope, $rootScope,  parasetService){
    var load_parasets = function () {
        parasetService.parasets({}).success(function (reps) {
            $scope.targets = reps.data;
        });
    };
    $scope.search = function () {
        load_parasets();
    };
    
    $scope.to_edit = function(target){
        element.modal('show');
        $scope.edit_rqsc = target.rqsc;
        
    };

    $scope.edit_save = function(){
        parasetService.edit_save({'edit_rqsc':$scope.edit_rqsc}).success(function(resp){
            alert(resp.data);
            element.modal('hide');
            load_parasets();
        });
    };


    var element = angular.element('#edit_modal');
  
    load_parasets();
}]);

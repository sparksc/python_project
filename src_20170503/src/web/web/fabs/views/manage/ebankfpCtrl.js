
/**
 *  ebankfp  Controller
 */
function ebankfpController($scope, $rootScope, $attrs, $filter, SqsReportService,branchmanageService) {
    $scope.init = function (){
        $rootScope.addSubTab(1,'企业网上银行待分配','<div ng-include="\'views/manage/wyfp.html\'"></div>',{},false);
        $rootScope.addSubTab(0,'ETC待分配','<div ng-include="\'views/manage/etcfp.html\'"></div>',{},false);
        $rootScope.subTabFocus(0);
    }
    if($attrs.init == 'yes'){
        $scope.init();
        return;
    }
}

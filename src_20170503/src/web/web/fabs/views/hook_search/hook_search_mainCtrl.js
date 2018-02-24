
/**
 *  HookSearchMain  Controller
 */
function HookSearchMainController($scope, $rootScope, $attrs, $filter, SqsReportService,branchmanageService) {
    $scope.init = function (){
        $rootScope.addSubTab(5,'支付宝快捷归属查询','<div ng-include="\'views/hook_search/AliPaySearch.html\'"></div>',{},false);
        $rootScope.addSubTab(4,'支付宝卡通归属查询','<div ng-include="\'views/hook_search/AliCardSearch.html\'"></div>',{},false);
        $rootScope.addSubTab(3,'丰收E支付归属查询','<div ng-include="\'views/hook_search/EPaySearch.html\'"></div>',{},false);
        $rootScope.addSubTab(2,'企业网上银行归属查询','<div ng-include="\'views/hook_search/CEbkSearch.html\'"></div>',{},false);
        $rootScope.addSubTab(1,'个人网上银行归属查询','<div ng-include="\'views/hook_search/PEbkSearch.html\'"></div>',{},false);
        $rootScope.addSubTab(0,'手机银行归属查询','<div ng-include="\'views/hook_search/MobileSearch.html\'"></div>',{},false);
        $rootScope.subTabFocus(0);
    }
    if($attrs.init == 'yes'){
        $scope.init();
        return;
    }
}

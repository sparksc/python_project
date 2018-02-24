
/**
 *  custrend  Controller
 */
function custrendController($scope, $rootScope, $attrs, $filter, SqsReportService,branchmanageService) {
    $scope.init = function (){
        $rootScope.addSubTab(5,'机具待认定','<div ng-include="\'views/manage/machrend.html\'"></div>',{},false);
        $rootScope.addSubTab(4,'POS待认定','<div ng-include="\'views/manage/posrend.html\'"></div>',{},false);
        $rootScope.addSubTab(3,'第三方存管待认定','<div ng-include="\'views/manage/thirdrend.html\'"></div>',{},false);
        $rootScope.addSubTab(2,'电子银行待认定','<div ng-include="\'views/manage/ebankrend.html\'"></div>',{},false);
        $rootScope.addSubTab(1,'理财客户号待认定','<div ng-include="\'views/manage/lcrend.html\'"></div>',{},false);
        $rootScope.addSubTab(0,'存款客户待认定','<div ng-include="\'views/manage/deprend.html\'"></div>',{},false);
        $rootScope.subTabFocus(0);
    }
    if($attrs.init == 'yes'){
        $scope.init();
        return;
    }
}

/**
 * tparadetail Controller
 */
function tparadetailController($scope,$rootScope, $filter, SqsReportService,tparaService) {
    function init_para(){
        $scope.upmodel_id = "upmodel_Ctl"+$scope.para_type_id;
        $scope.addmodel_id = "addmodel_Ctl"+$scope.para_type_id;
        var str = angular.element("#tab_"+($rootScope.tabIndex-1)+"_content").children("div:eq(0)").attr("ng-include");
        var n = str.indexOf('?');
        if(n>=0){
            //表示从n这个位置一直截取到最后   
             var url_sub=str.substr(n+1).replace("'","");
            //对截取到的字符串进行分割
             var sp_arr=url_sub.split("&");
             //对第一个数组中的值进行分割
             var id_arr=sp_arr[0].split("=");
             $scope.para_type_id = id_arr[1];
        }
        make_excle_url()
    }
    init_para(); 

    function make_excle_url(params){
        var url = rpt_base_url+"/report_proxy/sqs/paradetail";
        var flag = 0
        for(var key in params){
            if(flag==0){
                url = url+"?"+key+"="+params[key];
                flag=2;
            }
            else{
                url = url+"&"+key+"="+params[key];
            }
        }
        url = url + "&export=1";
        console.log(url)
        $scope.excelurl = url
    }

    //查询功能
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        do_search();
    };
   function do_search(){ 
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        params.para_type_id =$scope.para_type_id;
        SqsReportService.info('paradetail', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
            make_excle_url(params)
        });
    };
    do_search();
    //查询功能
    
    //excel导出
    //$scope.excel = function() {
      //  params = $scope.cust_search;
       // params.para_type_id =$scope.para_type_id;
       // SqsReportService.excel('paradetail', params).success(function(resp) {
         //   alert("导出成功")
        //});
    //};
    //添加参数
    $scope.save = function() {
        var element = angular.element('#'+$scope.addmodel_id);
        $scope.newdata = {};
        element.modal('show');
    };
    $scope.do_save = function(){
        var element = angular.element('#'+$scope.addmodel_id);
        var detaildata =$scope.newdata;
        var rowdata = {"row_status":"启用","para_type_id":$scope.para_type_id,"row_start_date":moment().format('YYYY-MM-DD'),"row_end_date":"3000-12-31"};
        tparaService.para_save({'detaildata':$scope.newdata,"rowdata":rowdata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='添加成功'){
                element.modal('hide');
	            do_search();
            }
        });
    };
    var rid =0;
    $scope.change = function(row) {
        var upelement = angular.element('#'+$scope.upmodel_id);
        $scope.updata = {};
        var pheader = $scope.data.para_header;
        for(var i =0;i<pheader.length;i++)
        {
            $scope.updata[pheader[i].para_header_id] = row[i];
        }
        rid = row[row.length-1];
        upelement.modal('show');
    };

    $scope.do_change = function(){
        var upelement = angular.element('#'+$scope.upmodel_id);
        tparaService.detail_update({'updata':$scope.updata,'rid':rid}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
                upelement.modal('hide');
	            do_search();
            }
        });
    };
    //操作
    $scope.change_status = function(row){
        var perkey = row.length-1;
        var updata = {}
        if(row[perkey-1]=='启用')
            updata.row_status ='禁用'
        else
            updata.row_status ='启用'
        updata.id = row[perkey]
        tparaService.row_update({'updata':updata}).success(function(resp){
            alert(resp.data);
            if(resp.data=='修改成功'){
	            do_search();
            }
        });

    };
   $scope.add_header = function(row){
        $rootScope.forward(row[0]+row[1],'views/tpara/tparaheader.html',{'para_type_id':row[perkey]}); 
   };

   $scope.add_para = function(row){
        $rootScope.forward(row[0]+row[1],'views/tpara/tparadetail.html',{'para_type_id':row[perkey]}); 
   };

};

tparadetailController.$inject = ['$scope','$rootScope', '$filter', 'SqsReportService','tparaService'];

angular.module('YSP').service('tparadetailController', tparadetailController);

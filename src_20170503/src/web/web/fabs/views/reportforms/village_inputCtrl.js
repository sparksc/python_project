/**
 * villageinput Controller
 */
function villageinputController($scope,store, $filter, $rootScope, SqsReportService,villageinputService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.DATE_ID = moment();
    $scope.newstaffdata= {};    

    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[2]='';$scope.newstaffdata[3]='';$scope.newstaffdata[4]='';}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[3]=null;
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[4]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[4]=$scope.model3[i].name;     
            }
        } 
    }
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        });
    };
    find_branchs();    
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.ORG_CODE){role_id=$scope.model1[i].role_id;}
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.STAFF_CODE = null;
    }
    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };

    $scope.search = function() {
        params = {};        
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/village_input?export=1";
       
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(params[key] instanceof moment)params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        console.log(params)
        SqsReportService.info('village_input',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/village_input?export=1"+"&DATE_ID="+moment().format('YYYYMMDD');

    $scope.add = function(){
    $scope.newstaffdata={};
    $scope.newstaffdata[0] = moment();
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').show();
    $('#villageinput_save_edit_button').hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["date_id"]=$scope.newstaffdata[0].format('YYYYMMDD');
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["staff_code"]=$scope.newstaffdata[3];
        nsd["staff_name"]=$scope.newstaffdata[4];
        nsd["times"]=$scope.newstaffdata[5];
        console.log(nsd)
        var nd = {"newdata":nsd};
        villageinputService.save(nd).success(function (reps){
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $('#villageinput_modal').modal('show');
    $('#villageinput_new_add_button').hide();
    $('#villageinput_save_edit_button').show();
    $scope.change_name(row[1]);
    a = String(row[0]);
    str = a.substr(0,4)+'-'+a.substr(4,2)+'-'+a.substr(6,2);
    console.log('qwe'+row[3])
    $scope.newstaffdata[0] = moment(str);
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    $scope.newstaffdata[6] = row[6];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["date_id"]=$scope.newstaffdata[0].format('YYYYMMDD');
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["staff_code"]=$scope.newstaffdata[3];
        nsd["staff_name"]=$scope.newstaffdata[4];
        nsd["times"]=$scope.newstaffdata[5];
        nsd["id"]=$scope.newstaffdata[6];
        var nd = {"newdata":nsd};
        villageinputService.update(nd).success(function (reps){
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[6];
    var nd = {"newdata":nsd};
        villageinputService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#villageinput_modal').modal('hide');
        });
        }
    };


};

villageinputController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','villageinputService','branchmanageService'];

angular.module('YSP').service('villageinputController', villageinputController);

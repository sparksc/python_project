/**
 * manaddcom Controller
 */
function manaddcomController($scope,store, $filter, $rootScope, SqsReportService,manscoinputService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_per_input?export=1"
    //$scope.cust_search.e_p_OPEN_DATE = moment();
    $scope.newstaffdata= {};
    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[1]='';$scope.newstaffdata[6]='';$scope.newstaffdata[5]=''}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[1]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[5]=null;
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[6]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[6]=$scope.model3[i].name;     
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
        console.log($rootScope.user_session)
        params = $scope.cust_search;
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/man_per_input?export=1"
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        SqsReportService.info('man_per_input', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
    $scope.newstaffdata={};
    $('#manaddcom_modal').modal('show');
    $('#manaddcom_new_add_button').show();
    $('#manaddcom_save_edit_button').hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["smouth"]=$scope.newstaffdata[1];
        nsd["staff_code"]=$scope.newstaffdata[4];
        nsd["staff_name"]=$scope.newstaffdata[5];
        nsd["org_code"]=$scope.newstaffdata[2];
        nsd["org_name"]=$scope.newstaffdata[3];
        nsd["score"]=$scope.newstaffdata[6];
        nsd["typ"]="得分";
        console.log(nsd)
        var nd = {"newdata":nsd};
        manscoinputService.save(nd).success(function (reps){
        $scope.search(); 
        $('#manaddcom_modal').modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $('#manaddcom_modal').modal('show');
    $('#manaddcom_new_add_button').hide();
    $('#manaddcom_save_edit_button').show();
    $scope.newstaffdata[0] = row[0];
    $scope.newstaffdata[1] = row[1];
    $scope.newstaffdata[2] = row[2];
    $scope.newstaffdata[3] = row[3];
    $scope.newstaffdata[4] = row[4];
    $scope.newstaffdata[5] = row[5];
    $scope.newstaffdata[6] = row[6];
    $scope.newstaffdata[7] = row[7];
    };
    $scope.edit_save = function(){
        var nsd ={};
        console.log($scope.newstaffdata)
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["smouth"]=$scope.newstaffdata[1];
        nsd["staff_code"]=$scope.newstaffdata[4];
        nsd["staff_name"]=$scope.newstaffdata[5];
        nsd["org_code"]=$scope.newstaffdata[2];
        nsd["org_name"]=$scope.newstaffdata[3];
        nsd["score"]=$scope.newstaffdata[6];
        nsd["id"]=$scope.newstaffdata[7];
        var nd = {"newdata":nsd};
        manscoinputService.update(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#manaddcom_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[7];
    var nd = {"newdata":nsd};
        manscoinputService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#manaddcom_modal').modal('hide');
        });
        }
    };

    function find_dict(){
	branchmanageService.get_dict({'dict_type':'CKTYPE'}).success(function (reps) {
        $scope.model3=reps.data;
	});	
    }
    //find_dict();    
    $scope.searchEle = function(){
        imageService.pdfile_query($scope.applicationId,'elec_arch').success(function(resp){
                $scope.pdf_list  = resp.data;      
                console.log(resp.data);
        });
    }
    $scope.upload_excel = function(){
        console.log($scope.tabId)
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        var token = store.getSession("token");
        var form = new FormData();
        console.log(files)
        for(var i = 0 ; i < files.length ; ++i){
            console.log('---',files[i]);
            form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/manaddcom/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                console.log(msg);
                alert(msg.data);
            }    
        });  
    }    



};

manaddcomController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','manscoinputService','branchmanageService'];

angular.module('YSP').service('manaddcomController', manaddcomController);

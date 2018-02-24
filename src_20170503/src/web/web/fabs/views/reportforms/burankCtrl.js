/**
 burank Controller
 */
function burankController($scope,store, $filter, $rootScope, SqsReportService,burankService,branchmanageService) {
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.flag_tdate={};
    $scope.cust_search.tdate = moment();
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/burank?export=1"
    $scope.newstaffdata= {};
    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[2]='';}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[2]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
            }
        } 
    }
    $scope.change_name1 = function(target){
        if(target == null)$scope.newstaffdata[5]='';
        for(var i in $scope.model3){
            if($scope.model3[i].user_name==target){
                $scope.newstaffdata[5]=$scope.model3[i].name;     
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

    $scope.filterInt = function(value){
        if(/^[0-9]+$/.test(value))
            return true;
        return false;
    };
    $scope.search = function() {
        console.log($rootScope.user_session)
        $("div[name='loading']").modal("show");
        if($scope.cust_search.SYEAR && $scope.cust_search.SYEAR instanceof moment){
          $scope.cust_search.SYEAR = $scope.cust_search.SYEAR.format("YYYY");
        }

        params = $scope.cust_search;
        console.log(params);
        $scope.data = {};
        $scope.tableMessage = "正在查询";
        
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/burank?export=1"
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!='' && $scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        
        SqsReportService.info('burank', params).success(function(resp) {
            $("div[name='loading']").modal("hide");
            $scope.data = resp;
            console.log($scope.data)
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };

    $scope.add = function(){
        $scope.newstaffdata={};
        $scope.newstaffdata[0]='';
        $scope.newstaffdata[1]='';
        $scope.newstaffdata[2]='';
        $('#burank_modal').modal('show');
        $('#burank_new_add_button').show();
        $('#burank_save_edit_button').hide();
    };
    
    $scope.save = function(){
        if($scope.newstaffdata[0] == null||$scope.newstaffdata[1]==null||$scope.newstaffdata[2]==null){
            alert("信息未填完全,请检查!");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[0])){
            alert("请输入合法年份!如:2017");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[1])){
            alert("请输入合法数字!");
            return;
        }
        console.log($scope.newstaffdata);
        var nsd ={};
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["srank"]=$scope.newstaffdata[1];
        nsd["remarks"]=$scope.newstaffdata[2];
        var SYEAR = $scope.newstaffdata[0];
        //判断数据库中是否存在syear数据
        params = {'SYEAR':SYEAR};
        SqsReportService.info('burank', params).success(function(resp) {
            $scope.data = resp;
            console.log($scope.data)
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
                $scope.search()
                alert(SYEAR+" 年份的数据已存在");
            }
            else{
                $scope.tableMessage = ""
                console.log(nsd)
                var nd = {"newdata":nsd};
                burankService.save(nd).success(function (reps){
                    $scope.search(); 
                    $('#burank_modal').modal('hide');
                    alert(reps.data);
                });
            }
        });
    };
    $scope.to_edit = function(row){
         $('#burank_edit_modal').modal('show');
         $('#burank_new_add_button').hide();
         $('#burank_save_edit_button').show();
         $scope.newstaffdata[0] = row[0];
         $scope.newstaffdata[1] = row[1];
         $scope.newstaffdata[2] = row[2];
         $scope.newstaffdata[3] = row[3];
         console.log($scope.newstaffdata);
    };
    $scope.edit_save = function(row){
        if($scope.newstaffdata[0]==null||$scope.newstaffdata[1]==null||$scope.newstaffdata[2]==null){
            alert("信息未填完全,请检查!");
            return;
        }
        if(!$scope.filterInt($scope.newstaffdata[1])){
            alert("请输入合法数字!");
            return;
        }
        var nsd ={};
        
        if($scope.newstaffdata[0] instanceof moment){
            $scope.newstaffdata[0]=$scope.newstaffdata[0].format("YYYY");
        }
        else{
            $scope.newstaffdata[0]=$scope.newstaffdata[0];
        }
        console.log($scope.newstaffdata)
        nsd["syear"]=$scope.newstaffdata[0];
        nsd["srank"]=$scope.newstaffdata[1];
        nsd["remark"]=$scope.newstaffdata[2];
        nsd["id"]=$scope.newstaffdata[3];
        var nd = {"newdata":nsd};
        console.log(nd);
        burankService.update({"syear":$scope.newstaffdata[0],"srank":$scope.newstaffdata[1],"remarks":$scope.newstaffdata[2],"id":$scope.newstaffdata[3]}).success(function (reps){
            $scope.search(); 
            $('#burank_edit_modal').modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[3];
    var nd = {"newdata":nsd};
        burankService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        $('#burank_modal').modal('hide');
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
        //console.log($scope.tabId)
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        if(files.length==0) {
            alert("请先选择对应的文件内容,再导入!");
            return;
        }
        $("div[name='loading']").modal("show");
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
            url : base_url+"/burank/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                $scope.search();
                console.log(msg);
                alert(msg.data);
                $("div[name='loading']").modal("hide");
            }    
        });  
    }
};

burankController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','burankService','branchmanageService'];

angular.module('YSP').service('burankController', burankController);

/**
 * villageinput Controller
 */
function reportCreditVillNumController($scope,store, $filter, $rootScope, SqsReportService,branchmanageService,huiPuBranchTargeTService){
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };

    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.newstaffdata= {};    

    $scope.change_name = function(target){
        if(target == null){$scope.newstaffdata[3]='';$scope.newstaffdata[4]='';$scope.newstaffdata[5]='';}
        for(var i in $scope.model1){
            if($scope.model1[i].branch_code==target){
                $scope.newstaffdata[3]=$scope.model1[i].branch_name;     
                branchmanageService.users({'branch_id':$scope.model1[i].role_id}).success(function(reps){
                    $scope.model3 = reps.data;
                    });
                $scope.newstaffdata[4]=null;
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
        $scope.cust_search.SALE_CODE = null;
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
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/report_credit_villNum?export=1";
       
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        console.log(params)
        SqsReportService.info('report_credit_villNum',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
        if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    var add_element=angular.element('#report_credit_villNum__modal');
    var add_button_element=angular.element('#report_credit_villNum_new_add_button')
    var edit_button_element=angular.element('#report_credit_villNum_save_edit_button')
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/report_credit_villNum?export=1";

    $scope.add = function(){
    $scope.edit_flag=false
    $scope.newstaffdata={};
    add_element.modal('show');
    add_button_element.show();
    edit_button_element.hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        if($scope.newstaffdata[0]==null || $scope.newstaffdata[0]==""){
            alert("请填写年份")
            return
        }
        if($scope.newstaffdata[1]==null || $scope.newstaffdata[1]==""){
            alert("请填写月份")
            return
        }
        if($scope.newstaffdata[2]==null || $scope.newstaffdata[2]=="")
        {
            alert("请填写机构号")
            return
        }
        if($scope.newstaffdata[4]==null || $scope.newstaffdata[4]=="")
        {
            alert("请填写报告期已整村授信个数")
            return
        }
        var month_stand=[1,2,3,4,5,6,7,8,9,10,11,12] 
        nsd["syear"]=Number($scope.newstaffdata[0])
        nsd["smonth"]=Number($scope.newstaffdata[1])
        if(month_stand.indexOf(nsd["smonth"])==-1){
            alert("请输入正确的月份")
            return;
        }
        nsd["org_code"]=$scope.newstaffdata[2];
        nsd["org_name"]=$scope.newstaffdata[3];
        nsd["report_creditvill_num"]=($scope.newstaffdata[4] || 0);
        nsd["remark"]=$scope.newstaffdata[5];
        console.log(nsd)
        var nd = {"newdata":nsd};
        huiPuBranchTargeTService.credit_save(nd).success(function (reps){
        $scope.cust_search.syear=Number($scope.newstaffdata[0])
        $scope.cust_search.smonth=Number($scope.newstaffdata[1])
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $scope.edit_flag=true
    add_element.modal('show');
    add_button_element.hide();
    edit_button_element.show();
    $scope.change_name(row[2]);
    a = String(row[0]);
    $scope.newstaffdata[0] = a;
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
        if($scope.newstaffdata[4]==null || $scope.newstaffdata[4]=="")
        {
            alert("请填写报告期已整村授信个数")
            return
        }
 
        nsd["syear"]=Number($scope.newstaffdata[0])
        nsd["smonth"]=Number($scope.newstaffdata[1])
        nsd["org_code"]=$scope.newstaffdata[2];
        nsd["org_name"]=$scope.newstaffdata[3];
        nsd["report_creditvill_num"]=($scope.newstaffdata[4] || 0);
        nsd["remark"]=$scope.newstaffdata[5];
        nsd["id"]=$scope.newstaffdata[6];
        var nd = {"newdata":nsd};
        huiPuBranchTargeTService.credit_update(nd).success(function (reps){
        $scope.cust_search.syear=Number($scope.newstaffdata[0])
        $scope.cust_search.smonth=Number($scope.newstaffdata[1])
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
        
    };
    $scope.delete = function(row){
    if(confirm("确认删除？")){
    var nsd={};
    nsd["id"]=row[6];
    var nd = {"newdata":nsd};
        huiPuBranchTargeTService.delete(nd).success(function (reps){
        //console.log(reps) 
        $scope.search(); 
        add_element.modal('hide');
        });
        }
    };

    $scope.upload_excel = function(){
    var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
    if(files.length==0)
        {
          alert("请先选择对应的文件内容,再导入!");
          return;
          }
        $("div[name='loading']").modal("show");
        var token = store.getSession("token");
        var form = new FormData();
        for(var i = 0 ; i < files.length ; ++i){
        console.log('---',files[i]);
        form.append('files',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
        type: "POST",
        url : base_url+"/huiPu_branchTarget_hander/credit_upload/",
        data: form,
        processData: false,
        contentType: false,
        beforeSend: function(request) {
        request.setRequestHeader("x-session-token", token);
        },
        success: function(msg){
        $("div[name='loading']").modal("hide");
        alert(msg.data);
        },
        error:function(msg){
        $("div[name='loading']").modal("hide");
        }

        });
    }

};

reportCreditVillNumController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','branchmanageService','huiPuBranchTargeTService'];

angular.module('YSP').service('reportCreditVillNumController', reportCreditVillNumController);

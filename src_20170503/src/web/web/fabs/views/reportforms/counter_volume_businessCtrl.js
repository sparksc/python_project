/**
 * villageinput Controller
 */
function counterVolumeBusinessController($scope,store, $filter, $rootScope, SqsReportService,branchmanageService,counterFineAmountService) {
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
        $scope.excelurl = rpt_base_url + "/report_proxy/sqs/counter_volume_business?export=1";
       
        for(var key in $scope.cust_search){
            if($scope.cust_search[key]!=''&&$scope.cust_search[key]!=null){
            params[key]=$scope.cust_search[key];
            if(params[key] instanceof moment)params['DATE_ID']=params['DATE_ID'].format("YYYYMMDD");
            $scope.excelurl = $scope.excelurl + "&"+key+"="+params[key]
            }
        }
        console.log(params)
        SqsReportService.info('counter_volume_business',params).success(function(resp) {
            $scope.data = resp;
         console.log(resp)
        if(resp.rows[0]=='未'){
            alert("未到月末,不能查看")
            resp.rows=''
            $scope.tableMessage = "未查到数据";
            return;
        }
	    if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查到数据";
            }
        });
    }
    var add_element=angular.element('#counter_volume_business__modal');
    var add_button_element=angular.element('#counter_volume_business_new_add_button')
    var edit_button_element=angular.element('#counter_volume_business_save_edit_button')
    $scope.excelurl = rpt_base_url + "/report_proxy/sqs/counter_volume_business?export=1"+"&DATE_ID="+moment().format('YYYYMMDD');

    $scope.add = function(){
    $scope.edit_flag=false
    $scope.show_flag=1
    $scope.newstaffdata={};
    $scope.newstaffdata[0] = moment();
    add_element.modal('show');
    add_button_element.show();
    edit_button_element.hide();
    };
    
    $scope.save = function(){
        console.log($scope.newstaffdata)
        var nsd ={};
        nsd["date_id"]=$scope.newstaffdata[0].format('YYYYMMDD');
        if($scope.newstaffdata[1]==null || $scope.newstaffdata[1]=="")
        {
            alert("请填写机构号")
            return
        }
        if($scope.newstaffdata[3]==null || $scope.newstaffdata[3]=="")
        {
          alert("请填写员工号")
          return
        }
        if($scope.newstaffdata[5]==null||$scope.newstaffdata[5]=="")
        {
            alert("请填写业务量计酬")
            return
        }
        if(Number($scope.newstaffdata[5])<0)
        {
            $scope.newstaffdata[5]=null
            alert("业务量计酬不能为负数")
            return
        }
        if(Number($scope.newstaffdata[5]).toString()=='NaN')
        {
            $scope.newstaffdata[5]=null
            alert("业务量计酬不能为非法字符")
            return
        }
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["sale_code"]=$scope.newstaffdata[3];
        nsd["sale_name"]=$scope.newstaffdata[4];
        nsd["counter_base_work_sal"]=$scope.newstaffdata[5];
        var nd = {"newdata":nsd};
        counterFineAmountService.business_save(nd).success(function (reps){
        $scope.cust_search.DATE_ID=$scope.newstaffdata[0].format('YYYYMMDD');
        alert(reps.data)
        $scope.search(); 
        add_element.modal('hide');
        });
    };
    $scope.to_edit = function(row){
    $scope.edit_flag=true
    $scope.show_flag=2
    add_element.modal('show');
    add_button_element.hide();
    edit_button_element.show();
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
        if($scope.newstaffdata[5]==null||$scope.newstaffdata[5]=="")
        {
            alert("请填写业务量计酬")
            return
        }
        if(Number($scope.newstaffdata[5])<0)
        {
            $scope.newstaffdata[5]=null
            alert("业务量计酬不能为负数")
            return
        }
        if(Number($scope.newstaffdata[5]).toString()=='NaN')
        {
            $scope.newstaffdata[5]=null
            alert("业务量计酬不能为非法字符")
            return
        }
        console.log($scope.newstaffdata)
        nsd["date_id"]=moment($scope.newstaffdata[0]).format('YYYYMMDD');
        nsd["org_code"]=$scope.newstaffdata[1];
        nsd["org_name"]=$scope.newstaffdata[2];
        nsd["sale_code"]=$scope.newstaffdata[3];
        nsd["sale_name"]=$scope.newstaffdata[4];
        nsd["counter_base_work_sal"]=$scope.newstaffdata[5];
        nsd["id"]=$scope.newstaffdata[6];
        var nd = {"newdata":nsd};
        counterFineAmountService.business_update(nd).success(function (reps){
        $scope.cust_search.DATE_ID=moment($scope.newstaffdata[0]).format('YYYYMMDD');
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
        counterFineAmountService.delete(nd).success(function (reps){
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
        console.log('aaaaaaa',form)
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        console.log('sssssssss',form)
        $.ajax({
        type: "POST",
        url : base_url+"/counter_fine_amount/business_upload/",
        data: form,
        processData: false,
        contentType: false,
        beforeSend: function(request) {
        request.setRequestHeader("x-session-token", token);
        },
        success: function(msg){
        $("div[name='loading']").modal("hide");
        alert(msg.data);
        }
        });
    }

};

counterVolumeBusinessController.$inject = ['$scope','store', '$filter', '$rootScope', 'SqsReportService','branchmanageService','counterFineAmountService'];

angular.module('YSP').service('counterVolumeBusinessController', counterVolumeBusinessController);

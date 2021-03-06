/**
 * Hundred Loan  Controller
 */
ysp.controller('loanpublicinputController', function($scope, $rootScope,  handInputService,SqsReportService,loaninputService,branchmanageService){
    $scope.dict = {
        "first": "首页",
        "previous": "上一页",
        "next": "下一页",
        "last": "末页",
        "release": "释放",
    };
    $scope.tableMessage = "请点击查询";
    $scope.cust_search = {};
    $scope.cust_search.date = moment();
    function find_branchs(){
        branchmanageService.branchs({'name':$scope.search_name}).success(function (reps) {
        $scope.model1=reps.data;
        console.log($scope.model1)
        });
    };
    find_branchs();
    $scope.find_users = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.BRANCH_CODE){role_id=$scope.model1[i].role_id;}
        }
        
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model2 = reps.data;
        });
        $scope.cust_search.SALE_CODE = null;
    }
    $scope.find_users2 = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target.org_no){
                role_id=$scope.model1[i].role_id;
                $scope.add_date.org_name=$scope.model1[i].branch_name;
            }
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model3 = reps.data;
        });
        $scope.add_date.rale_no =null;
    }
    $scope.find_users6 = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target){
                role_id=$scope.model1[i].role_id;
                $scope.up_date.org_name=$scope.model1[i].branch_name;
            }
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model4 = reps.data;
            $scope.up_date.rale_no=null
            $scope.up_date.rale_name=''

        });
    }
    $scope.find_users4 = function(target){
        var role_id = 0;
        for(i in $scope.model1){
            if($scope.model1[i].branch_code == target){
                role_id=$scope.model1[i].role_id;
                $scope.up_date.org_name=$scope.model1[i].branch_name;
            }
        }
        branchmanageService.users({'branch_id':role_id}).success(function(reps){
            $scope.model4 = reps.data;
        });
    }
    $scope.find_users3 = function(target){
        for(i in $scope.model3){
            if($scope.model3[i].user_name == target.rale_no){
                $scope.add_date.rale_name=$scope.model3[i].name;
            }
        }
    }
    $scope.find_users5 = function(target){
        for(i in $scope.model4){
            if($scope.model4[i].user_name == target.rale_no){
                $scope.up_date.rale_name=$scope.model4[i].name;
            }
        }
    }

    $scope.onAction = function(conversation_id, action) {
        SqsReportService.action(conversation_id, action).success(function(resp) {
            $scope.data = resp;
        });
    };
    $scope.search = function() {
        $scope.tableMessage = "正在查询";
        params=$scope.cust_search;
        console.log($scope.cust_search,"");
        if(params.date instanceof moment){
            params.date = params.date.format('YYYYMMDD');
        }
        SqsReportService.info('loan_public', params).success(function(resp) {
            $scope.data = resp;
            if (($scope.data.rows || []).length > 0) {
                $scope.tableMessage = "";
            } else {
                $scope.tableMessage = "未查询到数据";
            }
        });
    };


 
    var element_edit = angular.element('#loan_public_edit');
    var element_add = angular.element('#loan_public_add');

    $scope.add = function(){
        $scope.add_date={};
        $scope.add_date.d_rate = moment();
    	element_add.modal('show');
    };
    $scope.add_save = function (){
        if($scope.add_date.d_rate instanceof moment){
            $scope.add_date.d_rate = $scope.add_date.d_rate.format('YYYYMMDD');
        }else {
            $scope.add_date.d_rate = '0000';
        };
        console.log($scope.add_date)
        loaninputService.tsave({'add_date':$scope.add_date}).success(function (resp){
            alert(resp.data);
            $scope.search();
            element_add.modal('hide');
        });
    };

    $scope.del = function(item){
		var r=confirm("确定删除？");
		if(r==true){
           loaninputService.tdelt({'item_id':item[14]}).success(function(resp){
              alert(resp.data);
              $scope.search();
           });
        }
        else{alert("取消删除");}
    };
    
    $scope.edit = function(item){
		element_edit.modal('show');
        $scope.up_date={};
        $scope.up_date.d_rate=item[0]
        $scope.up_date.org_no=item[1]
        $scope.up_date.org_name=item[2]
        $scope.up_date.rale_no=item[3]
        $scope.up_date.rale_name=item[4]
        $scope.up_date.gust_no=item[5]
        $scope.up_date.gust_name=item[6]
        $scope.up_date.public_loan_name=item[7]
        $scope.up_date.public_assuer_name=item[8]
        $scope.up_date.yyzz=item[9]
        $scope.up_date.zzdmz=item[10]
        $scope.up_date.swdjz=item[11]
        $scope.up_date.khxkz=item[12]
        $scope.up_date.jgxydmz=item[13]
        $scope.up_date.id=item[14]
        
        $scope.find_users4(item[1]);
    };
    $scope.search();
    $scope.edit_save = function (){
	    	element_edit.modal('hide');
            loaninputService.tedit({'up_date':$scope.up_date}).success(function(resp){
           
            alert(resp.data);
            $scope.search();
            element_edit.modal('hide');
            });
    };
});





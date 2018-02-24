ysp.controller('mboxController', function($scope, $rootScope,mboxService){
    $scope.Head=['编号','发件人','收件人','发送时间','是否已读','标题','操作'];
    $scope.tableData=[];
    $scope.tableMessage='请点击查询';

    //弹出新邮件窗口
    $scope.mbox_new = function () {
        $scope.new={};
        $scope.new.a={};
        $scope.new.b={};
        //$rootScope.get_current_tab($scope.tabId).find("#a_modal").modal('show');
        angular.element('#a_modal').modal('show');
        $scope.branch();
    }

    //获取所有支行
    $scope.branch = function(){
        mboxService.branch().success(function(resp){
              $scope.branch_list = resp.data;
      })
    };

    //
    $scope.user = function(){
        mboxService.user($scope.user_branch).success(function(resp){
              $scope.user_list = resp.data;
              console.log($scope.user_list);
        })    
    }

    //邮件查询
    $scope.mbox_query = function(){
      mboxService.query().success(function(resp){
              $scope.tableData = resp.data;
              if($scope.tableData.length > 0){
                  $scope.tableMessage='';
              }else{
                  $scope.tableMessage='未查询到数据';
              }
          }
        );
    };

    //邮件发送
    $scope.mbox_add = function(){
        console.log($scope.new);
        mboxService.save($scope.new).success(function(){
            alert("保存成功 ");   
        });
    };

    //邮件查看
    $scope.mbox_detail = function (body,title,id) {
    $scope.title=title;
    $scope.body=body;
    //$rootScope.get_current_tab($scope.tabId).find("#b_modal").modal('show');
    angular.element('#b_modal').modal('show');
    mboxService.update(id).success(function(){
            $scope.mbox_query();
        });
    }
    $scope.mbox_del = function(id){
            if(confirm("确定删除吗？")){
            mboxService.del(id).success(function(){
            $scope.mbox_query();
        });
      }
    }
});

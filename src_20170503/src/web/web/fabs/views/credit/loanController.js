ysp.controller('creditBaseController', function($compile,$scope, $rootScope,loanService ,creditService,industryService,imageService,store,approvalService){
    $scope.imageFileName=['personImage', 'certFrontImage', 'certBackImage'];
    $scope.btn_edit_flag = true;
    $scope.base_info_display = false;
    $scope.money={};
    $scope.data = {
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        product_code:'',
        product_name:'',
        application_id:'',
        status:'',
    };
    $scope.onSubmit = function(){
        $scope.btn_edit_flag = false;
        creditService.submit($scope.data).then(function(resp){
            var application_id = resp.data.data.application_id;
            if(application_id){
                angular.element("div[name='loanBaseForm']").find("input,select,textarea").attr('disabled','disabled');
                alert('提交成功');
            }else{
                alert("数据保存失败");
            }
        });
    }
    //TODO:提交后不能修改
    $scope.onSave = function(d){
           if($scope.data.lend_transaction != null && $scope.data.lend_transaction.transaction_id ){
                 loanService.update($scope.data).success(function(resp){
                       alert(resp.data.msg);
                 });
           }else{
                 loanService.save($scope.data).success(function(resp){
                       loanService.query($scope.data.transaction_info.transaction_id).success(function(rsp){
                              $scope.data.lend_transaction=rsp.data.lend_transaction;
                              alert(resp.data.msg);
                       });
                 });
           }
           $scope.btn_edit_flag = true;
    };
    $scope.onEdit = function(){
        $scope.btn_edit_flag = true;
        angular.element("div[name='loanBaseForm']").find("input,select,textarea").removeAttr('disabled');
    };

    /************************ 审批使用 *************************/
    $scope.approveActivityFlag=false;
    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            $scope.approveActivityFlag=true;
            $scope.btn_edit_flag=false;
            angular.element("div[name='loanBaseForm']").find("input,select,textarea").attr('disabled','disabled');
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                // 设置默认值
                if(resp.data.transaction_info.currency_code == null){
                    $scope.data.transaction_info.currency_code='CNY';
                }
                if(resp.data.application_info.repayment_method == null){
                    $scope.data.application_info.repayment_method='一次性还款';
                }
                if(resp.data.application_info.agreement_rate == null){
                    $scope.data.application_info.agreement_rate='否';
                }
                if(resp.data.application_info.handle_branch == null){
                    $scope.data.application_info.handle_branch=store.getSession('branch_code')+'-'+store.getSession('branch_name');
                }
                if(resp.data.application_info.handle_person == null){
                    $scope.data.application_info.handle_person=store.getSession('user_name')+'-'+store.getSession('name');
                }
                if(resp.data.application_info.purpose_type == null){
                     $scope.data.application_info.purpose_type='经营周转';
                }
                if(resp.data.application_info.apply_date == null){
                    var d = new Date();
                    var Y = d.getFullYear();
                    var M = d.getMonth()+1 ; if (M<10) M='0'+M
                    var D = d.getDate();if (D < 10) D='0'+D
                    $scope.data.application_info.apply_date=Y + '-' + M + '-' + D;
                }
                if(resp.data.application_info.purpose_type == null){
                    $scope.data.application_info.purpose_type="经营周转";
                }
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                $scope.end_date = resp.data.end_date
                $scope.data.product_name = resp.data.product.name;
                //$scope.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.ltSelected = false;
            });

            $scope.base_info_display = true;
            $scope.money.amount = app_money_ch($scope.data.transaction_info.amount)
        
        }
    }
    // -----------------------  行业类别
    $scope.initIndustry = function(){                                                                                        $scope.industry_top=null;
       $scope.industry_big=null;
       $scope.industry_mid=null;
       $scope.industry_small=null;
       $scope.industry_topList=[];
       industryService.query('_').success(function(resp){ 
           $scope.industry_topList = resp.data;                                                                   
       });
    }       
                
    $scope.industry_select=function(para,which){
       if (which == 'big'){
            industryService.query(para.substring(0,1)+'__').success(function(resp){
                $scope.industry_bigList = resp.data;                                                    
                $scope.industry_top=para;                                                                                  
                $scope.industry_big=null;                                                                  
                $scope.industry_mid=null; 
                $scope.industry_small=null;                                                                         
            });      
            $scope.industry_midList = null;
            $scope.industry_smallList=null;                                                                           
        }else if(which == 'mid'){
            industryService.query(para.substring(0,3)+'_').success(function(resp){
                $scope.industry_midList = resp.data;                                                                  
                $scope.industry_big=para;                                                                             
                $scope.industry_mid=null;                                                                              
                $scope.industry_small=null;
            });
            $scope.industry_smallList=null;
        }else if(which == 'small'){
            industryService.query(para.substring(0,4)+'_').success(function(resp){
                $scope.industry_smallList = resp.data;
                $scope.industry_mid=para;
                $scope.industry_small=null;
             });
        }else{
            $scope.industry_small=para;
        }
    }
    $scope.info();
    $scope.approve = function(form_data){
        /* 使用application_status，有错误请查找*/
        approvalService.approve_flag($scope.applicationId,{'application_status':$scope.application_status}).success(function(resp){
            if(resp.data.error){
                alert(resp.data.error);
            }else {
                approvalService.approve($scope.applicationId, {'comment_type': '同意', 'comment': $scope.result})
                    .success(function (resp) {
                        if (resp.data.success) {
                            $scope.submitedFlag = true;
                            $scope.next_step = resp.data.next_step;
                            $("#tab_" + $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                        } else {
                            alert(resp.data.msg);
                        }
                    });

            }
        });
    }
    $scope.reject = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'不同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                alert('提交成功'); 
            });
    };
    // 确认种类后管理相关内容标签页
    //$scope.base_info_display = false; 
    $scope.relative_info_tabId = undefined;

   function getObjectURL(file) {
        var url = null ; 
        if (window.createObjectURL!=undefined) { // basic
            url = window.createObjectURL(file) ;
        } else if (window.URL!=undefined) { // mozilla(firefox)
            url = window.URL.createObjectURL(file) ;
        } else if (window.webkitURL!=undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file) ;
        }
        return url ;
    };

    $scope.btmConfirm = function(){
        //$scope.ltSelected = false;
        if($scope.relative_info_tabId != undefined){
            $scope.subTabClose($scope.relative_info_tabId);
            $scope.relative_info_tabId = undefined;
        }
        if($scope.loan_type_code != '#'){
            //$scope.base_info_display = true;
            $scope.LoanPage='views/credit/loan/'+$scope.loan_type_page+'.html'
        }else{
            $scope.base_info_display = false;
        } 
        //TODO:使用工厂模式代替
        if($scope.loan_type_code == '101'){
            $scope.relative_info_tabId = $scope.addSubTab('房产信息', '<div ng-include="'+'\'views/credit/LoanTypesInfo/reality.html' +'\'" ng-controller="realityController" ></div>', {}, false);
        }
    };
    $scope.btmClose = function(){ 
        $scope.loan_type_code = undefined;
        $scope.loan_type_name = undefined;
        $scope.base_info_display = false; 
        $scope.data.loan={};
        $scope.data.lendtran={};
    };
    /*****************************影像数据**********************************/
    $scope.selectImage = function(fileInputElementName){
        var file = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
                    .find("input[type='file'][name='"+fileInputElementName+"']");
        file.click();
        file.change(function(){
            var fileObj = $(this).get(0).files[0];
            fileObj.name = fileInputElementName;
            var src = getObjectURL(fileObj);
            $(this).next().attr('src',src);
        });
    }
    //格式转换
    //日期
    $scope.apply_date = function(data){
        $scope.data.application_info.apply_date =app_date_ch(data);
    } 
    $scope.first_drawing_date= function(data){
        $scope.data.application_info.first_drawing_date=app_date_ch(data);
    } 
    $scope.first_rep_date= function(data){
        $scope.data.application_info.first_rep_date=app_date_ch(data);
    }
    $scope.discount_deadline = function(data){
        $scope.data.lend_transaction.discount_deadline=app_date_ch(data);
    }
    $scope.discount_firstend= function(data){
        $scope.data.lend_transaction.discount_firstend=app_date_ch(data);
    }
    $scope.from_date= function(data){
        $scope.data.lend_transaction.from_date=app_date_ch(data);
    }
    $scope.thur_date= function(data){
        $scope.data.lend_transaction.thur_date=app_date_ch(data);
    } 
    $scope.trade_date= function(data){
        $scope.data.lend_transaction.trade_date=app_date_ch(data);
    }
    //金额
    $scope.amount = function(data){ 
        $scope.data.transaction_info.amount = data;
        $scope.money.amount = app_money_ch(data);
    }

});
ysp.controller('loanBaseController', function($compile,$scope, $rootScope,loanService ,creditService,industryService,imageService,store,contractService,approvalService){
    $scope.imageFileName=['personImage', 'certFrontImage', 'certBackImage'];
    $scope.btn_edit_flag = true;
    $scope.base_info_display = false;
    $scope.end_loan_display = false;
    $scope.money={};
    $scope.data = {
        contract:{},
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        lend_transaction:{},
        product_code:'',
        product_name:'',
        application_id:'',
        status:'',
    };
    function showIndustry(ls){
                industryService.query('_').success(function(resp){                                                    
                    $scope.industry_topList = resp.data;                                                               
                });                                                                                                   
                industryService.query(ls[0].substring(0,1)+'__').success(function(resp){                                
                    $scope.industry_bigList = resp.data;                                                                
                })
                industryService.query(ls[1].substring(0,3)+'_').success(function(resp){                                         
                    $scope.industry_midList = resp.data;                                                                      
                })
                industryService.query(ls[2].substring(0,4)+'_').success(function(resp){                                           
                    $scope.industry_smallList = resp.data;                                                                  
                })
                 //setInterval("myInterval()",1000); 为了让其显示正常
                 window.setTimeout(function(){
                 $scope.industry_top=ls[0];      
                 $scope.industry_big=ls[1];
                 $scope.industry_mid=ls[2];
                 $scope.industry_small=ls[3];
                 },1000);

    }

    $scope.showEnd = function(){
        loanService.query($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             $scope.data.contract=resp.data.contract;
             if($scope.data.lend_transaction && $scope.data.lend_transaction.transaction_id){
                contractService.list_query($scope.data.lend_transaction.transaction_id).success(function(resp){
                    $scope.havecontractList = resp.data.contracts
                            
                });
                 if($scope.data.lend_transaction.industry_1){
                    var ls=[];
                    ls.push($scope.data.lend_transaction.industry_1);
                    ls.push($scope.data.lend_transaction.industry_2);
                    ls.push($scope.data.lend_transaction.industry_3);
                    ls.push($scope.data.lend_transaction.industry_4);
                    showIndustry(ls);
                 }else{
                     //读取客户行业分类
                     industryService.query_cust($scope.customer.id).success(function(resp){
                        var ls = resp.data;
                        if(ls.length == 4 && ls.indexOf(null) == -1){
                            showIndustry(ls); 
                        }
                        else{
                            $scope.initIndustry();
                        }
            
                    });
                }
                
            }else{
                    //读取客户行业分类
                industryService.query_cust($scope.customer.id).success(function(resp){
                    var ls = resp.data;
                    if(ls.length == 4 && ls.indexOf(null) == -1){
                        showIndustry(ls) 
                    }
                    else{
                        $scope.initIndustry();
                    }
            
                });
            }
        });
        $scope.btn_edit_flag=false;
        $scope.approveActivityFlag=true;
        angular.element("div[name='loanApplicationForm']").find("input,select,textarea").attr('disabled','disabled');
        $scope.end_loan_display = true; 

    };

    $scope.onSubmit = function(){
       loanService.submit($scope.data).success(function(resp){
            alert(resp.data.msg);
            angular.element("div[name='loanApplicationForm']").find("input,select,textarea").attr('disabled','disabled');
       });     
    };
    //TODO:提交后不能修改
    $scope.onSave = function(d){
           if($scope.data.lend_transaction != null && $scope.data.lend_transaction.transaction_id ){
                 loanService.update($scope.data).success(function(resp){
                       alert(resp.data.msg);
                 });
           }else{
                 loanService.save($scope.data).success(function(resp){
                       loanService.query($scope.data.transaction_info.transaction_id).success(function(rsp){
                              $scope.data.lend_transaction=rsp.data.lend_transaction;
                              alert(resp.data.msg);
                       });
                 });
           }
           angular.element("div[name='loanApplicationForm']").find("input,select,textarea").attr('disabled','disabled');
           $scope.btn_edit_flag = false;
    };

    $scope.onEdit = function(){
        angular.element("div[name='loanApplicationForm']").find("input,select,textarea").removeAttr('disabled');
        $scope.btn_edit_flag = true;
    };
    $scope.onContract = function(){
         if($scope.data.lend_transaction.transaction_id){
            contractService.save($scope.data).success(function(resp){
                  alert('生成成功')
                  $scope.data.contract=resp.data.contract;
            });  
         }else{
            alert('请先录入必要信息')
         }
    };

    $scope.onCancel = function(){
        $scope.btn_edit_flag = false;
        $scope.data.loan={};
        $rootScope.tabClose($scope.tabId);
    };
    
    
    /************************ 审批使用 *************************/
    //TODO:ng-include的内容如何更好的通讯？ 使用element获取的scope并不能获得该方法
    $scope.approveActivityFlag=false;
    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            //$scope.loan_type_name = $scope.product_name;
                        // 获取申请信息
            $scope.loan_type_page = $scope.product_page
            $scope.submitedFlag = false;
            
            $scope.LoanPage='views/credit/LoanTypesInfo/'+$scope.loan_type_page+'.html'
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                // 设置默认值
                if(resp.data.transaction_info.currency_code == null){
                    $scope.data.transaction_info.currency_code='CNY';
                }
                if(resp.data.application_info.repayment_method == null){
                    $scope.data.application_info.repayment_method='一次性还款';
                }
                if(resp.data.application_info.agreement_rate == null){
                    $scope.data.application_info.agreement_rate='否';
                }
                if(resp.data.application_info.handle_branch == null){
                    $scope.data.application_info.handle_branch=store.getSession('branch_code')+'-'+store.getSession('branch_name');
                }
                if(resp.data.application_info.handle_person == null){
                    $scope.data.application_info.handle_person=store.getSession('user_name')+'-'+store.getSession('name');
                }
                if(resp.data.application_info.purpose_type == null){
                     $scope.data.application_info.purpose_type='经营周转';
                }
                if(resp.data.application_info.apply_date == null){
                    var d = new Date();
                    var Y = d.getFullYear();
                    var M = d.getMonth()+1 ; if (M<10) M='0'+M
                    var D = d.getDate();if (D < 10) D='0'+D
                    $scope.data.application_info.apply_date=Y + '-' + M + '-' + D;
                }
                if(resp.data.application_info.purpose_type == null){
                    $scope.data.application_info.purpose_type="经营周转";
                }
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                $scope.end_date = resp.data.end_date
                $scope.data.product_name = resp.data.product.name;
                //$scope.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.ltSelected = false;
                    // 该状态从sidebar 传过来
                $scope.showEnd(); 
                $scope.money.amount = app_money_ch($scope.data.transaction_info.amount)

            });

         }
    }
    // -----------------------  行业类别
    $scope.initIndustry = function(){                                                                                        $scope.industry_top=null;
       $scope.industry_big=null;
       $scope.industry_mid=null;
       $scope.industry_small=null;
       $scope.industry_topList=[];
       industryService.query('_').success(function(resp){ 
           $scope.industry_topList = resp.data;                                                                   
       });
    }       
                
    $scope.industry_select=function(para,which){
       if (which == 'big'){
            industryService.query(para.substring(0,1)+'__').success(function(resp){
                $scope.industry_bigList = resp.data;                                                    
                $scope.industry_top=para;                                                                                  
                $scope.industry_big=null;                                                                  
                $scope.industry_mid=null; 
                $scope.industry_small=null;                                                                         
            });      
            $scope.industry_midList = null;
            $scope.industry_smallList=null;                                                                           
        }else if(which == 'mid'){
            industryService.query(para.substring(0,3)+'_').success(function(resp){
                $scope.industry_midList = resp.data;                                                                  
                $scope.industry_big=para;                                                                             
                $scope.industry_mid=null;                                                                              
                $scope.industry_small=null;
            });
            $scope.industry_smallList=null;
        }else if(which == 'small'){
            industryService.query(para.substring(0,4)+'_').success(function(resp){
                $scope.industry_smallList = resp.data;
                $scope.industry_mid=para;
                $scope.industry_small=null;
             });
        }else{
            $scope.industry_small=para;
        }
    }
    $scope.info();
    $scope.approve = function(form_data){
        /* 使用application_status，有错误请查找*/
        approvalService.approve_flag($scope.applicationId,{'application_status':$scope.application_status}).success(function(resp){
            if(resp.data.error){
                alert(resp.data.error);
            }else{

                approvalService.approve($scope.applicationId, {'comment_type':'同意', 'comment':$scope.result})
                    .success(function(resp){
                        if(resp.data.success){
                            $scope.submitedFlag = true;
                            $scope.next_step=resp.data.next_step;
                            $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                        }else if(resp.data.msg){
                            alert(resp.data.msg);
                        }else{
                            alert("错误");
                        }
                    });
            }
        });

    }
    $scope.reject = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'不同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                alert('提交成功'); 
            });
    };
    // 确认种类后管理相关内容标签页
    //$scope.base_info_display = false; 
    $scope.relative_info_tabId = undefined;

   function getObjectURL(file) {
        var url = null ; 
        if (window.createObjectURL!=undefined) { // basic
            url = window.createObjectURL(file) ;
        } else if (window.URL!=undefined) { // mozilla(firefox)
            url = window.URL.createObjectURL(file) ;
        } else if (window.webkitURL!=undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file) ;
        }
        return url ;
    };
    /*****************************影像数据**********************************/
    $scope.selectImage = function(fileInputElementName){
        var file = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
                    .find("input[type='file'][name='"+fileInputElementName+"']");
        file.click();
        file.change(function(){
            var fileObj = $(this).get(0).files[0];
            fileObj.name = fileInputElementName;
            var src = getObjectURL(fileObj);
            $(this).next().attr('src',src);
        });
    }
    //格式转换
    //日期
    $scope.apply_date = function(data){
        $scope.data.application_info.apply_date =app_date_ch(data);
    } 
    $scope.first_drawing_date= function(data){
        $scope.data.application_info.first_drawing_date=app_date_ch(data);
    } 
    $scope.first_rep_date= function(data){
        $scope.data.application_info.first_rep_date=app_date_ch(data);
    }
    $scope.discount_deadline = function(data){
        $scope.data.lend_transaction.discount_deadline=app_date_ch(data);
    }
    $scope.discount_firstend= function(data){
        $scope.data.lend_transaction.discount_firstend=app_date_ch(data);
    }
    $scope.from_date= function(data){
        $scope.data.lend_transaction.from_date=app_date_ch(data);
    }
    $scope.thur_date= function(data){
        $scope.data.lend_transaction.thur_date=app_date_ch(data);
    } 
    $scope.trade_date= function(data){
        $scope.data.lend_transaction.trade_date=app_date_ch(data);
    }
    //金额
    $scope.amount = function(data){ 
        $scope.data.transaction_info.amount = data;
        $scope.money.amount = app_money_ch(data);
    }

    //
    //
    // 合同 借据增加
    //
    //
    $scope.havecontractList=[];
    $scope.contractList=[];
    $scope.con=[];
    $scope.contract_flag = true;
    $scope.addContract =  function(){
        contractService.querycontract($scope.$parent.applicationId).success(function(resp){
           $scope.con=resp.data;
            if($scope.con.length==0){
                alert("请先生成担保合同");
            }else if($scope.data.lend_transaction && $scope.data.lend_transaction.transaction_id){
                contractService.save($scope.data).success(function(resp){
                    $scope.data.contract=resp.data.contract;
                    var item = new Object();
                    var index = $scope.contractList.length;
                    item.contract_id = resp.data.contract.contract_id;
                    item.contract_no = resp.data.contract.contract_no
                    $scope.contractList.push(item);
                    var tr_html = "<tr>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"true\" ng-model = \"contractList["+index+"].contract_no \" /> </td>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].begin_date \"/> </td>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].end_date \"/> </td>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].amount \"/> </td>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].is_credit_card \"/> </td>"+
                        "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].debt_rate \"/> </td>"+
                        //"<td> <button ng-click=\"saveContrat("+index+")\"> 保存 </button> <button > 修改 </button> </td>"+
                        "</tr>";

                    var contentTemplate = angular.element(tr_html);
                    var contentElement = $compile(contentTemplate)($scope);
                    angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find('#addContractId').append(contentElement);

                });
            }else{
                alert('请先填写放款信息');
            }
        });


    }
    $scope.saveContract = function(){
        for(var i in $scope.havecontractList){
            $scope.contractList.push($scope.havecontractList[i]);
        }
        contractService.list_update({'contracts':$scope.contractList}).success(function(resp){
            alert('更新成功');
        });
        
    }
    $scope.changeContract = function(){
        $scope.contract_flag = false;
    }
    
});
ysp.controller('loanController', function($compile,$scope, $rootScope,loanService ,creditService,industryService,imageService,store,contractService,investReportService){
    $scope.data = {
        contract:{},
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        lend_transaction:{},
        product_code:'',
        product_name:'',
        application_id:'',
        status:'',
    };
    $scope.onSubmit = function(){
        loanService.loan($scope.data).success(function(resp){
              console.log(resp)
              alert(resp.data.msg);
       });
   };
    angular.element("div[name='loanForm']").find("input,select,textarea").attr('disabled','disabled');
    /************************ 审批使用 *************************/
    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            $scope.loan_type_page = $scope.product_page
            $scope.LoanPage='views/credit/LoanTypesInfo/'+$scope.loan_type_page+'.html'
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                // 设置默认值
                if(resp.data.transaction_info.currency_code == null){
                    $scope.data.transaction_info.currency_code='CNY';
                }
                if(resp.data.application_info.repayment_method == null){
                    $scope.data.application_info.repayment_method='一次性还款';
                }
                if(resp.data.application_info.agreement_rate == null){
                    $scope.data.application_info.agreement_rate='否';
                }
                if(resp.data.application_info.handle_branch == null){
                    $scope.data.application_info.handle_branch=store.getSession('branch_code')+'-'+store.getSession('branch_name');
                }
                if(resp.data.application_info.handle_person == null){
                    $scope.data.application_info.handle_person=store.getSession('user_name')+'-'+store.getSession('name');
                }
                if(resp.data.application_info.purpose_type == null){
                     $scope.data.application_info.purpose_type='经营周转';
                }
                if(resp.data.application_info.apply_date == null){
                    var d = new Date();
                    var Y = d.getFullYear();
                    var M = d.getMonth()+1 ; if (M<10) M='0'+M
                    var D = d.getDate();if (D < 10) D='0'+D
                    $scope.data.application_info.apply_date=Y + '-' + M + '-' + D;
                }
                if(resp.data.application_info.purpose_type == null){
                    $scope.data.application_info.purpose_type="经营周转";
                }
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                $scope.end_date = resp.data.end_date
                $scope.data.product_name = resp.data.product.name;
                //$scope.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.showEnd(); 
            });

         }
    }
    $scope.loan_print = function(form_data){
        loanService.loan_print(form_serializable(document.getElementById(form_data))).success(function(resp){
            $scope.loan_static_path = resp.data;
            window.setTimeout(function(){
                var iframe = document.getElementById('print_frame');
                iframe.contentWindow.print();
            },5000);

        });
    };
    $scope.showEnd = function(){
        loanService.query($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             $scope.data.contract=resp.data.contract;
       });
    }
    $scope.info();
});
ysp.controller('realityController', function($scope){
    $scope.data={};
    $scope.editFlag = true;
    $scope.save = function(){
    };
    $scope.edit = function(){ };
    $scope.cancel = function(){ };
});


ysp.controller('realityController', function($scope){
    $scope.data={};
    $scope.editFlag = true;
    $scope.save = function(){
    };
    $scope.edit = function(){ };
    $scope.cancel = function(){ };
});

// 调查报告
ysp.controller('reportController',function($scope,investReportService){
    application_id=$scope.$parent.applicationId;
    investReportService.get(application_id).success(function(resp){
            if(resp.data.success){
                document.getElementById("iframe").src = resp.data.src;
            }
 
    });
    $scope.openIt = function(){
       investReportService.save({'application_id':application_id}).success(function(resp){
            if(resp.data.success){
                document.getElementById("iframe").src = resp.data.src;
            }else{
                alert(resp.data.msg);
            }
       });
   }
   $scope.submit = function(){
       investReportService.submit({'application_id':application_id}).success(function(resp){
            alert(resp.data.msg);
       });
   }
});



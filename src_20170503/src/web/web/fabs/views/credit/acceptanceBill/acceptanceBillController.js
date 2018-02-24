ysp.controller('accBillManagerController', function($scope, $rootScope, creditService, companyInformationService,CustomerSearchService){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus='新增申请';
    /* Query Application */
    $scope.tableHead=['申请书号','客户名称', '业务品种', '主要担保方式', '申请状态', '币种', '金额', '申请人', '申请机构', '操作'];
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.queryApplication=function(){
          $scope.cust_type='company'
          $scope.lend_type='007'
          creditService.query(
                $scope.applicationStatus,
                $scope.cust_type,
                $scope.queryCond.cust_name,
                $scope.queryCond.guarantee_type,
                $scope.lend_type,
                $scope.queryCond.ld_ratio,
                $scope.queryCond.start_date,
                $scope.queryCond.end_date
            ).success(function(resp){
                $scope.tableData = resp.data;
                console.log($scope.tableData)
                if($scope.tableData.length > 0){
                    $scope.tableMessage='';
                }else{
                    $scope.tableMessage='未查询到数据';
                }
            }
        );

    }

    $scope.init = function(){
        $scope.queryApplication();
    };
    
    /* New Application */
    $scope.newApplication = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        $scope.confirmBtnDisabled = false;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    };

    // Customer Search
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = { 'cust_name':'',};
    $scope.chosenCust = null;
    $scope.searchCustomer = function(){
        CustomerSearchService.queryroleparty($rootScope.user_session).success(function(resp){
            $scope.custTableData =  resp.data.party;

        });
    };
    $scope.choseCustomer = function(cust, $event){
        $scope.chosenCust = cust;
        var obj = event.srcElement;
        var oTr = obj.parentNode;
        var tableObj = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content'))
                        .find("table[name='custListTable']")[0];
        for(var i=1; i<tableObj.rows.length; i++){ 
            tableObj.rows[i].style.backgroundColor = "";   
            tableObj.rows[i].tag = false;   
        }
        oTr.style.backgroundColor = "#87CEFA";   
    };

    $scope.custSearchConfirm = function(){
        $scope.confirmBtnDisabled = true;
        if($scope.chosenCust == null){alert('请先选择申请的客户');};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');

        var cust_id = $scope.chosenCust.no;
        var cust_name = $scope.chosenCust.name;
        var tabName = cust_name+'的承兑汇票申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/acceptanceBill/preLoan.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust,'apply_type':'新增'});
    };

        $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };
      /* Application Detail */
    $scope.applicationDetail = function(data){
            var cust_name = data.party.name;
            var tabName = cust_name+'的汇票申请详情';
            var htmlContent = '<div ng-include="'+'\'views/credit/pageDistribute/index.html' +'\'" ></div>';
            var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':data.party,'application_status':data.activity_name,'activity_page':data.activity_page,'activity_status':data.activity_status,'applicationId':data.id,'product_code':'007','product_name':'承兑汇票签发','role':data.role});
            var applicationScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).scope();
    };
})
ysp.controller('accBillPreController', function($scope, $rootScope, creditService){
     $scope.pre_apply={};
     $scope.pre_apply.party_id=$scope.customer.id
     $scope.pre_apply.no=$scope.customer.no;
     $scope.pre_apply.name=$scope.customer.name;
     $scope.pre_apply.loan_type='签发承兑汇票';
     $scope.pre_apply.main_gua='质押';
     $scope.pre_apply.bill_type='全额';
     $scope.pre_apply.bill_kind='纸票';
     $scope.pre_apply.loan_type_code='007';
     $scope.term  = function(data){
        if($scope.pre_apply.bill_kind=='纸票' && data*1 > 6){
            alert('期限需小于6个月');
            $scope.pre_apply.term = '';
        }else if($scope.pre_apply.bill_kind=='电票' && data*1 > 12){
            alert('期限需小于12个月');
            $scope.pre_apply.term = '';
        }
     }
     $scope.onSubmit = function(){
           creditService.save($scope.pre_apply).success(function(resp){
               alert('提交成功');
               angular.element("div[name='acceptForm']").find("button,input,select,textarea").attr('disabled','disabled');
           });
     }
});

ysp.controller('accBillApplicationController', function($scope, $rootScope,loanService ,creditService,industryService,imageService,store,contractService,approvalService, BillService){
   $scope.imageFileName=['personImage', 'certFrontImage', 'certBackImage'];
    $scope.money={};
    $scope.edit_flag=true;
    $scope.data = {
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
    };
    if ($scope.role == '客户经理' ){
        $scope.approve_flag=false;
    }else{
        $scope.approve_flag=true;
    }
    $scope.onEdit =function(){
        $scope.edit_flag=false;
    }
    $scope.onSubmit = function(){
        if($scope.edit_flag == false){
            alert('请先保存数据') 
        }else{
            if($scope.data.transaction_info.amount != undefined &&  $scope.data.transaction_info.amount*1 > 0){
                  angular.element("div[name='applicationButtonGroup']").find("button,input,select,textarea").attr('disabled','disabled');
                  creditService.submit($scope.data).success(function(resp){
                           $scope.next_step=resp.data.next_step;
                           $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                  });
            }else{
                alert('申请金额必须大于0');
            }
        }
    };
    $scope.onSave = function(){
        creditService.update($scope.data).success(function(resp){
             $scope.edit_flag=true;
             alert('保存成功');
        }); 
    }

    $scope.info = function(){
        if($scope.applicationId){
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
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
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                if(resp.data.application_info.bill_type == null){
                    $scope.data.application_info.bill_type="全额";
                }
                $scope.money.amount = app_money_char($scope.data.transaction_info.amount)[1]
            });
        }
    }
    $scope.info();
    $scope.approve = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'同意', 'comment':$scope.result})
        .success(function(resp){
            angular.element("div[name='applicationButtonGroup']").find("button,input,select,textarea").attr('disabled','disabled');
            $scope.next_step=resp.data.next_step;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
        });
    };
    $scope.reject = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'不同意', 'comment':$scope.result})
            .success(function(resp){
                $scope.submitedFlag = true;
                alert('提交成功');
            });

    };

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

    $scope.acc_name = function(data){
        if(data != undefined && data.length >= 10){
            BillService.query_dis_name(data).success(function(resp){
                if(resp.data.reason != '交易成功'){
                    alert(resp.data.reason);
                }
                if(resp.data.code == 0){
                    $scope.data.name = resp.data.户名;
                }
            })
        }else{
            alert('请输入正确的账号')
        }
    }

    $scope.apply_date = function(data){
        $scope.data.application_info.apply_date =app_date_ch(data);
    }
    $scope.first_drawing_date= function(data){
        $scope.data.application_info.first_drawing_date=app_date_ch(data);
    }
    $scope.first_rep_date= function(data){
        $scope.data.application_info.first_rep_date=app_date_ch(data);
    }
    $scope.amount = function(data){
        $scope.data.transaction_info.amount =app_money_char(data)[0];
        $scope.money.amount = app_money_char(data)[1];
    }

});
ysp.controller('accBillLoanApplicationController', function($scope, $rootScope,loanService ,creditService,industryService,imageService,store,contractService,approvalService, BillService){
    $scope.edit_flag=true;
    $scope.money={};
    $scope.data = {
        contract:{},
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        lend_transaction:{},
        check:'no'
    };

    if ($scope.role == '客户经理' ){
        $scope.approve_flag=false;
    }else{
        $scope.approve_flag=true;
    }
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
                window.setTimeout(function(){
                 $scope.industry_top=ls[0];
                 $scope.industry_big=ls[1];
                 $scope.industry_mid=ls[2];
                 $scope.industry_small=ls[3];
                 },1000);

    }

    $scope.showEnd = function(){
        loanService.query_acceptanceBill($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             $scope.data.contract=resp.data.contract;
             if($scope.data.lend_transaction){
                 if($scope.data.lend_transaction.industry_1){
                    var ls=[];
                    ls.push($scope.data.lend_transaction.industry_1);
                    ls.push($scope.data.lend_transaction.industry_2);
                    ls.push($scope.data.lend_transaction.industry_3);
                    ls.push($scope.data.lend_transaction.industry_4);
                    showIndustry(ls);
                 }else{
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

    };
    $scope.onSubmit = function(){
        if($scope.edit_flag == false){
            alert('请先保存数据'); 
        }else if (!$scope.data.contract) {
            alert('请先生存合同信息');
        }else{
            if($scope.data.lend_transaction.amount != undefined &&  $scope.data.lend_transaction.amount*1 > 0){
                 angular.element("div[name='loanApplicationForm']").find("button,input,select,textarea").attr('disabled','disabled');
                 loanService.submit($scope.data).then(function(resp){
                      $scope.next_step=resp.data.next_step;
                      $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                 });
            }else{
                alert('申请金额必须大于0');
            }
       }
    };
    $scope.onSave = function(){
          $scope.edit_flag=true;
          if($scope.data.lend_transaction != null && $scope.data.lend_transaction.transaction_id){
              loanService.update_acceptanceBill($scope.data).success(function(resp){
                    loanService.query_acceptanceBill($scope.data.transaction_info.transaction_id).success(function(rsp){
                          $scope.data.lend_transaction=rsp.data.lend_transaction;
                    });
                   alert(resp.data.msg);
              });
          }else{
               loanService.save_acceptanceBill($scope.data).success(function(resp){
                    loanService.query_acceptanceBill($scope.data.transaction_info.transaction_id).success(function(rsp){
                         $scope.data.lend_transaction=rsp.data.lend_transaction;
                         alert('保存成功');
                     });
               });
          }
    }
    $scope.onEdit = function(){
        $scope.edit_flag = false;
    };
    $scope.onContract = function(){
         if($scope.data.lend_transaction.transaction_id){
            contractService.save($scope.data).success(function(resp){
                  alert('生成成功');
                  $scope.data.contract=resp.data.contract;
            });
         }else{
            alert('请先录入必要信息')
         }
    }

    $scope.info = function(){
        if($scope.applicationId){
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
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
                if(resp.data.application_info.first_drawing_date== null){
                    var d = new Date();
                    var Y = d.getFullYear();
                    var M = d.getMonth()+1 ; if (M<10) M='0'+M
                    var D = d.getDate();if (D < 10) D='0'+D
                    $scope.data.application_info.first_drawing_date=Y + '-' + M + '-' + D;
                }
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                if(resp.data.application_info.bill_type == null){
                    $scope.data.application_info.bill_type="全额";
                }
                $scope.data.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.showEnd();
                $scope.money.amount = app_money_char($scope.data.transaction_info.amount)[1]

            });
            $scope.initIndustry = function(){
                $scope.industry_top=null;
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
        }
    }
    $scope.info();
    $scope.approve = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'同意', 'comment':$scope.result}).success(function(resp){
             angular.element("div[name='applicationButtonGroup']").find("button,input,select,textarea").attr('disabled','disabled');
             $scope.next_step=resp.data.next_step;
             $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
        });
    };
    $scope.reject = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'不同意', 'comment':$scope.result})
            .success(function(resp){
                alert('提交成功');
            });

    };

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

    $scope.acc_name = function(data){
        if(data != undefined && data.length >= 10){
            BillService.query_dis_name(data).success(function(resp){
                if(resp.data.reason != '交易成功'){
                    alert(resp.data.reason);
                }
                if(resp.data.code == 0){
                    $scope.data.name = resp.data.户名;
                }
            })
        }else{
            alert('请输入正确的账号')
        }
    }

    $scope.first_drawing_date= function(data){
        $scope.data.lend_transaction.first_drawing_date=app_date_ch(data);
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
    $scope.amount = function(data){
        $scope.data.transaction_info.amount =app_money_char(data)[0];
        $scope.money.amount = app_money_char(data)[1];
    }
    $scope.bill_rate_sum = function(data){
        $scope.data.lend_transaction.bill_rate_sum =app_money_char(data)[0];
        $scope.money.bill_rate_sum = app_money_char(data)[1];
    }
});
ysp.controller('accBillLoanController', function($scope, $rootScope,loanService ,creditService,industryService,imageService,store,contractService,approvalService, BillService){
    $scope.edit_flag=true;
    $scope.data = {
        contract:{},
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        lend_transaction:{},
        check:'no'
    };

    if ($scope.role == '客户经理' ){
        $scope.approve_flag=false;
    }
    $scope.acc_bill_loan_print = function(form_data){
        loanService.loan_print(form_serializable(document.getElementById(form_data))).success(function(resp){
            $scope.loan_static_path = resp.data;
            window.setTimeout(function(){
                var iframe = document.getElementById('acc_bill_print_frame');
                iframe.contentWindow.print();
            },5000);

        });
    };
    $scope.showEnd = function(){
        loanService.query_acceptanceBill($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             $scope.data.contract=resp.data.contract;
             if($scope.data.lend_transaction){
                 if($scope.data.lend_transaction.industry_1){
                    var ls=[];
                    ls.push($scope.data.lend_transaction.industry_1);
                    ls.push($scope.data.lend_transaction.industry_2);
                    ls.push($scope.data.lend_transaction.industry_3);
                    ls.push($scope.data.lend_transaction.industry_4);
                    showIndustry(ls);
                 }else{
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

    };
    $scope.onSubmit = function(){
        if($scope.edit_flag == false){
            alert('请先保存数据'); 
        }else{
             angular.element("div[name='loanApplicationForm']").find("button,input,select,textarea").attr('disabled','disabled');
             loanService.submit($scope.data).then(function(resp){
                 alert('提交成功')
             });
         }
    };
    $scope.info = function(){
        if($scope.applicationId){
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
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
                if(resp.data.application_info.first_drawing_date== null){
                    var d = new Date();
                    var Y = d.getFullYear();
                    var M = d.getMonth()+1 ; if (M<10) M='0'+M
                    var D = d.getDate();if (D < 10) D='0'+D
                    $scope.data.application_info.first_drawing_date=Y + '-' + M + '-' + D;
                }
                if(resp.data.application_info.repayment_from == null){
                    $scope.data.application_info.repayment_from="经营收入";
                }
                if(resp.data.application_info.bill_type == null){
                    $scope.data.application_info.bill_type="全额";
                }
                $scope.data.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.showEnd();
                $scope.money.amount = app_money_char($scope.data.transaction_info.amount)[1]

            });
            $scope.initIndustry = function(){
                $scope.industry_top=null;
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
        }
    }
    $scope.info();
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

    $scope.acc_name = function(data){
        if(data != undefined && data.length >= 10){
            BillService.query_dis_name(data).success(function(resp){
                if(resp.data.reason != '交易成功'){
                    alert(resp.data.reason);
                }
                if(resp.data.code == 0){
                    $scope.data.name = resp.data.户名;
                }
            })
        }else{
            alert('请输入正确的账号')
        }
    }

    $scope.first_drawing_date= function(data){
        $scope.data.lend_transaction.first_drawing_date=app_date_ch(data);
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
    $scope.amount = function(data){
        $scope.data.transaction_info.amount =app_money_char(data)[0];
        $scope.money.amount = app_money_char(data)[1];
    }
    $scope.bill_rate_sum = function(data){
        $scope.data.lend_transaction.bill_rate_sum =app_money_char(data)[0];
        $scope.money.bill_rate_sum = app_money_char(data)[1];
    }
});

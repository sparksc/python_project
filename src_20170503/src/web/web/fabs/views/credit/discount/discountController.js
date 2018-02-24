ysp.controller('discountController', function($scope, store,$rootScope, creditService, companyInformationService,CustomerSearchService ){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus='新增申请';
    /* Query Application */
    $scope.tableHead=['申请书号','客户名称', '业务品种', '主要担保方式', '申请状态', '币种', '金额', '申请人', '申请机构', '操作'];
    $scope.queryCond = {};
    $scope.tableData = [];
    $scope.data = {};
    $scope.queryApplication=function(){
          $scope.cust_type='company'
          $scope.lend_type='023'
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
                if($scope.tableData.length > 0){
                    $scope.tableMessage='';
                }else{
                    $scope.tableMessage='未查询到数据';
                }
            });
    }

    $scope.init = function(){
        $scope.queryApplication();
    };

    $scope.term_month = function(data){
        console.log($scope.data)
        alert($scope.data.application_info.term_month)
        $scope.data.application_info.term_month=app_date_ch(data);
    }
    /* Application Detail */
    $scope.applicationDetail = function(data){
        var cust_name = data.party.name;
        var tabName = cust_name+'的贴现详情';
        var htmlContent = '<div ng-include="'+'\'views/credit/pageDistribute/index.html' +'\'" ></div>';
        var eventObj = {'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':data.party,'application_status':data.application_status,'activity_status':data.activity_status,'applicationId':data.id,'product_code':'023','product_name':'承兑汇票贴现','product_page':data.product.product_page,'transaction_id':data.transaction_id,'activity_page':data.activity_page});                       
        var applicationScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).scope();

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
     $scope.term_month= function(data){
        $scope.data.application_info.term_month=app_date_ch(data);
    }
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
        var tabName = cust_name+'的贴现申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/discount/preLoan.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        console.log($scope.chosenCust.party);
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':$scope.chosenCust,'apply_type':'新增'});
    };

    $scope.custSearchCancel = function(){
        $scope.chosenCust = null;
        $scope.custTableData = {};
        $("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal('hide');
    };
   /* Cancel Application */
    $scope.cancelModalData = null;
    $scope.cancelApplication = function(applicationId){
        $scope.cancelId = applicationId;
        $("#tab_"+ $scope.tabId + "_content").find("div[name='cancelConfirmModal']").modal({backdrop: 'static',});
    }
    $scope.cancelConfirmed = function(){
        creditService.cancel($scope.cancelId).success(function(resp){
            $scope.cancelId = null;
            $("#tab_"+ $scope.tabId + "_content").find("div[name='cancelConfirmModal']").modal('hide');
            $scope.queryApplication();
        }).error(function(){
            alert('取消失败，请重试');
        });
    }
});

//预申请
ysp.controller('discountApplicationController', function($scope,  creditService){
    $scope.data = {};
    $scope.btn_edit_flag=true;
    $scope.pre_apply={};
    $scope.pre_apply.party_id=$scope.customer.id
    $scope.pre_apply.no=$scope.customer.no;
    $scope.pre_apply.name=$scope.customer.name;
    $scope.pre_apply.loan_type='承兑汇票贴现';
    $scope.pre_apply.main_gua='质押';
    $scope.pre_apply.loan_type_code='023'
    $scope.onSubmit = function(d){
          alert(d)
          console.log($scope.pre_apply);
          creditService.save_discount($scope.pre_apply).success(function(resp){
              var data = resp.data
              if(data.success){
                  alert('新增成功');
                  creditService.get(data.id).success(function(rsp){
                    $scope.pre_apply.end_date  = rsp.data.end_date;
                  });
              }else{
                  alert(data.error)
              }
         });
    }

});

// -------------------   放款界面 控制 ----------------
ysp.controller('discountLoanController',function($scope, $rootScope,loanService ,creditService,industryService,store,contractService,approvalService,BillService){
    $scope.money={};
    $scope.btn_edit_flag = true;
    $scope.data = {
        contract:{},
        customer:$scope.customer,
        transaction_info:{},
        application_info:{},
        lend_transaction:{},
    };

    function showIndustry(ls){
                console.log(ls)
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
        loanService.query($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             console.log('safsaf',resp.data)
             $scope.data.contract=resp.data.contract;
             var ls=[];
             if($scope.data.lend_transaction){
                 ls.push($scope.data.lend_transaction.industry_1);
                 ls.push($scope.data.lend_transaction.industry_2);
                 ls.push($scope.data.lend_transaction.industry_3);
                 ls.push($scope.data.lend_transaction.industry_4);
                 showIndustry(ls);
                 $scope.money.amount = app_money_char($scope.data.lend_transaction.amount)[1]
                 $scope.money.bill_rate_sum = app_money_char($scope.data.lend_transaction.bill_rate_sum)[1];
             }
        });
        $scope.base_info_display = false;
        $scope.end_loan_display = true; 
    };
    $scope.onSubmit = function(){
              loanService.loan($scope.data).success(function(resp){
                    alert(resp.data.msg);
        })
    };

    $scope.onCancel = function(){
        $scope.btn_edit_flag = false;
        $scope.data.loan={};
    };
    
    /************************ 审批使用 *************************/
    //TODO:ng-include的内容如何更好的通讯？ 使用element获取的scope并不能获得该方法
    $scope.submitedFlag = false;
    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            // 获取申请信息
            creditService.get($scope.applicationId).success(function(resp){
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                console.log('$scope.data.application_info',$scope.data.application_info)
                console.log('$scope.data.transaction_info',$scope.data.transaction_info)
                $scope.end_date = resp.data.end_date
                $scope.showEnd(); 
            });
        }
    }
    $scope.info();
    //打印
    $scope.acc_bill_loan_print = function(form_data){
        loanService.loan_print(form_serializable(document.getElementById(form_data))).success(function(resp){
            $scope.loan_static_path = resp.data;
            window.setTimeout(function(){
                var iframe = document.getElementById('acc_bill_print_frame');
                iframe.contentWindow.print();
            },5000);

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
});

ysp.controller('billController', function($scope, store, $rootScope, loanService, BillService){
    $scope.tableHead=['票据号码','票据类型', '票面金额','复核', '操作'];
    $scope.application_id=$scope.$parent.applicationId;
    $scope.form_data={};
    $scope.money={};
    $scope.tableData=[];
    $scope.$on('dis_bill_kind',function(event,msg){
        $scope.bill_kind = msg.bill_kind;
        $scope.bill_kill = msg.bill_kill;
        $scope.proposer_acc = msg.repayment_account_no;
        $scope.form_data.bill_type = $scope.bill_kind;
        $scope.form_data.bill_kill = $scope.bill_kill;
        if($scope.bill_kind == '电票')
            $scope.form_data.use_date = 0;
        else if($scope.bill_kind == "纸票")
            $scope.form_data.use_date = 3;
        $scope.form_data.proposer_acc = $scope.proposer_acc;
    }); 

    if($scope.form_data.discount_type== undefined){
       $scope.form_data.discount_type='普通贴现';
    }
    if($scope.form_data.bill_kill== undefined){
       $scope.form_data.bill_kill='银行承兑汇票';
    }
    $scope.queryInfo = function(){
        if($scope.application_id != undefined){
            BillService.query_info($scope.application_id).success(function(resp){
                $scope.tableData=resp.data;
                if(resp.data.length >0){
                    $scope.tableMessage='';
                }else{
                    $scope.tableMessage='未查询到数据';
                }
            })
        }
    }
    
    $scope.check = function(data){
        if(data == undefined || data.length != 12){
            alert('请输入12位正确的行号')
            return -1;
        }
    }
    $scope.bill_no = function(data){
        if(data == undefined){
            alert("请输入正确的票据号码");
            return -1;
        }else if($scope.form_data.bill_type == "电票"){
            if(data.length != 30){
                alert("请输入30的正确票据号码");
                return -1;
            }
        }else{
            if(data.length != 16){
                alert("请输入16的正确的票据号码");
                return -1;
            } 
        }
    }
    $scope.check_one_bill=function(d){
        d.checked = '是';
        BillService.update(d.id,d).success(function(resp){
            alert('复核成功');
        });
    }
    $scope.submit = function(v){
        if(v){
            $scope.calinvest();
            if($scope.max_month($scope.form_data.bill_due_date) == -1
                || $scope.bill_no($scope.form_data.bill_no) == -1){
                return ;
            }
            $scope.form_data.product_type = '贴现';
            if($scope.form_data.id == undefined){
                BillService.query($scope.application_id , {'bill_no':$scope.form_data.bill_no,'product_type':$scope.form_data.product_type}).success(function(resp){
                    var sig = 1;
                    if(resp.data.msg == "err"){
                        sig = 0;
                        alert('该票据号已存在');
                    }
                    if(resp.data.bill_type != null && resp.data.bill_type.bill_type != $scope.form_data.bill_type){
                        sig = 0;
                        alert('请录入统一的票据类型')
                    }
                    if(sig){
                        BillService.create($scope.application_id,$scope.form_data).success(function(resp){
                        alert('票据新增成功')
                        $scope.disabled_flag=true;
                        $scope.disabled_flag = false;
                        $scope.form_data={};
                        $scope.money={};
                        $scope.form_data.bill_kill='银行承兑汇票';
                        $scope.form_data.discount_type='普通贴现';
                        })
                    }
                })
            }else{
                BillService.update($scope.form_data.id,$scope.form_data).success(function(resp){
                    alert('票据保存成功')
                })
            }
        }
    }

    $scope.clear = function(){
        $scope.form_data={};
        $scope.money={};
        $scope.disabled_flag=false;
        $scope.form_data.discount_type='普通贴现';
        $scope.form_data.bill_kill='银行承兑汇票';
        $scope.form_data.bill_kill = $scope.bill_kill;
        $scope.form_data.bill_type = $scope.bill_kind;
        if($scope.bill_kind == '电票')
            $scope.form_data.use_date = 0;
         else if($scope.bill_kind == "纸票")
            $scope.form_data.use_date = 3;
        $scope.form_data.proposer_acc = $scope.proposer_acc;

    }
    $scope.check_bill = function(){
        var user = {'user_name':store.getSession('user_name')}
        BillService.check_bill($scope.application_id,user).success(function(resp){
           alert(resp.data.msg); 
        });
    }

    $scope.edit = function(){
        $scope.disabled_flag=false;
    }
     
    $scope.billInfoDetail = function(data){
        $scope.disabled_flag=true;
        $scope.form_data=data;
        $scope.money.bill_amount = app_money_char($scope.form_data.bill_amount)[1];
        $scope.money.deal_amount = app_money_char($scope.form_data.deal_amount)[1];
        $scope.money.discount_interest = app_money_char($scope.form_data.discount_interest)[1];
    }
    $scope.delbillInfo = function(bill_id){
        BillService.del(bill_id).success(function(resp){
           $scope.queryInfo();
        })    
    }
    //到期日天数控制
    $scope.max_month = function(data){
        if($scope.form_data.bill_from_date == undefined || $scope.form_data.bill_from_date == ''){
            return -1;
        }
        if(data == undefined || data ==''){
            return -1;
        }
        from_date = $scope.form_data.bill_from_date;
        if($scope.days(from_date, data) >= 0){
            alert('票据到期日不能小于等于出票日期')
            $scope.form_data.bill_due_date = '';
            return -1;
        }
        if($scope.form_data.bill_type == "电票"){
            var year = from_date.substring(0,4)*1+1;
            var from_date = year + from_date.substring(4,10);
            if($scope.days(from_date, data) < 0){ 
                alert('出票日期至票据到期日不能大于1年')
                $scope.form_data.bill_due_date = '';
                return -1;
            }   
        }else{
            var month = from_date.substring(5,7)*1+6;
            console.log(month)
            if(month > 12){
                month = month - 12; 
                console.log(month)
                var year = from_date.substring(0,4)*1+1;
                var from_date = year +'-'+ month + from_date.substring(7,10);
                console.log(from_date)
            }else{
                var year = from_date.substring(0,4);
                var from_date = year +'-'+ month + from_date.substring(7,10);
            }   
            if($scope.days(from_date, data) < 0){ 
                $scope.form_data.bill_due_date = '';
                alert('出票日期至票据到期日不能大于6个月')
                return -1;
            }   
        }   
    }
    //获取当前日期
    $scope.new_date =function(){
        var newd = new Date();
        var year = newd.getFullYear()
        var month = newd.getMonth()+1
        var day = newd.getDate();
        if(month<10){
           month = '0'+month;
        }
        if(day<10){
            day = '0'+day;
        }
        return year+'-'+month+'-'+day;
    }
    $scope.days = function(date1, date2){
        var from_date = new Date(Date.parse(date1.replace(/-/g,'/')));
        var due_date = new Date(Date.parse(date2.replace(/-/g,'/')));
        var days = (from_date - due_date)/(24*60*60*1000);
        return days;
    }

    $scope.calinvest = function(){
        var amount = $scope.form_data.bill_amount * 1; //金额
        var from_date = new Date(Date.parse($scope.form_data.discount_date.replace(/-/g,'/')));
        var due_date = new Date(Date.parse($scope.form_data.bill_due_date.replace(/-/g,'/')));
        var days = (due_date - from_date)/(24*60*60*1000);
        var day = $scope.form_data.use_date;
        days = days + day*1;

        var rate = $scope.form_data.discount_rate * 1;
        $scope.form_data.discount_interest = (amount * days * rate/(30*1000)).toFixed(2);
        var data = $scope.form_data.discount_interest + "";
        data = data.substring(0,data.length-3);
        $scope.money.discount_interest = app_money_char(data)[1];
    }
    //文件上传
    $scope.upload = function(){
        var token = store.getSession("token");
        var file = $('#Bill').find('input[name="file"]').prop('files');
        var form = new FormData();
        if(file[0] == undefined){
            alert('请选择上传文件');
            return;
        }
        form.append('file',file[0]);
        form.append('application_id', $scope.application_id);
        $.ajax({
            type: "POST",
            url : base_url+"/bill/Bill/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },
            success: function(msg){
                if(msg.data == 'err'){
                    alert('文件数据有误，上传失败')
                }else{
                    $scope.queryInfo();
                    alert("上传成功");
                }
            }
        });
    }

    $scope.bill_amount = function(data){
        console.log(data)
        var list =  app_money_char(data);
        $scope.form_data.bill_amount = list[0];
        $scope.money.bill_amount = list[1];
    }
    $scope.deal_amount = function(data){
        var list =  app_money_char(data);
        $scope.form_data.deal_amount = list[0];
        $scope.money.deal_amount = list[1];
    }
    $scope.bill_from_date = function(data){
        $scope.form_data.bill_from_date = app_date_ch(data);
        if($scope.days($scope.new_date(), $scope.form_data.bill_from_date)<=0){
            alert('出票日期大于当天');
            $scope.form_data.bill_from_date = '';
            return;
        }
    } 
    $scope.bill_due_date = function(data){
        $scope.form_data.bill_due_date = app_date_ch(data);
        if($scope.days($scope.new_date(), $scope.form_data.bill_due_date)>0){
            alert('到期日期小于当天');
            $scope.form_data.bill_due_date = '';
            return ;
        }
        $scope.max_month($scope.form_data.bill_due_date);
    }
    //大于出票日  小于到期日
    $scope.discount_date = function(data){
        $scope.form_data.discount_date = app_date_ch(data);
        if($scope.days($scope.new_date(), $scope.form_data.discount_date)>0){
            alert('贴现日期小于当天');
            $scope.form_data.discount_date = '';
            return ;
        }
        if($scope.days($scope.form_data.bill_from_date, $scope.form_data.discount_date)>0){
            alert('贴现日期小于出票日');
            $scope.form_data.discount_date = '';
            return ;
        } 
        if($scope.days($scope.form_data.discount_date, $scope.form_data.bill_due_date)>0){
            alert('贴现日期大于到期日');
            $scope.form_data.discount_date = '';
            return ;
        } 
    }
    $scope.discount_due_date = function(data){
        $scope.form_data.discount_due_date = app_date_ch(data);}
    $scope.deal_date = function(data){
        $scope.form_data.deal_date = app_date_ch(data);}
})

//贷款申请
ysp.controller('discountBaseInfoController',function($scope, $rootScope,loanService ,creditService,industryService,store,contractService,approvalService,BillService){
    $scope.disabled_flag = true;
    if($scope.$parent.user == '客户经理' && $scope.$parent.application_status!='贴现支行风险评价'){
        $scope.btn_edit_flag = false;
        $scope.end_loan_display = false; 
        $scope.approveActivityFlag=false;
    }else{
        $scope.btn_edit_flag = true;
        $scope.end_loan_display = false;
        $scope.approveActivityFlag=true;
    }
    if($scope.$parent.application_status=='贴现撰写调查报告'){
        $scope.end_loan_display = true;
    }
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
        check:'no'
    };

    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            // 获取申请信息
            console.log('info'+$scope.product_page);
            creditService.get($scope.applicationId).success(function(appresp){
                var resp = appresp;
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                // 设置默认值
                if(resp.data.transaction_info.currency_code == null){
                    $scope.data.transaction_info.currency_code='CNY';
                }
                if(resp.data.application_info.agreement_rate == null){
                    $scope.data.application_info.agreement_rate='否';
                }
                //获取经办机构 经办人
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
                if(resp.data.application_info.bill_type == null){
                    $scope.data.application_info.bill_type="全额";
                }
                $scope.end_date = resp.data.end_date
                $scope.data.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.ltSelected = false;
                $scope.money.amount = app_money_char($scope.data.transaction_info.amount)[1];
            });
        }
    }  
    $scope.info(); 
    $scope.onSubmit = function(v){
        if(v && $scope.data.transaction_info.amount*1 > 0){
            if($scope.disabled_flag == false){
                $scope.onSave();
            } 
            creditService.submit_discount($scope.data).success(function(resp){
                if(resp.data.success){
                    $scope.submitedFlag = true;
                    $scope.disabled_flag = true;
                    $scope.next_step=resp.data.next_step;
                    console.log($scope.next_step)
                    $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                }else{
                    alert(resp.data.msg);
                }
            });
        }else{
            alert('贴现金额必须大于0');
        }
    };
    
    $scope.onSave = function(){
        creditService.saveInfo_discount($scope.data).success(function(resp){
            var application_id = resp.data.application_id;
            if(application_id){
                alert('保存成功');
                $scope.btn_edit_flag = false;
                $scope.disabled_flag = true;
            }else{
                alert("数据保存失败");
            }
        });
    }

    $scope.onEdit = function(){
        $scope.btn_edit_flag = true;
        $scope.end_loan_display = true;
        $scope.disabled_flag = false;
    };

    $scope.approve = function(){
        approvalService.approve($scope.applicationId, {'comment_type':'同意', 'comment':$scope.result})
        .success(function(resp){
            if(resp.data.success){
                $scope.submitedFlag = true;
                $scope.next_step=resp.data.next_step;
                $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
            }else{
                alert(resp.data.msg);
            }    
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
    $scope.repayment_account_no = function(data){
        if(data != undefined && data.length >= 10){
            BillService.query_dis_name(data).success(function(resp){
                alert(resp.data.reason);
                if(resp.data.code == 0){
                    $scope.discount_name = resp.data.户名;
                }
            })
        }else{
            alert('请输入正确的账号') 
        } 
    } 
    //格式转换
    //日期
    $scope.apply_date = function(data){
        $scope.data.application_info.apply_date =app_date_ch(data);
    } 
    //金额
    $scope.amount = function(data){
        var list = app_money_char(data);
        $scope.data.transaction_info.amount = list[0];
        $scope.money.amount = list[1];
    }
});

// ------------------- 票据录入界面 控制 ----------------
ysp.controller('discountAppInfoController',function($scope, $rootScope,loanService ,creditService,industryService,store,contractService,approvalService,BillService){
    $scope.money={};
    $scope.btn_creadit_flag = true;
    $scope.disabled_flag = true;
    if($scope.$parent.user == '客户经理'){
        $scope.btn_edit_flag = false;
        $scope.end_loan_display = true;
        $scope.approveActivityFlag=true;
    }else if($scope.$parent.user == '贴现支行长审批'){
        $scope.approveActivityFlag=false;
    }else{
        $scope.btn_edit_flag = true;
        $scope.end_loan_display = false;
    }
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
        check:'no'
    };
    if($scope.data.contract == undefined){
        $scope.btn_creadit_flag = true;
    }
    function showIndustry(ls){
                console.log(ls)
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

    $scope.onSubmit = function(v){
        if($scope.disabled_flag == false){
            $scope.loanSave();
        }
        if($scope.application_status.indexOf('贴现信息录入') != -1){
            $scope.loanSave();
            $scope.data.check = 'yes';
        }
        BillService.check_bill_query($scope.applicationId).success(function(rsp){
            if(rsp.data.msg=="success"){
                $scope.btn_edit_flag = false;
                creditService.submit_discount($scope.data).success(function(resp){
                    if(resp.data.success){
                        $scope.submitedFlag = true;
                        $scope.disabled_flag = true;
                        $scope.next_step=resp.data.next_step;
                        $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                        var application_id = resp.data.application_id;
                        alert('提交成功');
                     }else{
                        alert(resp.data.msg);
                     }
                });
            }else{
                alert('需双人验票')
            }
        });
    } 

    $scope.loanSave = function(){
        if($scope.industry_top && $scope.industry_big && $scope.industry_mid && $scope.industry_small){
                $scope.data.lend_transaction.industry_1=$scope.industry_top;
                $scope.data.lend_transaction.industry_2=$scope.industry_big;
                $scope.data.lend_transaction.industry_3=$scope.industry_mid;
                $scope.data.lend_transaction.industry_4=$scope.industry_small;
         }     
         if($scope.data.lend_transaction != null && $scope.data.lend_transaction.transaction_id){
            console.log($scope.data.lend_transaction)
            loanService.update($scope.data).success(function(resp){
                  loanService.query($scope.data.transaction_info.transaction_id).success(function(rsp){
                        $scope.data.lend_transaction=rsp.data.lend_transaction;
                        $scope.$emit('bill_kind',{'bill_kind':$scope.data.lend_transaction.bill_kind,'repayment_account_no':$scope.data.lend_transaction.repayment_account_no,'bill_kill':$scope.data.lend_transaction.bill_kill});
                   });
                 alert(resp.data.msg);
                 $scope.btn_edit_flag=false;
                 $scope.disabled_flag = true;
                 $scope.btn_creadit_flag = true;
            });
         }else{
            loanService.save($scope.data).success(function(resp){
                 loanService.query($scope.data.transaction_info.transaction_id).success(function(rsp){
                      $scope.data.lend_transaction=rsp.data.lend_transaction;
                      $scope.$emit('bill_kind',{'bill_kind':$scope.data.lend_transaction.bill_kind,'repayment_account_no':$scope.data.lend_transaction.repayment_account_no,'bill_kill':$scope.data.lend_transaction.bill_kill});
                      alert('保存成功');
                      $scope.btn_edit_flag=false;
                      $scope.disabled_flag = true;
                      $scope.btn_creadit_flag = true;
                });
            });
         }
    }

    $scope.showEnd = function(){
        loanService.query($scope.data.transaction_info.transaction_id).success(function(resp){
             $scope.data.lend_transaction=resp.data.lend_transaction;
             $scope.data.contract=resp.data.contract;
             if($scope.data.lend_transaction){
                 $scope.money.amount = app_money_char($scope.data.lend_transaction.amount)[1]
                 $scope.$emit('bill_kind',{'bill_kind':$scope.data.lend_transaction.bill_kind,'repayment_account_no':$scope.data.lend_transaction.repayment_account_no,'bill_kill':$scope.data.lend_transaction.bill_kill});
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
                        console.log('cust_industry1',ls);
                        if(ls.length == 4 && ls.indexOf(null) == -1){
                            showIndustry(ls);
                        }
                        else{
                            $scope.initIndustry();
                        }
                    });
                }
            }else{
                $scope.data.lend_transaction={};
                industryService.query_cust($scope.customer.id).success(function(resp){
                    var ls = resp.data;
                        console.log('cust_industry2',ls);
                    if(ls.length == 4 && ls.indexOf(null) == -1){
                        showIndustry(ls)
                    }
                    else{
                        $scope.initIndustry();
                    }
                });
            }
        });
    }
    $scope.onEdit = function(){
        $scope.end_loan_display = true;
    	$scope.btn_edit_flag = true;
        $scope.disabled_flag = false;
    }
    $scope.onContract = function(){
         if($scope.data.lend_transaction.transaction_id){
            contractService.save($scope.data).success(function(resp){
                  alert('生成成功')
                  $scope.btn_creadit_flag = false;
                  $scope.data.contract=resp.data.contract;
            });  
         }else{
            alert('请先录入必要信息')
         }
    };

    $scope.info = function(){
        if($scope.applicationId){
            // 显示基本信息 
            // 显示产品
            // 获取申请信息
            $scope.loan_type_page = $scope.product_page
            creditService.get($scope.applicationId).success(function(appresp){
                var resp = appresp;
                $scope.data.transaction_info = resp.data.transaction_info;
                $scope.data.application_info = resp.data.application_info;
                // 设置默认值
                $scope.end_date = resp.data.end_date
                $scope.data.product_name = resp.data.product.name;
                $scope.product_code= resp.data.product.product_code;
                $scope.ltSelected = false;
                $scope.base_info_display = true;
                loanService.query($scope.data.transaction_info.transaction_id).success(function(rsp){
                    console.log(rsp)
                    $scope.data.contract=rsp.data.contract;
                    $scope.data.lend_transaction=rsp.data.lend_transaction;
                    console.log($scope.data)
                    $scope.showEnd();
                    if($scope.data.lend_transaction == undefined){
                        $scope.money.amount = app_money_char($scope.data.transaction_info.amount)[1];
                    }else{
                        $scope.money.amount = app_money_char($scope.data.lend_transaction.amount)[1];
                    }
                })
                $scope.money.bill_rate_sum = app_money_char($scope.data.lend_transaction.bill_rate_sum)[1];
            });

            // -----------------------  行业类别
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
            if(resp.data.success){
                $scope.submitedFlag = true;
                $scope.next_step=resp.data.next_step;
                $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
            }else{
                alert(resp.data.msg);
            }
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

    $scope.btmClose = function(){ 
        $scope.loan_type_code = undefined;
        $scope.loan_type_name = undefined;
        $scope.base_info_display = false; 
        $scope.data.loan={};
        $scope.data.lendtran={};
    };
    /*****************************影像数据**********************************/
    $scope.selectImage = function(fileInputElementName){
        file.click();
        file.change(function(){
            var fileObj = $(this).get(0).files[0];
            fileObj.name = fileInputElementName;
            var src = getObjectURL(fileObj);
            $(this).next().attr('src',src);
        });
    }
    $scope.repayment_account_no = function(data){
        if(data != undefined && data.length >= 10){
            BillService.query_dis_name(data).success(function(resp){
                alert(resp.data.reason);
                if(resp.data.code == 0){
                    $scope.discount_name = resp.data.户名;
                }
            })
        }else{
            alert('请输入正确的账号') 
        } 
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
        var list = app_money_char(data);
        $scope.data.lend_transaction.amount = list[0];
        $scope.money.amount = list[1];
    }
    $scope.bill_rate_sum = function(data){
        var list = app_money_char(data);
        $scope.data.lend_transaction.bill_rate_sum = list[0];
        $scope.money.bill_rate_sum = list[1];
    }
});


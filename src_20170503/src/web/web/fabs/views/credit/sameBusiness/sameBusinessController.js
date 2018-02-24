ysp.controller('sameBusinessController', function($scope, $rootScope, creditService, companyInformationService ){
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus='新增申请';
    /* Table Operating Flag */

    /* Query Application */
    $scope.tableHead=['编号','对手行名称', '业务类型',  '金额','申请时间', '申请状态',  '操作'];
    $scope.tableData = [];
    $scope.queryApplication=function(){
          creditService.samequery(
                $scope.opponent_name,
                $scope.amount,
                $scope.applicationStatus
            ).success(function(resp){
                console.log("同业返回：");
                console.log(resp.data);
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

    /* Application Detail  查看详情*/
    $scope.applicationDetail = function(data){
        var tabName = data.application_info.opponent_name+'的同业业务审批详情';
        var htmlContent = '<div ng-include="'+'\'views/credit/sameBusiness/detail.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'applicationId':data.application_info.id,'application_status':data.application_info.application_status,'product_code':data.product.product_code,'product_page':data.product.product_page,'product_name':data.product.name}); 
    };

    /* New Application */
    $scope.newApplication = function(){
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        var tabName = '同业业务申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/sameBusiness/sameBusinessInfo.html' +'\'" ></div>';
        var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'',};
        console.log($scope.curr_date);
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {});
    };
})
.controller('sameBusinessApplicationController', function($scope,$compile, store,$rootScope, creditService, CustomerSearchService,approvalService ){
    $scope.btn_edit_flag=true;
    $scope.btn_con_flag=true;
    $scope.disabled_flag=false;
    $scope.pre_apply={};
    $scope.money={};
    $scope.form_data={
        application_info:{},
        transaction_info:{},
        product_code:'',
        product_name:'',
    };
    //提交
    $scope.onSubmit = function(){
        var product_code = $scope.form_data.product_code;
        if (product_code == undefined || product_code == ''){
            alert('请选择业务种类')
        }else{
            if(product_code == '803' || product_code == '804' 
                || product_code == '805' || product_code == '806'){
                var index = $scope.contractList.length;
                if(index != 0 && $scope.contractList[0].opponent_name!='' && $scope.contractList[0].opponent_name!=undefined){
                    $scope.form_data.application_info.opponent_name=$scope.contractList[0].opponent_name;
                    var amount = 0;
                    for(var i =0;i<index;i++){
                        amount = amount*1 + $scope.contractList[i].amount*1;
                    }
                    $scope.form_data.transaction_info.amount = amount;
                }
            }else if(product_code == '807'){
                $scope.contractList={};
            }else{
                $scope.contractList={};
                $scope.calinvest();
            }
            creditService.same_bus_con($scope.form_data).then(function(resp){
                $scope.form_data.application_info.credit_con_no = resp.data.data;
                creditService.same_bus_submit({'contracts':$scope.contractList,'form_data':$scope.form_data}).then(function(resp){
                     var data = resp.data.data
                     if(data.success){
                         $scope.disabled_flag=true;
                         alert('新增成功');
                     }else{
                         alert(data.error)
                     }   
                })
            })
        }
    }
    //查找所属机构
    $scope.branch_select = function(){ 
        creditService.same_branch().success(function(resp){
            $scope.branchList = resp.data;
            console.log(resp)
        })
    }
    $scope.branch_select();
    $scope.havecontractList=[];
    $scope.contractList=[];
    $scope.same_addList =  function(){
            var item = new Object();
            //获取当前日期
            var index = $scope.contractList.length;
            item.open_name = '乌海银行股份有限公司';
            item.apply_date = $scope.new_date();
            $scope.contractList.push(item);
            var tr_html = "<tr>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"ture\" ng-model = \"contractList["+index+"].open_name \" /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].opponent_name \"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].amount \" /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].term_day \"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].product_rate \"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].apply_date \" ng-blur=\"apply_date_List("+index+")\"/> </td>"+ 
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].thur_date \" ng-blur=\"calinvest_List("+index+")\"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"true\" ng-model = \"contractList["+index+"].interest\"  /> </td>"+
           "</tr>";
            var contentTemplate = angular.element(tr_html);
            var contentElement = $compile(contentTemplate)($scope);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find('#addContractId').append(contentElement);
    }

    $scope.cred_addList =  function(){
            var item = new Object();
            var index = $scope.contractList.length;
            item.remark = 'DVP';
            $scope.contractList.push(item); 
            var tr_html = "<tr>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].bill_type \" /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].all_amount \" /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].opponent_name \"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].amount \"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].term_day \" ng-blur=\"thur_date_List("+index+")\"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].product_rate \" ng-blur=\"calinvest_List("+index+")\"/> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].thur_date \" /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"true\" ng-model = \"contractList["+index+"].interest\"  /> </td>"+
            "<td> <input type=\"text\" style=\"width:100%;\"ng-disabled = \"contract_flag\" ng-model = \"contractList["+index+"].remark\"  /> </td>"+
           "</tr>";
            var contentTemplate = angular.element(tr_html);
            var contentElement = $compile(contentTemplate)($scope);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find('#addContractId').append(contentElement);
    }

    $scope.show_lt_modal = function(trigger_elem){
        $("#tab_"+ $scope.tabId + "_content").find("div[name='loan_type_modal']").modal("show");
    }

    //查找对应页面
    $scope.choose_business_type = function(typeCode, typeName,typePage,guaType){
        $scope.pre_apply.loan_type_code = typeCode.replace(/(^\s*)|(\s*$)/g, "");
        $scope.form_data.product_code = typeCode.replace(/(^\s*)|(\s*$)/g, "");
        $scope.pre_apply.loan_type = typeName.replace(/(^\s*)|(\s*$)/g, "");
        $scope.form_data.product_name = typeName.replace(/(^\s*)|(\s*$)/g, "");
        $scope.pre_apply.main_gua = guaType;
        $scope.Page="views/credit/sameBusiness/"+typePage+".html";
        $scope.ltSelected = false;
        
        $scope.form_data.application_info.apply_date = $scope.new_date();
    };  
    $scope.onCancel = function(){
        $scope.form_data={
            application_info:{},
            transaction_info:{},
            product_code:'',
            product_name:'',
        };
    }
    $scope.init_business_type = function(){
        var tree_html = '<ul id="loan_type_tree'+$scope.tabId+'" class="ztree"> </ul>';
        angular.element($('#tab_'+ $scope.tabId + '_content').find("div[name='for_lt_tree']")).append(tree_html);
        var setting = {}; 
        var Nodes=[];
        //查询数据库
        creditService.products('同业').success(function(resp){
            var data = resp.data;
            show_product(data)
            $.fn.zTree.init($("#loan_type_tree"+$scope.tabId), setting, Nodes);
        });
        //生成业务类型列表
        function show_product(data){
            for(var i = 0 ; i < data.length ; ++i){
                var One = new Object();
                One.name = data[i].product_type.name;
                pro_arr = data[i].products;
                One.children=new Array();
                if(pro_arr.length>0){
                    for (var j = 0 ; j < pro_arr.length; ++j){
                        var Two = new Object();
                        Two.name=pro_arr[j].name;
                        Two.click="choose_business_type(this, '"+pro_arr[j].product_code+"', '"+Two.name+"','"+pro_arr[j].product_page+"', '"+pro_arr[j].main_gua_type+"')";
                        One.children.push(Two);
                    }
                }else{
                    One.click="choose_business_type(this, '"+data[i].product_code+"', '"+One.name+"','"+data[i].product_page+"')";
                }
                Nodes.push(One);
            }
        }
    }
    $scope.init_business_type();

    $scope.approveActivityFlag=false;
    $scope.approveCommitteeActivityFlag = false;
    $scope.submitedFlag = false;
    $scope.examine = function(){
        if($scope.applicationId){
            // 显示基本信息详情 
            // 显示产品
            // 获取申请信息
            $scope.approveActivityFlag=true;
            $scope.btn_edit_flag=false;
            $scope.btn_con_flag=false;
            $scope.loan_type_page = $scope.product_page
            $scope.Page='views/credit/sameBusiness/'+$scope.loan_type_page+'.html'
            $scope.form_data.product_name = $scope.product_name
            creditService.get($scope.applicationId).success(function(resp){
                $scope.form_data.transaction_info = resp.data.transaction_info;
                $scope.form_data.application_info = resp.data.application_info;
                //列表回显
                $scope.havecontractList = resp.data.list;
                $scope.ltSelected = false;
                $scope.money.amount = app_money_char($scope.form_data.transaction_info.amount)[1];
            });
        }
    }
    $scope.examine();
    $scope.approve = function(){
       approvalService.approve($scope.applicationId, {'comment_type':'同意', 'comment':$scope.result})
            .success(function(resp){
                if(resp.data.success){
                    $scope.submitedFlag = true;
                    $scope.next_step=resp.data.next_step;
                    if($scope.next_step.length>0){
                        $("#tab_"+ $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                    }else{
                        alert('审批完成');
                    }
                }else{
                    alert(resp.data.msg)
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
    //根据天数算到期日
    $scope.due_days = function(date1, days){
        var from_date = new Date(date1);
        var due_date = new Date(from_date.getFullYear(),from_date.getMonth(),from_date.getDate()+days*1);
        var month = due_date.getMonth()+1;
        var day = due_date.getDate();
        if(month<10){
           month = '0'+month;
        }
        if(day<10){
            day = '0'+day;
        }
        due = due_date.getFullYear()+'-'+month+'-'+day;
        return due;
    }
    $scope.days = function(date1, date2){
        if($scope.unde_null(date1)|| $scope.unde_null(date2)){
            return '';
        }
        var from_date = new Date(Date.parse(date1.replace(/-/g,'/')));
        var due_date = new Date(Date.parse(date2.replace(/-/g,'/')));
        var days = (from_date - due_date)/(24*60*60*1000);
        return days;
    }   

    $scope.calinvest = function(){
        if($scope.unde_null($scope.form_data.transaction_info.amount)
            || $scope.unde_null($scope.form_data.application_info.apply_date)
            || $scope.unde_null($scope.form_data.application_info.thur_date)
            || $scope.unde_null($scope.form_data.application_info.product_rate)){
            $scope.form_data.application_info.interest = 0;
            return ;
        }
        var amount = $scope.form_data.transaction_info.amount * 1; //金额
        var from_date = new Date(Date.parse($scope.form_data.application_info.apply_date.replace(/-/g,'/')));
        var due_date = new Date(Date.parse($scope.form_data.application_info.thur_date.replace(/-/g,'/')));
        var days = (due_date - from_date)/(24*60*60*1000);
        var rate = $scope.form_data.application_info.product_rate * 1;
        $scope.form_data.application_info.interest = (amount * days * rate/(360*100)).toFixed(2);
    }

    $scope.handle_date = function(data){
        $scope.form_data.application_info.handle_date =app_date_ch(data);
    }
    $scope.from_date= function(data){
        $scope.form_data.application_info.apply_date=app_date_ch(data);
    }
    $scope.thur_date= function(data){
        $scope.form_data.application_info.thur_date=app_date_ch(data);
    }
    $scope.first_drawing_date = function(data){
        $scope.form_data.application_info.first_drawing_date = app_date_ch(data);
    }
    $scope.amount = function(data){
       var list = app_money_char(data);
       $scope.form_data.transaction_info.amount = list[0];
       $scope.money.amount = list[1];
    }
    $scope.all_amount = function(data){
        var list = app_money_char(data);
        $scope.form_data.application_info.gty_amount = list[0];
        $scope.money.all_amount = list[1];
    }
    $scope.apply_date_List = function(id){
        $scope.contractList[id].apply_date=app_date_ch($scope.contractList[id].apply_date);
        if($scope.unde_null($scope.contractList[id].apply_date) || $scope.unde_null($scope.contractList[id].term_day)){
            $scope.contractList[id].thur_date = '';
            return ;
        }
        $scope.contractList[id].thur_date = $scope.due_days($scope.contractList[id].apply_date, $scope.contractList[id].term_day);
    }
    $scope.thur_date_List = function(id){
        if($scope.unde_null($scope.contractList[id].term_day)){
            $scope.contractList[id].thur_date = '';
        }else{
            $scope.contractList[id].thur_date = $scope.due_days($scope.new_date(), $scope.contractList[id].term_day);
        }
    }
    $scope.amount_List = function(id){
        var list = app_money_char($scope.contractList[id].amount);
        $scope.form_data.transaction_info.amount = list[0];
        $scope.contractList[id].amount = list[1];
    }
    $scope.calinvest_List= function(id){
        if($scope.unde_null($scope.contractList[id].amount) 
            || $scope.unde_null($scope.contractList[id].term_day)
            || $scope.unde_null($scope.contractList[id].product_rate)){
            $scope.contractList[id].interest = 0;
            return ;
        }
        var amount = $scope.contractList[id].amount * 1; //金额
        var days = $scope.contractList[id].term_day * 1;
        var rate = $scope.contractList[id].product_rate * 1;
        $scope.contractList[id].interest = (amount * days * rate/(365*100)).toFixed(2);
    }
    
    $scope.unde_null = function(data){
        if(data == undefined || data == ''){
            return 1;
        }
        return 0;
    }
});

//生成右边侧栏tab 
ysp.controller('sameDetailController',function($scope, $compile, creditService,userService){
    /*tab动态增加功能*/
    $scope.money = {};
    $scope.data={};
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab
    
    var defaultEvent = {
        'on':function(){
            return true;
        }
    };
    $scope.addSubTab = function(tabName, htmlContent, eventObj, autoFocus){
        var t = new Object();
        t.index = $scope.subTabIndex;
        t.tabName = tabName;
        t.htmlContent = htmlContent;
        t.createEvent = eventObj.create? eventObj.create:defaultEvent;
        t.closeEvent = eventObj.close? eventObj.close:defaultEvent;
        t.focusEvent = eventObj.focus? eventObj.focus:defaultEvent;
        t.loseFocusEvent = eventObj.loseFocus? eventObj.loseFocus:defaultEvent;

        $scope.subTab[t.index] = t;
        var tabContentId = $scope.subTabCreate(t);
        $scope.subTabIndex = $scope.subTabIndex + 1;       

        if (autoFocus == true){
            $scope.changeFocus(t.index);
        }
        return t.index;
    }; 
    
    $scope.subTabCreate = function(tabObj){
        succ_flag = $scope.subTab[tabObj.index].createEvent.on();
        if(succ_flag==true){
            // 多个Tab打开,使用$scope.$id 唯一标示
            var tabId = 'loan_tab_' + $scope.$id + '_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            var tabHtml = '<li id="'+ tabId +'" ng-click="changeFocus('+tabObj.index+')"> <a href="#'+ tabContentId +'" data-toggle="tab">'+ tabName +'</a></li>';
            var tabContentHtml = '<div class="tab-pane" id="'+ tabContentId +'"></div>';
            baseScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent']").scope();
            scope = baseScope.$new();
            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);

            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("ul[name='tab']").append(tabElement);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent']").append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);

            return tabContentId;
        }else{
            alert("tab 创建失败");
        };
    };
        
    $scope.changeFocus = function(focus_tabId){
        $scope.subTabLoseFocus($scope.currIndex);
        $scope.subTabFocus(focus_tabId);
        $scope.currIndex = focus_tabId;
    };

    $scope.subTabLoseFocus = function(index){
        succ_flag = $scope.subTab[index].loseFocusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).removeClass("ng-scope active").addClass("ng-scope");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane active").addClass("tab-pane");
        }else{
            alert("失焦失败！");
        }
    };

    $scope.subTabFocus = function(index){
        succ_flag = $scope.subTab[index].focusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).addClass("active");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane").addClass("tab-pane active");
        }else{
            alert("聚焦失败！");
        }
    };

    $scope.subTabClose = function(index){
        succ_flag = $scope.subTab[index].closeEvent.on();
        if(succ_flag==true){
            if(index == $scope.currIndex){
                var prevElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).prev();
                var nextElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).next();
                if (prevElement.length > 0){
                    $scope.changeFocus(prevElement.attr('id').split('_')[3]);
                }else if(nextElement.length > 0 ){
                    $scope.changeFocus(nextElement.attr('id').split('_')[3]);
                }else{
                    $scope.changeFocus(0);
                }
            }
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).remove();
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index+'_content')).remove();
            delete $scope.subTab[index];
        }else{
            alert("关闭失败！");
        }
    };
    $scope.init = function(){
        $scope.addSubTab('同业申请', '<div ng-include="'+'\'views/credit/sameBusiness/sameBusinessInfo.html' +'\'"></div>', {}, false);
        $scope.addSubTab('同业影像', '<div ng-include="'+'\'views/credit/image/elecImage.html' +'\'"></div>', {}, false);
        $scope.addSubTab('流程意见', '<div ng-include="'+'\'views/credit/CreditApproval/index.html' +'\'"></div>', {}, false);
        $scope.subTabFocus(0);
    };
    $scope.init();
});

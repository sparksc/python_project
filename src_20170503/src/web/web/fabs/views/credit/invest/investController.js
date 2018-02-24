ysp.controller('investController', function ($scope, $rootScope, creditService, companyInformationService) {
    $scope.guaranteeType = ['新发生', '展期', '借旧还新', '资产重组'];
    $scope.tableMessage = '请点击查询';
    $scope.applicationStatus = '新增申请';
    /* Table Operating Flag */
    /* Query Application */
    $scope.tableHead = ['编号', '业务种类', '审批状态', '操作'];
    $scope.tableData = [];

    $scope.queryApplication = function () {
        creditService.investquery(
            $scope.applicationStatus,
            $scope.bus_type,
            $scope.pj_type,
            $scope.openning_bank,
            $scope.open_name,
            $scope.account,
            $scope.big_num
        ).success(function (resp) {
                $scope.tableData = resp.data;
                if ($scope.tableData.length > 0) {
                    $scope.tableMessage = '';
                } else {
                    $scope.tableMessage = '未查询到数据';
                }

            }
        );

    }
    $scope.init = function () {
        $scope.queryApplication();

    };
    /* Application Detail */
    $scope.applicationDetail = function (data) {

        var cust_name = data.application_info.open_name;
        var tabName = cust_name + '的投资详情';
        var htmlContent = '<div ng-include="' + '\'views/credit/invest/detail.html' + '\'" ></div>';
        var eventObj = { 'create': '', 'focus': '', 'loseFocus': '', 'close': '', };
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'application_status': data.application_info.application_status,'image_about':'invest', 'applicationId': data.application_info.id, 'product_code': '705', 'product_page': data.product.product_page});
    };

    /* New Application */
    $scope.newApplication = function () {
        var d = new Date();
        $scope.curr_date = d.getFullYear() + '-' + d.getMonth() + '-' + d.getDay();
        var tabName = '投资业务审批';
        var htmlContent = '<div ng-include="' + '\'views/credit/invest/investInfo.html' + '\'" ></div>';
        var eventObj = { 'create': '', 'focus': '', 'loseFocus': '', 'close': '', };
        console.log($scope.curr_date);
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {});
        //$scope.confirmBtnDisabled = false;
        //$("#tab_"+ $scope.tabId + "_content").find("div[name='searchCustomerModal']").modal({backdrop: 'static',});
    };
})
    .controller('investApplicationController', function ($scope, store, $rootScope, creditService, CustomerSearchService, approvalService) {
        $scope.btn_edit_flag = true;
        $scope.save = '修改';
        $scope.pre_apply = {};
        $scope.money = {};
        $scope.form_data = {
            application_info: {},
            transaction_info: {},
            lend_transaction: {},
            product_code: '705',
            product_name: '投资',
        };
        $scope.app_status = '';
        $scope.state='';
        $scope.act_status='';
        if($scope.applicationId) {
            creditService.investquery(
                $scope.applicationStatus,
                $scope.bus_type,
                $scope.pj_type,
                $scope.openning_bank,
                $scope.open_name,
                $scope.account,
                $scope.big_num
            ).success(function (resp) {
                    for (var i = 0; i < resp.data.length; i++) {
                        if ($scope.applicationId == resp.data[i].application_info.id) {
                            $scope.app_status = resp.data[i].application_info.status;

                        }
                    }
                   
                    if($scope.app_status == '总行行长终审') {
                        $scope.act_status == '禁止';
                    }else{
                        creditService.querystatus({'application_id': $scope.applicationId, 'app_status': $scope.app_status}).success(function (resp) {
                            $scope.act_status = resp.data.act_status;

                            if (resp.data.msg == '投资申请未提交') {//晚一步。==投资申请 签署按钮
                                $scope.state = "不显示";

                            } else if ($scope.app_status == '资金分管行长审查') {//晚一步。== 投资委员会审议  签署按钮
                                $scope.state = "不显示";
                            }

                        });
                    }
             });
        }else{
            $scope.state="不显示";
            $scope.act_status='审议';
        }
        $scope.saveapprove = function () {
            creditService.saveapprove($scope.form_data).then(function (resp) {
                $scope.save = '保存';
                alert("保存成功");
            });
        }
        $scope.changeapprove = function () {
            if ($scope.applicationId) {
                $scope.save = '修改';
            } else {
                alert("您已存储,请查询后修改");
            }
        }
        $scope.onSubmit = function () {
            if ($scope.save == '保存') {
                creditService.invest_submit({'applicationId': $scope.applicationId})
                    .success(function (resp) {

                        $scope.submitedFlag = true;
                        $scope.next_step = resp.data.next_step;
                        if ($scope.next_step.length > 0) {
                            $("#tab_" + $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                        } else {
                            alert('审批完成');
                        }
                    });
            } else {
                alert("请先存数据！");
            }
        }
        $scope.approveActivityFlag = false;
        $scope.approveCommitteeActivityFlag = false;
        $scope.submitedFlag = false;
        $scope.examine = function () {
            if ($scope.applicationId) {
                $scope.approveActivityFlag = true;
                $scope.btn_edit_flag = false;
                $scope.loan_type_page = $scope.product_page
                $scope.Page = 'views/credit/invest/' + $scope.loan_type_page + '.html'
                $scope.form_data.product_name = $scope.product_name
                creditService.get($scope.applicationId).success(function (resp) {
                    $scope.form_data.transaction_info = resp.data.transaction_info;
                    $scope.form_data.application_info = resp.data.application_info;
                    $scope.form_data.lend_transaction = resp.data.lend_transaction;
                    $scope.ltSelected = false;
                    if ($scope.form_data.lend_transaction == null) {
                        $scope.form_data.lend_transaction = {}
                        var d = new Date();
                        var Y = d.getFullYear();
                        var M = d.getMonth() + 1;
                        if (M < 10) M = '0' + M
                        var D = d.getDate();
                        if (D < 10) D = '0' + D
                        $scope.form_data.lend_transaction.from_date = Y + '-' + M + '-' + D;
                    }
                    $scope.money.amount = app_money_char($scope.form_data.transaction_info.amount)[1];
                });

            }
        }
        $scope.examine();
        //格式转换
        //日期
        $scope.from_date = function (data) {
            $scope.form_data.application_info.from_date = app_date_ch(data);
        }
        $scope.thur_date = function (data) {
            $scope.form_data.application_info.thur_date = app_date_ch(data);
            console.log($scope.thur_date);
        }
        //金额
        $scope.amount = function (data) {
            $scope.form_data.transaction_info.amount = data;
            $scope.money.amount = app_money_char(data)[1];
        }
        $scope.approve = function () {
            approvalService.approve($scope.applicationId, {'comment_type': '同意', 'comment': $scope.result})
                .success(function (resp) {
                    if (resp.data.success) {
                        $scope.submitedFlag = true;
                        $scope.next_step = resp.data.next_step;
                        if ($scope.next_step.length > 0) {
                            $("#tab_" + $scope.tabId + "_content").find("div[name='next_step_modal']").modal("show");
                        } else {
                            alert('审批完成');
                        }
                    } else {
                        alert(resp.data.msg)
                    }
                });

        };
        $scope.reject = function () {
            approvalService.approve($scope.applicationId, {'comment_type': '不同意', 'comment': $scope.result})
                .success(function (resp) {
                    $scope.submitedFlag = true;
                    alert('提交成功');
                });

        };

    });

//生成右边侧栏tab 
ysp.controller('investDetailController', function ($scope, $compile, creditService, userService) {
    /*tab动态增加功能*/
    $scope.money = {};
    $scope.data = {};
    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab

    var defaultEvent = {
        'on': function () {
            return true;
        }
    };
    $scope.addSubTab = function (tabName, htmlContent, eventObj, autoFocus) {
        var t = new Object();
        t.index = $scope.subTabIndex;
        t.tabName = tabName;
        t.htmlContent = htmlContent;
        t.createEvent = eventObj.create ? eventObj.create : defaultEvent;
        t.closeEvent = eventObj.close ? eventObj.close : defaultEvent;
        t.focusEvent = eventObj.focus ? eventObj.focus : defaultEvent;
        t.loseFocusEvent = eventObj.loseFocus ? eventObj.loseFocus : defaultEvent;

        $scope.subTab[t.index] = t;
        var tabContentId = $scope.subTabCreate(t);
        $scope.subTabIndex = $scope.subTabIndex + 1;

        if (autoFocus == true) {
            $scope.changeFocus(t.index);
        }
        return t.index;
    };

    $scope.subTabCreate = function (tabObj) {
        succ_flag = $scope.subTab[tabObj.index].createEvent.on();
        if (succ_flag == true) {
            // 多个Tab打开,使用$scope.$id 唯一标示
            var tabId = 'loan_tab_' + $scope.$id + '_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            var tabHtml = '<li id="' + tabId + '" ng-click="changeFocus(' + tabObj.index + ')"> <a href="#' + tabContentId + '" data-toggle="tab">' + tabName + '</a></li>';
            var tabContentHtml = '<div class="tab-pane" id="' + tabContentId + '"></div>';
            baseScope = angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find("div[name='tabContent']").scope();
            scope = baseScope.$new();
            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);

            angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find("ul[name='tab']").append(tabElement);
            angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find("div[name='tabContent']").append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);

            return tabContentId;
        } else {
            alert("tab 创建失败");
        }
        ;
    };

    $scope.changeFocus = function (focus_tabId) {
        $scope.subTabLoseFocus($scope.currIndex);
        $scope.subTabFocus(focus_tabId);
        $scope.currIndex = focus_tabId;
    };

    $scope.subTabLoseFocus = function (index) {
        succ_flag = $scope.subTab[index].loseFocusEvent.on();
        if (succ_flag == true) {
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index)).removeClass("ng-scope active").addClass("ng-scope");
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index + '_content')).removeClass("tab-pane active").addClass("tab-pane");
        } else {
            alert("失焦失败！");
        }
    };

    $scope.subTabFocus = function (index) {
        succ_flag = $scope.subTab[index].focusEvent.on();
        if (succ_flag == true) {
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index)).addClass("active");
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index + '_content')).removeClass("tab-pane").addClass("tab-pane active");
        } else {
            alert("聚焦失败！");
        }
    };

    $scope.subTabClose = function (index) {
        succ_flag = $scope.subTab[index].closeEvent.on();
        if (succ_flag == true) {
            if (index == $scope.currIndex) {
                var prevElement = angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index)).prev();
                var nextElement = angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index)).next();
                if (prevElement.length > 0) {
                    $scope.changeFocus(prevElement.attr('id').split('_')[3]);
                } else if (nextElement.length > 0) {
                    $scope.changeFocus(nextElement.attr('id').split('_')[3]);
                } else {
                    $scope.changeFocus(0);
                }
            }
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index)).remove();
            angular.element(document.getElementById('loan_tab_' + $scope.$id + '_' + index + '_content')).remove();
            delete $scope.subTab[index];
        } else {
            alert("关闭失败！");
        }
    };
    $scope.init = function () {
        $scope.addSubTab('投资申请', '<div ng-include="' + '\'views/credit/invest/investInfo.html' + '\'"></div>', {}, false);
        $scope.addSubTab('投资影像', '<div ng-include="' + '\'views/credit/image/elecImage.html' + '\'"></div>', {}, false);
        $scope.addSubTab('流程意见', '<div ng-include="' + '\'views/credit/CreditApproval/index.html' + '\'"></div>', {}, false);
        $scope.subTabFocus(0);
    };
    $scope.init();
});

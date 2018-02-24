/*贷款申请——抵质押物生成合同*/
ysp.controller('guaranteeContractController', function ($scope, $rootScope, LOCAService, CustomerSearchService, PledgeService, contractService) {
    $scope.tableHead = ['合同编号', '申请书号', '客户名称', '合同类型', '合同金额', '到期日期', '操作'];
    $scope.tableData = [];
    $scope.queryCond = {};
    $scope.tableMessage = '请点击查询';
    $scope.queryContract = function () {
        console.log($scope.queryCond.contract_no);
        console.log($scope.queryCond.gty_method);
        contractService.query($scope.queryCond.contract_no,$scope.queryCond.gty_method).success(function (resp) {
            $scope.tableData = resp.data;
            if ($scope.tableData.length > 0) {
                $scope.tableMessage = '';
            } else {
                $scope.tableMessage = '未查询到数据';
            }
        });
    };
    $scope.contractDetail = function (data) {
        var cust_name = data.guarantee_info.gty_customer_name
        var gty_method = data.guarantee_info.gty_method;
        var tabName = cust_name + '的' + gty_method + '合同详情';
        var htmlContent = '<div ng-include="' + '\'views/credit/GuaranteeInformation/guaranty/index.html' + '\'" ></div>';
        var eventObj = {'create': '', 'focus': '', 'loseFocus': '', 'close': '', };
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {
            'contract_id': data.contract.contract_id,
            'gty_detail': data.guarantee_info.gty_detail,
            'gty_info_id':data.guarantee_info.id
        });
    }
});
ysp.controller('contractDetailController', function ($http, $scope, $rootScope, $compile, customerService, CustomerSearchService, guaranteeInfoService, PledgeService, MortgageService, contractService) {
    $scope.data = {
        'customer': $scope.customer,
        'contract': {},
        'guarantee_info': {}
    };
    $scope.onContract = function () {
        contractService.save_gty($scope.data).success(function (rsp) {
            $scope.data.contract = rsp.data.contract;
            $scope.guarantee_info.contract_no = rsp.data.contract.contract_no;
            alert('生成成功');
        });
    };
    $scope.PaperContract = function () {
        //  获取用户信息做合同信息用   return $http.get(base_url+'/customers/'+customer_id);
        PledgeService.PaperContract().success(function (resp) {
            console.log(resp);
            console.log("---------------");
        });
        //anular.element('#a_modal').modal('show');


    };
    if ($scope.contract_id) {
        contractService.get($scope.contract_id).success(function (rsp) {
            $scope.data.contract = rsp.data.contract;
            $scope.data.guarantee_info = rsp.data.guarantee_info;
        });
    } else if ($scope.gty_info_id) {
        guaranteeInfoService.query($scope.gty_info_id).success(function (rsp) {
            $scope.data.guarantee_info = rsp.data.guarantee_info;
            if (rsp.data.guarantee) {
                rsp.data.guarantee.ins_due_date = new Date(rsp.data.guarantee.ins_due_date);
                $scope.modal_data = rsp.data.guarantee;
            }
        });
    }
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
        $scope.line = 0;
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
        guaranteeInfoService.query($scope.gty_info_id).success(function (resp) {
            $scope.guarantee_info = resp.data.guarantee_info;
            guaranteeInfoService.methods().success(function (resp) {
                //alert($scope.activity_status);
                var pledge_type = $scope.guarantee_info.gty_detail;
                var url = 'index.html';
                var pledge_method = $scope.guarantee_info.gty_method;
                var data = resp.data;
                for (var i = 0; i < data.length; i++) {
                    if (data[i].detail == pledge_type) {
                        //alert($scope.activity_status);
                        if ($scope.activity_status == '审批') {
                            len = data[i].detail_page.length;
                            tempStr = data[i].detail_page.substr(0, len - 1);
                            tempStr = tempStr + 'b';
                            url = tempStr + '.html';
                        } else {
                            url = data[i].detail_page + '.html';
                        }
                        // alert(url);
                    }
                }
                guaranteeInfoService.query_party($scope.guarantee_info.customer_name).success(function (party) {
                    $scope.guarantee_info.contract_no = $scope.contract_no;
                    $scope.type_code = party.data.party.type_code;
                    // $scope.type_code='company';
                    $scope.addSubTab('合同详情', '<div ng-include="' + '\'views/credit/CreditContract/mrge_contract.html' + '\'"></div>', {'guarantee_info': $scope.guarantee_info,'activity_status': $scope.activity_status}, true);
                    if (pledge_method == '质押' || pledge_method == '抵押') {
                        var tabName = pledge_type + '信息';
                        $scope.addSubTab(tabName, '<div ng-include="' + '\'views/credit/GuaranteeInformation/pledge/' + url + '\'"></div>', {}, false);
                        $scope.subTabFocus(0);
                    }

                });
            });
        });
    };
    /**
     * customer search
     */
    $scope.show_customer_model = function (customer_modal) {
        $scope.confirmBtnDisabled = false;
        $scope.customer_model_target = customer_modal;
        angular.element('#guarantree_customer_modal').modal('show');
    };

    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = {'cust_name': ''};
    $scope.chosenCust = null;

    $scope.customer_search = function () {
        /*
         customerService.query($scope.cust_search.cust_name).success(function (resp) {
         $scope.custTableData = resp.data;
         });*/
        CustomerSearchService.queryroleparty($rootScope.user_session).success(function (resp) {
            console.log(resp.data.party);
            $scope.custTableData = resp.data.party;
            console.log($scope.custTableData);
        });
    };
    $scope.customer_select = function (cust, $event) {
        $scope.chosenCust = cust;
        var obj = event.srcElement;
        var oTr = obj.parentNode;
        var tableObj = angular.element(document.getElementById('tab_' + $scope.tabId + '_content'))
            .find("table[name='custListTable']")[0];
        for (var i = 1; i < tableObj.rows.length; i++) {
            tableObj.rows[i].style.backgroundColor = "";
            tableObj.rows[i].tag = false;
        }
        oTr.style.backgroundColor = "#87CEFA";
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

     $scope.customer_confirm_select = function () {
        $scope.confirmBtnDisabled = true;
        if ($scope.chosenCust == null) {
            alert('请先选择申请的客户');
        }
        ;
        if ($scope.customer_model_target === 'gty_customer') {                              // 担保人客户代码
            console.log($scope.chosenCust);
            //$scope.guarantee_info.gty_customer_id  = $scope.chosenCust.id;
            $scope.guarantee_info.gty_customer_no = $scope.chosenCust.no;
            $scope.guarantee_info.gty_customer_name = $scope.chosenCust.name;

        } else if ($scope.customer_model_target === 'own_customer') {                       // 所有人客户代码
            //$scope.guarantee_info.own_customer_id = $scope.chosenCust.id;
            $scope.guarantee_info.own_customer_no = $scope.chosenCust.no;
            $scope.guarantee_info.own_customer_name = $scope.chosenCust.name;
        } else if ($scope.customer_model_target === 'share_customer') {                     // 共有人客户代码
            ///$scope.guarantee_info.share_customer_id = $scope.chosenCust.id;
            $scope.guarantee_info.share_customer_no = $scope.chosenCust.no;
            $scope.guarantee_info.share_customer_name = $scope.chosenCust.name;
        }
        angular.element('#guarantree_customer_modal').modal('hide');
    };

    $scope.customer_cancel_select = function () {
        angular.element('#guarantree_customer_modal').modal('hide');
    };


    /** 抵质押物保存 **/
    $scope.init();
    $scope.save = '修改';
    $scope.modal_data = {};
    $scope.modal_data.gty_type = '最高额担保';
    $scope.modal_data.gty_method = '质押';
    $scope.modal_data.gty_ct = '人民币';
    $scope.modal_data.bfirst_gty = '是';
    $scope.modal_data.bboard_appr = '是';
    $scope.modal_data.reg_by = '00510';
    $scope.modal_data.reg_org_id = '乌海银行-总行';
    $scope.modal_data.gty_info_id = $scope.gty_info_id;
    //质押-其他 保存
    $scope.pledgechange = function () {
        $scope.save = '保存';
    };


    $scope.PawnOtherSave = function () {
        $scope.modal_data.pledge_type = '质押-其他';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });

        } else {
            PledgeService.othersave($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("保存成功 ");
            });
        }


    };
    //质押-单位定期存单 保存
    $scope.PawnStubSave = function () {
        $scope.modal_data.pledge_type = '质押-单位定期存单';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            PledgeService.stubsave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    //质押-账户资金 保存
    $scope.PawnSavingSave = function () {
        $scope.modal_data.pledge_type = '质押-账户资金';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });

        } else {
            PledgeService.savingsave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    //质押-本行理财产品 保存
    $scope.PawnFinanceSave = function () {
        $scope.modal_data.pledge_type = '质押-本行理财产品';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            PledgeService.vch_qlfsave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    //质押-应收账款 保存
    $scope.PawnAccRecSave = function () {
        $scope.modal_data.pledge_type = '质押-应收账款';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            PledgeService.acc_recsave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.PawnPerStubSave = function () {
        $scope.modal_data.pledge_type = '质押-个人定期存单'

        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });

        } else {
            PledgeService.perstubsave($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        }
    };
    //质押-银行承兑汇票 保存
    $scope.PawnAccpSave = function () {
        $scope.modal_data.pledge_type = '质押-银行承兑汇票';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            PledgeService.accpsave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    //抵押 保存
    $scope.MrgeEqpMovableSave = function () {
        $scope.modal_data.pledge_type = '抵押-设备+动产'
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeEqpMovableSave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.MrgeBuildingSave = function () {
        $scope.modal_data.pledge_type = '抵押-房屋所有权';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeBuildingSave($scope.modal_data).success(function () {
                alert("保存成功 ");

                $scope.save = '修改'
            });
        }
    };
    $scope.MrgeEqpSave = function () {
        $scope.modal_data.pledge_type = '抵押-设备';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeEqpSave($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("保存成功 ");
            });
        }
    };
    $scope.MrgeLandSave = function () {
        $scope.modal_data.pledge_type = '抵押-土地使用权';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeLandSave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.MrgeOtherSave = function () {
        $scope.modal_data.pledge_type = '抵押-其他';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeOtherSave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.MrgeVchSave = function () {
        $scope.modal_data.pledge_type = '抵押-交通工具';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeVchSave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.MrgeMovableSave = function () {
        $scope.modal_data.pledge_type = '抵押-动产';
        if ($scope.modal_data.gty_id) {
            PledgeService.update($scope.modal_data).success(function () {
                $scope.save = '修改'
                alert("修改成功 ");
            });
        } else {
            MortgageService.MrgeMovableSave($scope.modal_data).success(function () {
                alert("保存成功 ");
                $scope.save = '修改'
            });
        }
    };
    $scope.Info_Saves = function () {
        guaranteeInfoService.InfoSave($scope.guarantee_info).success(function (resp) {
            alert('提交成功')
        });
        guaranteeInfoService.InfoSaves($scope.guarantee_info).success(function (resp) {
            alert('信息已完善')
        });
    }
    $scope.Info_Save = function () {
        // $scope.guarantee_info.application_id = $scope.application_id;
        console.log($scope.guarantee_info);
        guaranteeInfoService.InfoSave($scope.guarantee_info).success(function (resp) {
            alert('保存成功')
        });
        /* $scope.guarantee_info.application_id = $scope.application_id;
         guaranteeInfoService.save($scope.guarantee_info).success(function (resp) {
         alert(resp.data.msg);
         angular.element('#guarantree_modal').modal('hide');
         query_guarantee();
         });*/
    }
    //日期转换
    $scope.mort_reg_date = function () {
        $scope.modal_data.mort_reg_date = app_date_ch($scope.modal_data.mort_reg_date);
    }
    $scope.eval_date = function () {
        $scope.modal_data.eval_date = app_date_ch($scope.modal_data.eval_date);
    }
    $scope.bought_date = function () {
        $scope.modal_data.bought_date = app_date_ch($scope.modal_data.bought_date);
    }
    $scope.bought_date1 = function () {
        $scope.modal_data.bought_date1 = app_date_ch($scope.modal_data.bought_date1);
    }
    $scope.mort_reg_date1 = function () {
        $scope.modal_data.mort_reg_date1 = app_date_ch($scope.modal_data.mort_reg_date1);
    }
    $scope.eval_date1 = function () {
        $scope.modal_data.eval_date1 = app_date_ch($scope.modal_data.eval_date1);
    }
    $scope.bought_date2 = function () {
        $scope.modal_data.bought_date2 = app_date_ch($scope.modal_data.bought_date2);
    }
    $scope.mort_reg_date2 = function () {
        $scope.modal_data.mort_reg_date2 = app_date_ch($scope.modal_data.mort_reg_date2);
    }
    $scope.eval_date2 = function () {
        $scope.modal_data.eval_date2 = app_date_ch($scope.modal_data.eval_date2);
    }
});
ysp.controller('lendContractController', function ($scope, $rootScope, LOCAService, CustomerSearchService, PledgeService, contractService) {
    $scope.tableHead = ['合同编号', '客户名称','贷款类型', '合同金额', '起始时间','到期日期', '操作'];
    $scope.tableData = [];
    $scope.queryCond = {};
    $scope.tableMessage = '请点击查询';
    $scope.queryContract = function () {
        contractService.query_lend($scope.queryCond).success(function (resp) {
            $scope.tableData = resp.data;
            if ($scope.tableData.length > 0) {
                $scope.tableMessage = '';
            } else {
                $scope.tableMessage = '未查询到数据';
            }
        });
    };
    $scope.contractDetail = function (data) {
        var tabName = data.party.name+'的合同详情';
        var htmlContent = '<div ng-include="' + '\'views/credit/pageDistribute/index.html' + '\'" ></div>';
        var eventObj = {'create': '', 'focus': '', 'loseFocus': '', 'close': '', };
        var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {
           'activity_page':'loanApplication','applicationId':data.application_info.id,'customer':data.party
        });
    }
});

ysp.controller('lendDetailController', function ($scope, $rootScope, LOCAService, CustomerSearchService, PledgeService, contractService) {
       angular.element("div[name='loanDetailForm']").find("input,select,textarea").attr('disabled','disabled'); 
});


ysp.controller('guarantyController', function ($scope, $rootScope, guaranteeInfoService) {
    $scope.show_new_pledge_modal = function () {
        $("#tab_" + $scope.tabId + "_content").find("div[name='new_pledge_modal']").modal("show");
    };
    $scope.init_pledge_type = function () {
        var tree_html = '<ul id="pledge_type_tree' + $scope.tabId + '" class="ztree"> </ul>';
        angular.element($('#tab_' + $scope.tabId + '_content').find("div[name='for_pledge_mortgage_tree']")).append(tree_html);
        var Nodes = [];
        var setting = {};
        var gua_list = [];
        var gua_details = [];
        guaranteeInfoService.methods().success(function (resp) {
            var data = resp.data;
            for (var i = 0; i < data.length; i++) {
                var gua = data[i]
                if (gua.name == '质押') {
                    gua_details.push(gua)
                }
            }
            gua_list.push({'name': '质押', 'details': gua_details});
            gua_details = [];
            for (var i = 0; i < data.length; i++) {
                var gua = data[i]
                if (gua.name == '抵押') {
                    gua_details.push(gua)
                }
            }
            gua_list.push({'name': '抵押', 'details': gua_details});
            show_methods(gua_list)
            $.fn.zTree.init($("#pledge_type_tree" + $scope.tabId), setting, Nodes);
        });
        function show_methods(data) {
            for (var i = 0; i < data.length; ++i) {
                var One = new Object();
                One.name = data[i].name;
                pro_arr = data[i].details;
                One.children = new Array();
                if (pro_arr.length > 0) {
                    for (var j = 0; j < pro_arr.length; ++j) {
                        var Two = new Object();
                        Two.name = pro_arr[j].detail;
                        Two.click = "choose_pledge_type(this, '" + pro_arr[j].detail + "','" + pro_arr[j].detail_page + "')";
                        One.children.push(Two);
                    }
                }
                Nodes.push(One);

            }
        }
    };
    $scope.show_pledge_modal = function () {
        $("#tab_" + $scope.tabId + "_content").find("div[name='new_pledge_modal']").modal("show");
    };
    $scope.choose_pledge = function (node_id, p_type, page) {
        $scope.p_type = p_type;

        $scope.detail_page = 'views/credit/GuaranteeInformation/pledge/' + page + '.html'
    };
    $scope.init_pledge_type();
    $scope.pledgeModalConfirm = function () {
        $scope.ltSelected = false;
    };

    $scope.pledgeModalClose = function () {
        $scope.choosePledgeFormName = null;
    };
});
ysp.controller('pledgeController', function ($scope, PledgeService, MortgageService) {
    $scope.modal_data = {};
    $scope.save = '修改';
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
    //金额转换
    $scope.pawn_amount = function () {
        //     $scope.modal_data.pawn_amount = {{$scope.modal_data.pawn_amount|number:2}};
    }
    /*
     //质押-其他 保存
     $scope.PawnOtherSave = function(){
     $scope.modal_data.pledge_type = '质押-其他'
     PledgeService.othersave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-个人定期存单 保存
     $scope.PawnPerStubSave = function(){
     $scope.modal_data.pledge_type = '质押-个人定期存单'
     PledgeService.perstubsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-单位定期存单
     $scope.PawnStubSave = function(){
     $scope.modal_data.pledge_type = '质押-单位定期存单'
     PledgeService.stubsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-账户资金 保存
     $scope.PawnSavingSave = function(){
     $scope.modal_data.pledge_type = '质押-账户资金'
     PledgeService.savingsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-本行理财产品 保存
     $scope.PawnFinanceSave = function(){
     $scope.modal_data.pledge_type = '质押-本行理财产品'
     PledgeService.vch_qlfsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-应收账款 保存
     $scope.PawnAccRecSave = function(){
     $scope.modal_data.pledge_type = '质押-应收账款'
     PledgeService.acc_recsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //质押-银行承兑汇票 保存
     $scope.PawnAccpSave = function(){
     $scope.modal_data.pledge_type = '质押-银行承兑汇票'
     PledgeService.accpsave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     //抵押 保存
     $scope.MrgeEqpMovableSave = function(){
     $scope.modal_data.pledge_type = '抵押-设备+动产'
     MortgageService.MrgeEqpMovableSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeBuildingSave = function(){

     $scope.modal_data.pledge_type = '抵押-房屋所有权'
     MortgageService.MrgeBuildingSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeEqpSave = function(){
     $scope.modal_data.pledge_type = '抵押-设备'
     MortgageService.MrgeEqpSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeLandSave = function(){

     $scope.modal_data.pledge_type = '抵押-土地使用权'

     MortgageService.MrgeLandSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeOtherSave = function(){
     $scope.modal_data.pledge_type = '抵押-其他'
     MortgageService.MrgeOtherSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeVchSave = function(){
     $scope.modal_data.pledge_type = '抵押-交通工具'
     MortgageService.MrgeVchSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     $scope.MrgeMovableSave = function(){
     $scope.modal_data.pledge_type = '抵押-动产'
     MortgageService.MrgeMovableSave($scope.modal_data).success(function(){
     alert("保存成功 ");
     });
     };
     */
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
});
ysp.controller('pledgeUpController', function ($scope, PledgeService, MortgageService) {
    /*
     // 修改
     $scope.PawnOtherSave = function(){
     $scope.modal_data.pledge_type = '质押-其他'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnPerStubSave = function(){
     $scope.modal_data.pledge_type = '质押-个人定期存单'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnStubSave = function(){
     $scope.modal_data.pledge_type = '质押-单位定期存单'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnFinanceSave = function(){
     $scope.modal_data.pledge_type = '质押-本行理财产品'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnSavingSave = function(){
     $scope.modal_data.pledge_type = '质押-账户资金'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnAccpSave = function(){
     $scope.modal_data.pledge_type = '质押-银行承兑汇票'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.PawnAccRecSave = function(){
     $scope.modal_data.pledge_type = '质押-应收账款'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeBuildingSave = function(){
     $scope.modal_data.pledge_type = '抵押-房屋所有权'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeLandSave = function(){
     $scope.modal_data.pledge_type = '抵押-土地使用权'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeEqpSave = function(){
     $scope.modal_data.pledge_type = '抵押-设备'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeEqpMovableSave = function(){
     $scope.modal_data.pledge_type = '抵押-设备+动产'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeMovableSave = function(){
     $scope.modal_data.pledge_type = '抵押-动产'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeVchSave = function(){
     $scope.modal_data.pledge_type = '抵押-交通工具'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     $scope.MrgeOtherSave = function(){
     $scope.modal_data.pledge_type = '抵押-其他'
     PledgeService.update($scope.modal_data).success(function(){
     alert("修改成功 ");
     });
     };
     */
    $scope.save = '修改';
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
});

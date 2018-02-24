ysp.controller('customerController', function($scope, $rootScope, customerService){
    $scope.displayInfo= function(tabName){
        $scope.display_info = tabName;
    };
    $scope.search_customer_name ='';
    $scope.customer_list=[];
    $scope.query_customer = function(){

        customerService.query($scope.search_customer_name).success(function(resp){
            $scope.customer_list = resp.data;
        });
        $scope.query_company_customer();
    };
    $scope.query_company_customer = function(){
          customerService.query_company($scope.search_customer_name).success(function(resp){
                $scope.org_list = resp.data;
          });
    };
    $scope.init = function(){
        return;
        $scope.display_info= "personalInformation";
        $scope.query_customer();
    };
    $scope.init();
     //关联个人
    $scope.associPerson = function(associate,party_id){
	    console.log(party_id);
        var tabName = '个人客户';
        var htmlContent = '<div ng-include="'+'\'views/customer/person/pre_add.html' +'\'"></div>'; 
        var tab_id = $rootScope.addTab(tabName, htmlContent, {}, true, {'associate':associate, 'party_id':party_id});   
    }
    //关联对公
    $scope.associCompany = function(associate,party_id){
        var tabName = '对公客户'; 
        var htmlContent = '<div ng-include="'+'\'views/customer/company/com_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, {}, true, {'associate':associate}); 
        tabScope = angular.element(document.getElementById('tab_'+ tab_id + '_content')).scope();
    }
  
})

.service('customerService', function($http){
    return {
        query:function(customer_name){
            return $http.get(base_url+'/customers?customer_name='+customer_name)
        },
        query_company:function(customer_name){
            return $http.get(base_url+'/customers/company?customer_name='+customer_name)
        },
        query_persons:function(custNo, custName, certType, certNo){
            return $http.get(base_url+'/customers/persons/?custNo='+custNo+'&custName='+custName+'&certType='+certType+'&certNo='+certNo)  
        },
    }
})
.controller('personalInformationController',function($scope, personalInformationService,industryService, store, $rootScope){
    $scope.customer_id = null;
    $scope.form_data ={'customer':{},'emp':{},'family':{},'certificate':{}, 'contact':{}, 'per_card':{},'per_bus':{}, 'opt':{}, 'spouse':{}, 'spouse_telephone':{}, 'spouse_mobile_phone':{}};
    $scope.form_data.certificate.cert_type='身份证';
    $scope.disabled_flag=true;
    $scope.spouse_disabled_flag = true;
    $scope.spou_btn_disabled = true;
    $scope.save = function(){
        $scope.form_data.state='完善'
        console.log($scope.form_data);
        $scope.disabled_flag = true;
        $scope.spouse_disabled_flag = true;
        if($scope.customer_id){
            if($scope.industry_top && $scope.industry_big && $scope.industry_mid && $scope.industry_small){
                    $scope.form_data.per_card.industry_top=$scope.industry_top;
                    $scope.form_data.per_card.industry_big=$scope.industry_big;
                    $scope.form_data.per_card.industry_mid=$scope.industry_mid;
                    $scope.form_data.per_card.industry_small = $scope.industry_small;
            }
            personalInformationService.update($scope.customer_id, $scope.form_data).success(function(resp){
                   alert('保存成功')
                   $scope.query($scope.customer_id);
            });
        }
    };
    $scope.add = function(){
        $scope.add_btn_disabled = false;
        $scope.associPerson('spouseInfo',$scope.customer_id);
    }
    $scope.queryspou = function(){
        $scope.spou_btn_disabled = false;
        personalInformationService.query_spou($scope.customer_id).success(function(resp){
            console.log(resp)
            if(resp.data){
                $scope.form_data.spouse = resp.data.customer;
            }
        })
    }

    $scope.phone_number = function(data){
        console.log(data)
        if(data.length > 60){
            alert('最多存储5个手机号');
            $scope.form_data.mobile_phone.phone_number = '';
            return ;
        }else if(data != undefined){
            var list = new Array();
            list = data.split("，");//中文逗号
            for(var i=0; i<5;i++){
                console.log(list[i])
                if(list[i] == undefined){
                    return;
                }
                if(list[i].length > 11){
                    var num = i*1 +1;
                    var msg = '第'+ num +'个号码不正确';
                    alert(msg);
                }
            }
        }
    }

    $scope.marital_status = function(){
        if($scope.form_data.customer.marital_status != '已婚'){
           $scope.spouse_disabled_flag = true;
        }else{
            $scope.spouse_disabled_flag = false;
            $scope.spou_btn_disabled = true;
            $scope.add_btn_disabled = true;
        }
    }
    $scope.marital_status();
    $scope.submit = function(d){
        if (!d) {
           alert('请输完必填项');
        }else if($scope.form_data.customer.marital_status == '已婚'){
            if($scope.form_data.spouse.current_name != null 
                && $scope.form_data.spouse.ric != null){
                alert('请补全配偶信息')
                return ;
            }
        }else{
           $scope.disabled_flag = true;
           $scope.spouse_disabled_flag = true;
           if($scope.customer_id){
                $scope.save()
               /*
               personalInformationService.update($scope.customer_id, $scope.form_data).success(function(resp){
                   $scope.query($scope.customer_id);
               });
               */
           }else{
               personalInformationService.create($scope.form_data).success(function(resp){
                    alert('创建成功')
               });
           }
        }
    };
        
    $scope.edit = function(){
        industryService.query_cust($scope.customer.id).success(function(resp){
           var ls = resp.data;
           if(ls.length == 4 && ls.indexOf(null) == -1){
               showIndustry(ls);
           }   
           else{
               $scope.initIndustry();
           }
        })
        $scope.disabled_flag = false;
        if($scope.form_data.customer.marital_status != '已婚'){
            $scope.spouse_disabled_flag = true;
        }else{
            $scope.spouse_disabled_flag = false;
        }  
    }

    $scope.clear = function(){
        $scope.form_data ={'customer':{},'emp':{},'family':{},'certificate':{}, 'contact':{}, 'per_card':{},'per_bus':{}, 'opt':{}, 'spouse':{}, 'spouse_telephone':{}, 'spouse_mobile_phone':{} };
        $scope.form_data.certificate.cert_type='身份证'
    };
    
    $scope.query = function(customer_id){
        personalInformationService.query(customer_id).success(function(resp){
	    
	    var list = resp.data.contact;
	    $(list).each(function(i,item){
		    if(item.type_code=="phone"){
			    if(item.phone_type=="手机号码"){
				    $scope.form_data.mobile_phone=item;//.phone_number;
		        }
                else if(item.phone_type=="电话号码"){
				    $scope.form_data.telephone=item;//.phone_number;
				}
			}
		    else if(item.type_code=="email"){
			    email=item.email_address;
			}
		//如果有地址传入则添加一个else if
		});
        // 工作,证件,基本,家庭信息,个人贷款卡,个体工商户
	    $scope.form_data.emp=resp.data.emp;
        $scope.form_data.certificate = resp.data.certificate;
        $scope.form_data.customer = resp.data.customer;
	    $scope.form_data.family=resp.data.family;
	    $scope.form_data.per_card=resp.data.per_card;
	    $scope.form_data.per_bus=resp.data.per_bus;
        //行业为空不能提交问题
        if($scope.form_data.per_card != null){
            $scope.industry_top = $scope.form_data.per_card.industry_class;
            $scope.industry_big = $scope.form_data.per_card.industry_large_class;
            $scope.industry_mid = $scope.form_data.per_card.industry_mid_class;
            $scope.industry_small = $scope.form_data.per_card.industry_small_class;
        }else{
            industryService.query_cust($scope.customer.id).success(function(resp){
                var ls = resp.data;
                if(ls.length == 4 && ls.indexOf(null) == -1){
                    showIndustry(ls);
                }else{
                    $scope.initIndustry();
                }
            });
        }
        if($scope.form_data.per_card && $scope.form_data.per_card.reg_institution == null){
            $scope.form_data.per_card.reg_institution = store.getSession("branch_code")+ '-' + store.getSession("branch_name");
        }
        });
    }
    $scope.initIndustry = function(){
       $scope.industry_top=null;
       $scope.industry_big=null;
       $scope.industry_mid=null;
       $scope.industry_small=null;
       $scope.industry_topList=[];
       industryService.query('_').success(function(resp){
            console.log('person industry');
           $scope.industry_topList = resp.data;
       });
    
    } 
    $scope.initIndustry();   
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
    $scope.industry_select=function(para,which){
        console.log(which+'-'+para)
       if (which == 'big'){
            industryService.query(para.substring(0,1)+'__').success(function(resp){
           // console.log('industry');
                $scope.industry_bigList = resp.data;
                $scope.industry_top=para
                $scope.industry_big=null;
                $scope.industry_mid=null;
                $scope.industry_small=null;
             });   
             $scope.industry_midList = null;
             $scope.industry_smallList = null;     
        }else if(which == 'mid'){
            industryService.query(para.substring(0,3)+'_').success(function(resp){
           // console.log('industry');
                $scope.industry_midList = resp.data;
                $scope.industry_big=para
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
    
    // 新增或是查看
    if ($scope.$parent.customer != undefined){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id);
        $scope.queryspou($scope.customer_id);
    }else{
        $scope.disabled_flag=false;
        if(data != '已婚'){
            $scope.spouse_disabled_flag = true;
        }else{
            $scope.spouse_disabled_flag = false;
        }
    }

})

.service('personalInformationService', function($http){
    return {
        create:function(data){
            return $http.post(base_url+'/customers', data)
        },
        query:function(customer_id){
            return $http.get(base_url+'/customers/'+customer_id)
        },
        update:function(customer_id, data){
            return $http.put(base_url+'/customers/'+customer_id, data)
        },
        query_spou:function(customer_id){
            return $http.get(base_url+'/customers/query_spou/'+customer_id);
        },
    }
})
.controller('relativesController', function($scope, relativesService){
    $scope.table_head=['证件号码', '姓名', '与该客户关系', '工作单位', '电话号码', '是否生效', '更新日期', '操作'];
    $scope.table_data=[];
    $scope.modal_data ={};
    
    
    $scope.refresh = function(customer_id){
        relativesService.query_relatives(customer_id).success(function(resp){
            console.log(resp.data)
            $scope.table_data=resp.data;
            console.log($scope.table_data)
            if(resp.data.length >0){
                $scope.tableMessage='';
             }else{
                $scope.tableMessage='未查询到数据';
            }
        })
    }

   if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
    }
    $scope.refresh($scope.customer_id);
    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }

    $scope.display_record = function(data){
        console.log(data)
        $scope.modal_title='客户亲属信息查看';
        $scope.modal_data.cust = data.cust_info;
        $scope.modal_data.fam = data.family;

        console.log($scope.modal_data)
        $scope.view("#relativesModal");
    };
    $scope.save = function(modal_data){
        $scope.disabled_flag=true;
        relativesService.update_relatives(modal_data).success(function(resp){
            alert('保存成功');
        });
    };


    $scope.init_modal = function(){
        $scope.disabled_flag=false;
    }

    // 关联客户打开
    $scope.customer_tab={};
    var eventObj = {
        'create':'',
        'focus':'',
        'loseFocus':'',
        'close':{
            'message': "关闭页面提示",
            'on':function(){
                alert(this.message);
                return true;
            },
        }
    }

    $scope.customerInfoDetail = function(cust){
        console.log(cust)
        var cust_id = cust.id;
        var cust_name = cust.name;
        var tabName = cust_name+'的客户信息';
        var htmlContent = '<div ng-include="'+'\'views/customer/index.html' +'\'"></div>';
        if($scope.customer_tab[cust_id] == undefined || $rootScope.tab[$scope.customer_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true);
            $scope.customer_tab[cust_id] = tab_id;
            tabScope = angular.element(document.getElementById('tab_'+ tab_id + '_content')).scope();
            tabScope['customer'] = cust;
        }else{
            alert("用户信息标签已打开");
        }
    }
})

.service('relativesService', function($http){
    return {
        query_relatives:function(customer_id){
            return $http.get(base_url+'/customers/query_relatives/'+customer_id);
        },
        update_relatives:function(modal_data){
            return $http.put(base_url+'/customers/update_relatives/', modal_data);
        },
    }
})

.controller('academicRecordController', function($scope){
    $scope.table_head=['开始日', '结束日', '所在学校', '所在院系', '专业', '学制', '学历', '登记日期', '更新日期', '操作'];
    $scope.table_data=[ 
        {
            'begin_date':'2000-01-01', 
            'end_date':'2004-01-01', 
            'school':'浙江大学', 
            'department':'计算机学院', 
            'pro':'软件专业', 
            'years':'4', 
            'xw':'学士',
            'xl':'大学本科',
            'xl_cert_no':'xxxxxxxxxx',
            'xw_cert_no':'xxxxxxxxxx',
            'comment':'xxxxxxxxxx',
            'register_branch':'xx银行xx支行', 
            'register_teller':'黄绮珊', 
            'register_date':'2014-01-01', 
            'update_date':'2014-01-01'
        },
        {
            'begin_date':'2004-01-01', 
            'end_date':'2008-01-01', 
            'school':'上海交通大学', 
            'department':'计算机学院', 
            'pro':'人工智能研究院', 
            'years':'4', 
            'xw':'学士',
            'xl':'研究生',
            'xl_cert_no':'xxxxxxxxxx',
            'xw_cert_no':'xxxxxxxxxx',
            'comment':'xxxxxxxxxx',
            'register_branch':'xx银行xx支行', 
            'register_teller':'黄绮珊', 
            'register_date':'2014-01-01', 
            'update_date':'2014-01-01'
        }
    ]
   
    $scope.init_modal = function(){
        $scope.modal_data = {};
    };

    $scope.save_data = function(modal){
        $scope.table_data.push(modal);
        $scope.init_modal();
    }

    $scope.new_record = function(){
        $scope.modal_data = {};
        $scope.modal_title='学历履历新增';
    };

    $scope.view_data = function(index){
        $scope.modal_title = '学历履历详情';
        $scope.modal_data = $scope.table_data[index];
    }
})
.controller('employmentsRecordController', function($scope){
    $scope.table_head=['开始日', '结束日', '所在单位', '所在部门', '担任职务', '登记日期', '更新日期', '操作'];
    $scope.table_data=[ 
        {
            'begin_date':'2010-01-01', 
            'end_date':'2014-01-01', 
            'company':'xxx单位', 
            'company_type':'事业、机关', 
            'address':'xxxxxxx',
            'telphone':'0571-66666666',
            'post_code':'0000000',
            'department':'xxxxxx部门', 
            'title':'xxxxx职位', 
            'income':12000,
            'register_branch':'xx银行xx支行', 
            'register_teller':'黄绮珊', 
            'register_date':'2014-01-01', 
            'update_date':'2014-01-01'
        }
    ]

    $scope.new_record = function(){
        $scope.modal_data = {};
        $scope.modal_title='工作履历新增';
    };
   
    $scope.save_data = function(modal){
        $scope.table_data.push(modal);
        $scope.modal_data={};
    }

    $scope.view_data = function(index){
        $scope.modal_data = $scope.table_data[index];
        $scope.modal_title='工作履历详情';
    }
})
.controller('bondController', function($scope){
    $scope.table_head=['统计截止日期', '债券类型', '购买总价格', '债券起始日期', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('intangibleAssetController', function($scope){
    $scope.table_head=['统计截止日期', '资产类型', '资产名称', '评估价值', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('investmentEnterpriseController', function($scope){
    $scope.table_head=['投向企业名称', '投资方式', '购买总价格', '实际投资金额', '登记机构', '登记人', '登记日期', '更新日期', '操作'];

})
.controller('lifeInsuranceController', function($scope){
    $scope.table_head=['统计截止日期', '保险名称', '投保日期', '保障金额', '退保时间', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('otherAssetController', function($scope){
    $scope.table_head=['资产类型', '价格金额', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('otherLiabilitiesController', function($scope){
    $scope.table_head=['开始日', '结束日', '所在学校', '所在院系', '专业', '学制', '登记日期', '更新日期', '操作'];
})
.controller('personalDocumentsController', function($scope){
    $scope.table_head=['记录日期', '文件名称', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('personalMemorabiliaController', function($scope){
    $scope.table_head=['发生日期', '事件类型', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
    $scope.table_data=[
        {
            'date':'2011-01-01', 
            'memo_type':'离婚', 
            'story':'由于家暴，妻子提出离婚，xxxxxx',
            'comment':'xxxxxxxx',
            'register_branch':'xx银行xx支行', 
            'register_teller':'黄绮珊', 
            'register_date':'2014-01-01', 
            'update_date':'2014-01-01'
        }
    ];
    $scope.view_record= function(index){
        $scope.modal_title="大事件详情";
        $scope.modal_data = $scope.table_data[index];
    };

    $scope.new_record = function(){
        $scope.modal_title="大事件新增";
        $scope.modal_data ={};
    }

    $scope.save_data = function(modal){
        $scope.table_data.push(modal);
        $scope.modal_data={};
    }
 
})
.controller('propertyInsuranceController', function($scope){
    $scope.table_head=['统计截止日期', '保险名称', '投保日期', '保障金额', '退保时间', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('realtyAssetsController', function($scope){
    $scope.table_head=['统计截止日期', '房屋名称', '房屋面积', '房屋地址', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('socialInsuranceController', function($scope){
    $scope.table_head=['统计截止日期', '社会保险种类', '余额', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('stockController', function($scope){
    $scope.table_head=['统计截止日期', '股票代码', '股票名称', '股票数量', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('vehicleController', function($scope){
    $scope.table_head=['统计截止日期', '车辆牌号', '车辆品牌', '买入价格', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('associatedPersonController', function($scope, $rootScope){
    $scope.customer_tab={};
    $scope.table_head=['姓名', '与该客户关系', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
    $scope.table_data=[
        {
            'id':3,
            'certificate_type':'身份证', 
            'certificate_number':330381198001010101, 
            'customer_name':'赵六', 
            'relationship':'远房亲戚', 
            'register_branch':'xx银行xx支行', 
            'register_teller':'黄绮珊', 
            'register_date':'2011-01-01', 
            'update_date':'2014-01-01'
        },
    ];

    var eventObj = {
        'create':'',
        'focus':'',
        'loseFocus':'',
        'close':{
            'message': "关闭页面提示",
            'on':function(){
                alert(this.message);
                return true;
            }
        }
    };



    $scope.tracing_customer = function(cust){
        var cust_id = cust.id;
        var cust_name = cust.customer_name;
        var tabName = '('+ cust.relationship +')'+cust_name;
        var htmlContent = '<div ng-include="'+'\'views/customer/index.html' +'\'"></div>';
        if($scope.customer_tab[cust_id] == undefined || $rootScope.tab[$scope.customer_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true);
            $scope.customer_tab[cust_id] = tab_id;
            tabScope = angular.element(document.getElementById('tab_'+ tab_id + '_content')).scope();
            tabScope['customer'] = cust;
        }else{
            alert("用户信息标签已打开");
        }
    };

})
.controller('taxController', function($scope){
    $scope.table_head=['统计截止日期', '税种', '纳税开始日期', '纳税金额', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
})
.controller('associatedOrgController', function($scope, $rootScope){
    $scope.customer_tab={};
    $scope.table_head=['关联公司名称', '与该客户关系', '登记机构', '登记人', '登记日期', '更新日期', '操作'];
    $scope.table_data=[];
})
.controller('prePersonController',function($scope,$http,$rootScope){
    $scope.pre={}

    var Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ];
    var ValideCode = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ];
    function IdCardValidate(idCard) {
         idCard = trim(idCard.replace(/ /g, ""));
         if (idCard.length == 15) {
             console.log(idCard.length)
             return isValidityBrithBy15IdCard(idCard);
         } else if (idCard.length == 18) {
             console.log(idCard.length)
             var a_idCard = idCard.split("");
             if(isValidityBrithBy18IdCard(idCard)&&isTrueValidateCodeBy18IdCard(a_idCard)){
                 //console.log("OK")
                 return true;
             }else {
                 alert('证件不合法')
                 return false;
             }
         } else {
             //console.log(idCard.length)
             alert("位数不足")
             return false;
         }
     }

    function isTrueValidateCodeBy18IdCard(a_idCard) {
         var sum = 0;
         if (a_idCard[17].toLowerCase() == 'x') {
             a_idCard[17] = 10;
         }
         for ( var i = 0; i < 17; i++) {
             sum += Wi[i] * a_idCard[i];
         }
         valCodePosition = sum % 11;
         if (a_idCard[17] == ValideCode[valCodePosition]) {
             return true;
         } else {
             return false;
         }
     }
     /**
     *  * 通过身份证判断是男是女
     *   * @param idCard 15/18位身份证号码
     *    * @return 'female'-女、'male'-男
     *     */
    function maleOrFemalByIdCard(idCard){
         idCard = trim(idCard.replace(/ /g, ""));
         if(idCard.length == 15){
             if(idCard.substring(14,15)%2==0){
                 return 'female';
             }else{
                 return 'male';
             }
         }else if(idCard.length == 18){
             if(idCard.substring(14,17)%2==0){
                 return 'female';
             }else{
                 return 'male';
             }
         }else{
             return null;
         }

     }

    /**
     *  * 验证18位数身份证号码中的生日是否是有效生日
     *   * @param idCard 18位书身份证字符串
     *    */
    function isValidityBrithBy18IdCard(idCard18){
         var year =  idCard18.substring(6,10);
         var month = idCard18.substring(10,12);
         var day = idCard18.substring(12,14);
         var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
         if(temp_date.getFullYear()!=parseFloat(year)
               ||temp_date.getMonth()!=parseFloat(month)-1
               ||temp_date.getDate()!=parseFloat(day)){
                 return false;
         }else{
             return true;
         }
     }

    function isValidityBrithBy15IdCard(idCard15){
          var year =  idCard15.substring(6,8);
          var month = idCard15.substring(8,10);
          var day = idCard15.substring(10,12);
          var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
          if(temp_date.getYear()!=parseFloat(year)
                   ||temp_date.getMonth()!=parseFloat(month)-1
                   ||temp_date.getDate()!=parseFloat(day)){
                     return false;
             }else{
                 return true;
             }
      }
    $scope.init = function(){
        $scope.pre.cert_type='身份证';
        $scope.pre.cert_no1=null;
        $scope.pre.cert_no2=null;
        $scope.pre.name = null;
    }
    $scope.init();
    $scope.cert_check1 = function(){
        if($scope.pre.cert_no1 == null)
            return;
        if(IdCardValidate($scope.pre.cert_no1.toString()) == false){
            $scope.pre.cert_no1 = null;
        }

    }
    $scope.submit = function(){
        $scope.pre.state='暂存';
        console.log($rootScope.user_session);

        if($scope.pre.name == null || $scope.pre.cert_no1==null){
            alert('请填写完信息')
        }else{
           if($scope.associate)
                $scope.pre.associate = $scope.associate;
           if($scope.party_id)
                $scope.pre.party_id = $scope.party_id;

           $scope.pre.branch_code=$rootScope.user_session.branch_code;

           $http.post(base_url+'/customers/person', $scope.pre).success(function(resp){

            var rt = resp.data
            console.log(rt)

            if(rt.success){
                alert('客户添加成功,客户代码:'+rt.success.cust_no,rt.success.cust_id)
                var cust_name = $scope.pre.name;
                var tabName = cust_name + '的客户信息';
                var htmlContent = 'views/customer/person/index.html';
                $rootScope.forward(tabName, htmlContent, {'customer': {id:rt.success.cust_id}});
            }else{
                alert('错误:'+rt.error)
            
            }
            console.log(resp);
            })
       }
                                                //IdCardValidate($scope.cert_no)
     }
            
    $scope.save = function(){

        if($scope.form.$valid){
            alert('通过验证可以提交表单');
        }else{
            alert('表单没有通过验证');
        }



        /*if($scope.pre.name == null || $scope.pre.cert_no1==null || $scope.pre.cert_no2 == null){
            alert('请填写完信息')
        }else{
           if($scope.associate)
                $scope.pre.associate = $scope.associate;
           if($scope.party_id)
                $scope.pre.party_id = $scope.party_id;
           $http.post(base_url+'/customers/person', $scope.pre).success(function(resp){
            var rt = resp.data
            console.log(rt)

            if(rt.success){
                alert('客户添加成功,客户编号:'+rt.success.cust_no)
            }else{
                alert('错误:'+rt.error)
            
            }
            //console.log(resp);
           })
            
        }*/
        //IdCardValidate($scope.cert_no)
    
    }
    $scope.clear = function(){
        $scope.init();
    }

})
.controller('personManageController', function($scope,$rootScope,customerService){
    $scope.customer_tab={};
    $scope.loan_tab={};
    
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = {'cust_name':null,'cust_no':null,'cert_type':'身份证','cert_no':null}; 
    $scope.custTableData = []
    var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'', };
    $scope.customerInfoDetail = function(cust){
        var cust_id = cust.id;
        var cust_name = cust.name;
        var cust_type = cust.type_code;
        var tabName = cust_name+'的客户信息';
        var htmlContent = '<div ng-include="'+'\'views/customer/person/index.html' +'\'" ></div>';       
        console.log(tabName);
        if($scope.customer_tab[cust_id] == undefined || $rootScope.tab[$scope.customer_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':cust});
            $scope.customer_tab[cust_id] = tab_id;
        }else{
            alert("用户信息标签已打开");
        }
    };
    // ------------- 加服务
    $scope.searchCustomer = function(){
        console.log('ook');
        customerService.query_persons($scope.cust_search.cust_no, $scope.cust_search.cust_name,$scope.cust_search.cert_type,$scope.cust_search.cert_no).success(function(resp){
            $scope.custTableData =  resp.data;
        });
    };
    $scope.newCustomer = function(){
        $rootScope.forward('新增个人客户','views/customer/person/pre_add.html');
    };
 
    $scope.loanApplication = function(cust){
        var cust_id = cust.id;
        var cust_name = cust.name;
        var apply_type='';
        apply_type='个人业务申请'
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/preCredit.html' +'\'"></div>';
        if($scope.loan_tab[cust_id] == undefined || $rootScope.tab[$scope.loan_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':cust,'apply_type':apply_type});
            $scope.loan_tab[cust_id] = tab_id;
        }else{
            alert("用户贷款标签已打开");
        }
    };
})

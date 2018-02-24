ysp.service('industryService',function($http){
    return {
        query:function(industry_d){
            return $http.get(base_url+'/common/industry/'+industry_d)
        },
        query_cust:function(party_id){
            return $http.get(base_url+'/common/industry/cust/'+party_id)
        },
    }
});


ysp.service('CustomerSearchService', function($http){
    return {
        query:function(custNo, custName, custType, certType, certNo){
            return $http.get(base_url+'/customers?customer_name='+custName);
        },
        /*组织机构判断查询*/
        queryroleparty:function(data){
            return $http.post(base_url+'/customers/roleparty/',data);
        },
        query_persons:function(custNo, custName, certType, certNo){
            return $http.get(base_url+'/customers/persons/?custNo='+custNo+'&custName='+custName+'&certType='+certType+'&certNo='+certNo);
        },
        query_companys:function(custNo, custName, certType, certNo){
            return $http.get(base_url+'/customers/companys/?custNo='+custNo+'&custName='+custName+'&certType='+certType+'&certNo='+certNo);
        },
    }
});
ysp.service('creditLevelService', function($http){
    return {
        query_level_person:function(cust_id){
            return $http.get(base_url+'/customers/level/person/'+cust_id);
        },
    
    }
})
ysp.service('guaranteeService', function($http){
    return {
        query:function(custNo, custName, custType, certType, certNo){
            return $http.get(base_url+'/customers?customer_name='+custName);
        }
    }
});
ysp.service('guaranteeInfoService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/guarantee_info/save/',data);
        },
        query_infos:function(application_id){
            return $http.get(base_url+'/guarantee_info/infos/'+application_id);
        },
        query:function(guarantee_info_id){
            return $http.get(base_url+'/guarantee_info/'+guarantee_info_id);
        },
        del:function(guarantee_info_id){
            return $http.put(base_url+'/guarantee_info/'+guarantee_info_id);
        },
        methods:function(){
            return $http.get(base_url+'/guarantee_info/methods');
        },
        InfoSave:function(data){/*抵质押合同 保存 */
             return $http.post(base_url+'/guarantee_info/InfoSave/',data);
        },
        InfoSaves:function(data){/*抵质押合同'完善'字段 保存 */
             return $http.post(base_url+'/guarantee_info/InfoSaves/',data);
        },
        query_allinfo:function(all_contract_no){/* 查询合同编号是否存在*/

            return $http.get(base_url+'/guarantee_info/all_contract_no/'+all_contract_no);
        },
        save_contract:function(data,contract_id){/*引用合同，并保存*/
            return $http.post(base_url+'/guarantee_info/save_contract/'+contract_id,data);
        },
        query_party:function(customer_name){/* 查询借款人类型，并保存*/
            return $http.get(base_url+'/guarantee_info/query_party/'+customer_name);
         },


    }
});
ysp.service('approvalService', function($http){
    return {
        query:function(application_id){
            return $http.get(base_url+'/approvals/'+application_id);
        },
        query_risk:function(application_id){
            return $http.get(base_url+'/approvals/risk/'+application_id);
        },
        save_risk:function(data){
            return $http.post(base_url+'/approvals/risk/',data);
        },
        update_risk:function(data){
            return $http.put(base_url+'/approvals/risk/',data);
        },
        query_examine:function(application_id){
            return $http.get(base_url+'/approvals/examine/'+application_id);
        },
        save_examine:function(data){
            return $http.post(base_url+'/approvals/examine/',data);
        },
        update_examine:function(data){
            return $http.put(base_url+'/approvals/examine/',data);
        },
        approve:function(application_id,data){
            return $http.post(base_url+'/approvals/'+application_id,data);
        },
        get_next:function(application_id){
            return $http.get(base_url+'/approvals/next/'+application_id);
        },
        bat_approve:function(data){
            return $http.post(base_url+'/approvals/',data);
        },        
        save_report:function(application_id){
            return $http.post(base_url+'/approvals/report/'+application_id);
        },
        save_risk_report:function(risk_id){
            return $http.post(base_url+'/approvals/report/risk/'+risk_id);
        },
        save_examine_report:function(examine_id){
            return $http.post(base_url+'/approvals/report/examine/'+examine_id);
        },
        approve_flag:function(application_id,data){
            return $http.post(base_url+'/approvals/approve_flag/'+application_id,data);
        },
    }
});

ysp.service('contractService', function($http){
    return {
        query:function(contract_no,gty_method){
            var a='';
            a=contract_no?a+'contract_no='+contract_no:a;
            a=gty_method?a+'&gty_method='+gty_method:a;
            console.log(a);
            return $http.get(base_url+'/contracts/?'+a);
        },
        query_lend:function(data){
            return $http.get(base_url+'/contracts/lend_contract/',data);
        },
        get:function(contract_id){
            return $http.get(base_url+'/contracts/'+contract_id);
        },
        save:function(data){
            return $http.post(base_url+'/contracts/submit/',data);
        },
        save_gty:function(data){
            return $http.post(base_url+'/contracts/save/',data);
        },
        list_update:function(data){
            return $http.put(base_url+'/contracts/list_update/',data);
        },
        list_query:function(tran_id){
            return $http.get(base_url+'/contracts/list_query/'+tran_id);
        },
        update_payment:function(debt_id,data){
            return $http.put(base_url+'/contracts/update_payment/'+debt_id,data);
        },
        query_payment:function(debt_id){
            return $http.get(base_url+'/contracts/query_payment/'+debt_id);
        },
        querycontract:function(application_id){
           return $http.post(base_url+'/contracts/querycontract/'+application_id);
        },

    }
});
ysp.service('userService',function($http){
    return {
        query_groups:function(){
            return $http.get(base_url+'/users/group/'+'11')
        },
    }
})
ysp.service('investReportService',function($http){
    return {
        get:function(application_id){
            return $http.get(base_url+'/report/'+application_id)
        },
        save:function(data){
            return $http.post(base_url+'/report/save',data)
        },
        submit:function(data){
            return $http.post(base_url+'/report/submit',data)
        },
    }
});
ysp.service('creditService', ['$http','ENDPOINT_URI', function ($http,ENDPOINT_URI) {
    return {
        query:function(application_status,cust_type, cust_name, guarantee_type, lend_type, ld_ratio, start_date, end_date){
            var cond = '';
            cond = application_status? cond+'application_status='+application_status:cond;
            cond = cust_type ? cond+'&cust_type='+cust_type:cond;
            cond = cust_name ? cond+'&cust_name='+cust_name:cond;
            cond = guarantee_type != undefined? cond+'&guarantee_type='+guarantee_type:cond;
            cond = lend_type != undefined? cond+'&lend_type='+lend_type:cond;
            cond = ld_ratio != undefined? cond+'&ld_ratio='+ld_ratio:cond;
            cond = start_date != undefined? cond+'&start_date='+start_date:cond;
            cond = end_date != undefined? cond+'&end_date='+end_date:cond;
            return $http.get(base_url+'/credit/list?'+cond);
        },
        samequery:function(opponent_name, amount,application_status){
            var conld = '';
            conld = opponent_name ? conld+'&opponent_name='+opponent_name:conld;
            conld = amount ? conld+'&amount='+amount:conld;
            conld = application_status? conld+'&status='+application_status:conld;
            return $http.get(base_url+'/credit/samequery/list?'+conld);
        },
        investquery:function(bus_type,pj_type,openning_bank,open_name,account,big_num){
            var conlud = '';
            conlud = bus_type ? conlud+'&bus_type='+bus_type:conlud;
            conlud = pj_type ? conlud+'&pj_type='+pj_type:conlud;
            conlud = openning_bank ? openning_bank+'&openning_bank='+openning_bank:conlud;
            conlud = open_name ? open_name+'&open_name='+open_name:conlud;
            conlud = account ? account+'&account='+account:conlud;
            conlud = big_num ? big_num+'&big_num='+big_num:conlud;
            return $http.get(base_url+'/credit/investquery/list?'+conlud);
        },
        detail:function(application_id){
            return $http.get(base_url+'/credit/'+application_id);
        },
        save:function(data){
            return $http.post(base_url+'/credit/save/',data);
        },
        save_discount:function(data){
            return $http.post(base_url+'/credit/discount/save',data);
        },
        submit:function(data){
            return $http.post(base_url+'/credit/submit/',data);
        },
        submit_discount:function(data){
            return $http.post(base_url+'/credit/discount/submit/',data);
        },
        saveInfo_discount:function(data){
            return $http.post(base_url+'/credit/discount/saveInfo/',data);
        },
        get:function(application_id){
            return $http.get(base_url+'/credit/query/'+application_id);
        },
        update:function(data){
            return $http.put(base_url+'/credit/update/',data);
        },
        testList:function(){
            return $http.post(base_url+'/users/auth');
        },
        testObj:function(){
            return $http.post(base_url+'/users/checkjson');
        },
        testMerge:function(){
            return $http.post(base_url+'/users/merge');
        },
        products:function(product_type){
            return $http.get(base_url+'/credit/products/'+product_type);
        },
        //同业
        same_bus_submit:function(data){
            return $http.post(base_url+'/credit/same_bus_submit/',data); 
        },
        same_bus_con:function(data){
            return $http.post(base_url+'/credit/same_bus_con/',data);
        },
        unite_credit_create:function(data){
            return $http.get(base_url+'/credit/unite_credit/create'); 
        },
        unite_credit_query:function(id){
            return $http.get(base_url+'/credit/unite_credit/query/'+id); 
        },
        unite_credit_queryList:function(data){
            return $http.post(base_url+'/credit/unite_credit/query/',data); 
        },
        unite_credit_update:function(data){
            return $http.put(base_url+'/credit/unite_credit/update/',data); 
        },
        invest_submit:function(data){
            return $http.post(base_url+'/credit/invest_submit/',data);
        },
        saveapprove:function(data){
             return $http.post(base_url+'/credit/saveapprove/',data);
        },
        querystatus:function(data){
            console.log(data);
             return $http.post(base_url+'/credit/querystatus/',data);
        }
   }
}]);
ysp.service('UniteService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        unite_credit_create:function(data){
            return $http.get(base_url+'/unite_credit/create'); 
        },
        unite_credit_query:function(uni_id){
            return $http.get(base_url+'/unite_credit/query/'+uni_id); 
        },
        unite_credit_queryList:function(data){
            return $http.post(base_url+'/unite_credit/query/',data); 
        },
        unite_credit_update:function(data){
            return $http.put(base_url+'/unite_credit/update/',data); 
        },
        invest_submit:function(data){
            return $http.post(base_url+'/invest_submit/',data);
        },
        inflow:function(uni_id){
            return $http.get(base_url+'/unite_credit/inflow/'+uni_id); 
        },
        query_by_app:function(app_id){
            return $http.get(base_url+'/unite_credit/query_by_app/'+app_id); 
        },
   }
}]);

ysp.service('loanService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        save:function(data){
            return $http.post(base_url+'/loan/save',data);
        },
        save_acceptanceBill:function(data){
            return $http.post(base_url+'/loan/acceptanceBill/save',data);
        },
        query:function(id){
            return $http.get(base_url+'/loan/query/'+id);
        },
        query_acceptanceBill:function(id){
            return $http.get(base_url+'/loan/acceptanceBill/query/'+id);
        },
        loan:function(data){
            return $http.post(base_url+'/loan/loan/',data);
        },
        loan_print:function(data){
            return $http.post(base_url+'/loan/loan_print/',data);
        },
        query_lend:function(application_id){
            return $http.get(base_url+'/loan/lend_transaction/'+application_id);
        }, 
        submit:function(data){
            return $http.post(base_url+'/loan/submit', data);
        },
        update:function(data){
            return $http.post(base_url+'/loan/update', data);
        },
        update_acceptanceBill:function(data){
            return $http.post(base_url+'/loan/acceptanceBill/update', data);
        },
        query_list:function(transactionId,custName,custType,loanType,contractNo,gtyType){
            var cond = '';
            cond = transactionId ? 'transaction_id='+transactionId:cond;
            return $http.get(base_url+'/loan/lend_transaction?'+cond);
        },
    }
}]);
ysp.service('imageService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        query:function(applicationId, about){
            return $http.get(base_url+'/img/'+applicationId+'?about='+about);
        },
        img_delete:function(data){
            return $http.post(base_url+'/img/img_delete/',data);
        },
        img_print:function(data){
            return $http.post(base_url+'/img/img_print/',data);
        },
        query_cust:function(party_id, about){
            return $http.get(base_url+'/img/customer/'+party_id+'?about='+about);
        },
        bill_query:function(bill_no){
            return $http.get(base_url+'/img/bill/query/'+bill_no);
        },
        img_check:function(data){
            return $http.post(base_url+'/img/bill/img_check/',data);
        },
        pdfile_query:function(applicationId, about){
            return $http.get(base_url+'/img/pdfile_query/'+applicationId+'?about='+about);
        },
        pdf_delete:function(data){
            return $http.post(base_url+'/img/pdf_delete/',data);
        },
        discount_print:function(data){
            return $http.post(base_url+'/img/discount_print/',data);
        },
    }
}]);
ysp.service('pendApproveService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        query:function(applicationId){
            return $http.get(base_url+'/approve/application_id/'+applicationId);
        },
    }
}]);
ysp.service('commonService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return {
        create_person_level:function(cust_id,data){
            return $http.post(base_url+'/common/cust_level/person/create/'+cust_id,data);
        },

    }

}]);
ysp.service('MortgageService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        MrgeEqpMovableSave:function(data){/*抵押-设备+动产 保存 */
            return $http.post(base_url+'/pledge/MrgeEqpMovableSave/',data);
        },
        MrgeBuildingSave:function(data){/*抵押-房屋所有权 保存 */
            return $http.post(base_url+'/pledge/MrgeBuildingSave/',data);
        },
        MrgeEqpSave:function(data){/*抵押-设备 保存 */
            return $http.post(base_url+'/pledge/MrgeEqpSave/',data);
        },
        MrgeLandSave:function(data){/*抵押-土地 保存 */
            return $http.post(base_url+'/pledge/MrgeLandSave/',data);
        },
        MrgeOtherSave:function(data){/*抵押-其他 保存 */
            return $http.post(base_url+'/pledge/MrgeOtherSave/',data);
        },
        MrgeVchSave:function(data){/*抵押-车辆 保存 */
            return $http.post(base_url+'/pledge/MrgeVchSave/',data);
        },
        MrgeMovableSave:function(data){/*抵押-动产 保存 */
            return $http.post(base_url+'/pledge/MrgeMovableSave/',data);
        },
        MrgeBuildingUpdate:function(data){/*抵押-房屋所有权 修改*/
            return $http.post(base_url+'/pledge/MrgeBuildingUpdate?gty_id='+data.gty_id,data);
        },
        MrgeLandUpdate:function(data){/*抵押-土地 修改*/
            return $http.post(base_url+'/pledge/MrgeLandUpdate?gty_id='+data.gty_id,data);
        },
        MrgeVchUpdate:function(data){/*抵押-车辆 修改*/
            return $http.post(base_url+'/pledge/MrgeVchUpdate?gty_id='+data.gty_id,data);
        },
        MrgeEqpUpdate:function(data){/*抵押-设备 修改*/
            return $http.post(base_url+'/pledge/MrgeEqpUpdate?gty_id='+data.gty_id,data);
        },
        MrgeOtherUpdate:function(data){/*抵押-其他 修改*/
            return $http.post(base_url+'/pledge/MrgeOtherUpdate?gty_id='+data.gty_id,data);
        },
    }
}]);
ysp.service('PledgeService',['$http','ENDPOINT_URI',function($http,ENDPOINT_URI){
    return{
        othersave:function(data){/*质押-其他 保存 */
            return $http.post(base_url+'/pledge/othersave/',data);
        },
        update:function(data){/*质押-其他 修改*/
            return $http.post(base_url+'/pledge/otherupdate?gty_id='+data.gty_id,data);
        },
        otherquery:function(gty_id,pledge_type,gty_cus_name){/*查询所有*/
             var conld ='';
             conld = pledge_type ? conld+'pledge_type='+pledge_type:conld;
             conld = gty_id ? conld+'&gty_id='+gty_id:conld;
             conld = gty_cus_name ? conld+'&gty_cus_name='+gty_cus_name:conld;             
             return $http.get(base_url+'/pledge/query/?'+conld);
        },
/*    删除    deleteGTY:function(id){
             return $http.get(base_url+'/pledge/deleteGTY?gty_id='+id);
        },*/
        detailsGTY:function(){
        },
          perstubsave:function(data){/*质押-单位定期存单 保存 */
              return $http.post(base_url+'/pledge/perstubsave/',data);
          },
          perstubupdate:function(data){/*质押-单位定期存单 修改*/
              return $http.post(base_url+'/pledge/perstubupdate?gty_id='+data.gty_id,data);
         },
         stubsave:function(data){/*质押-单位定期存单 保存 */
             return $http.post(base_url+'/pledge/stubsave/',data);
         },
         stubupdate:function(data){/*质押-单位定期存单 修改*/
             return $http.post(base_url+'/pledge/stubupdate?gty_id='+data.gty_id,data);
        },

         savingsave:function(data){/*质押-账户资金 保存 */
             return $http.post(base_url+'/pledge/savingsave/',data);
         },
         savingupdate:function(data){/*质押-账户资金 修改*/
             return $http.post(base_url+'/pledge/savingupdate?gty_id='+data.gty_id,data);
        },

         vch_qlfsave:function(data){/*质押-本行理财产品 保存 */
             return $http.post(base_url+'/pledge/vch_qlfsave/',data);
         },
         vch_qlfupdate:function(data){/*质押-本行理财产品 修改*/
             return $http.post(base_url+'/pledge/vch_qlfupdate?gty_id='+data.gty_id,data);
        },

         acc_recsave:function(data){/*质押-银行承兑汇票 保存 */
             return $http.post(base_url+'/pledge/acc_recsave/',data);
         },
         acc_recupdate:function(data){/*质押-银行承兑汇票 修改*/
             return $http.post(base_url+'/pledge/acc_recupdate?gty_id='+data.gty_id,data);
        },

         accpsave:function(data){/*质押-应收账款 保存 */
             return $http.post(base_url+'/pledge/accpsave/',data);
         },
         accpupdate:function(data){/*质押-应收账款 修改*/
             return $http.post(base_url+'/pledge/accpupdate?gty_id='+data.gty_id,data);
         },
        PaperContract:function(data){/*质押-应收账款 修改*/
             return $http.post(base_url+'/pledge/PaperContract/',data);
         },
    } 
}]);

ysp.service('BillService', function($http){
    return {
        query:function(application_id,data){
            return $http.post(base_url+'/bill/query/'+application_id, data);
        },   
        update:function(bill_id,data){
            return $http.put(base_url+'/bill/update/'+bill_id, data);
        },
        create:function(application_id,data){
            return $http.post(base_url+'/bill/create/'+application_id, data);
        },
        query_info:function(application_id){
            return $http.get(base_url+'/bill/query_info/'+application_id);
        },
        del:function(bill_id){
            return $http.put(base_url+'/bill/delete/'+bill_id);
        }, 
        check_bill:function(application_id,data){
            return $http.post(base_url+'/bill/check/'+application_id, data)
        },  
        check_bill_query:function(application_id){
            return $http.get(base_url+'/bill/check_query/'+application_id)
        },
        query_dis_name:function(account_no){
            return $http.get(base_url+'/bill/query_dis_name/'+account_no)
        },
    }           
});

ysp.service('batchService',function($http){

    return {
        batch_begin:function(){
            return $http.get(base_url+'/common/batch/')
        },
    }

});

ysp.service('RepossessionService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/repossession/save/',data);
        },
        query:function(cateType,cateId,cusId,gtyMainMethod,appStatus,transactionId,issueDate,dueDate){
            var cond = '';
            cond = cond+'cate_id='+cateId;
            cond = cateType ? cond+'&cate_type='+cateType:cond;
            cond = transactionId ? cond+'&transaction_id='+transactionId:cond;
            cond = cusId ? cond+'&cus_id='+cusId:cond;
            cond = gtyMainMethod ? cond+'&gty_main_method='+gtyMainMethod:cond;
            cond = appStatus ? cond+'&app_status='+appStatus:cond;
            cond = issueDate ? cond+'&issue_date='+issueDate:cond;
            cond = dueDate ? cond+'&due_date='+dueDate:cond;
            return $http.get(base_url+'/repossession/query?'+cond);
        },
        submit:function(data){
            return $http.put(base_url+'/repossession/submit/',data);
        },
        save_submit:function(data){
            return $http.post(base_url+'/repossession/submit/',data);
        },
        update:function(data){
            return $http.post(base_url+'/repossession/update/',data);
        },
        query_by_id:function(application_id){
            return $http.get(base_url+'/repossession/query/'+application_id);
        },
    }
});
ysp.service('ExtensionService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/extension/save/',data);
        },
        update:function(data){
            return $http.post(base_url+'/extension/update/',data);
        },
        query:function(cateType,cateId,cusId,gtyMainMethod,appStatus,transactionId,issueDate,dueDate){
            var cond = '';
            cond = cond+'cate_id='+cateId;
            cond = cateType ? cond+'&cate_type='+cateType:cond;
            cond = transactionId ? cond+'&transaction_id='+transactionId:cond;
            cond = cusId ? cond+'&cus_id='+cusId:cond;
            cond = gtyMainMethod ? cond+'&gty_main_method='+gtyMainMethod:cond;
            cond = appStatus ? cond+'&app_status='+appStatus:cond;
            cond = issueDate ? cond+'&issue_date='+issueDate:cond;
            cond = dueDate ? cond+'&due_date='+dueDate:cond;
            return $http.get(base_url+'/extension/query?'+cond);
        },
        submit:function(data){
            return $http.put(base_url+'/extension/submit/',data);
        },
        save_submit:function(data){
            return $http.post(base_url+'/extension/submit/',data);
        },
        query_by_id:function(application_id){
            return $http.get(base_url+'/extension/query/'+application_id);
        },
    }
});

ysp.service('AdjustmentService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/adjustment/save/',data);
        },
        update:function(data){
            return $http.post(base_url+'/adjustment/update/',data);
        },
        query:function(cateType,cateId,cusId,gtyMainMethod,appStatus,transactionId,issueDate,dueDate){
            var cond = '';
            cond = cond+'cate_id='+cateId;
            cond = cateType ? cond+'&cate_type='+cateType:cond;
            cond = transactionId ? cond+'&transaction_id='+transactionId:cond;
            cond = cusId ? cond+'&cus_id='+cusId:cond;
            cond = gtyMainMethod ? cond+'&gty_main_method='+gtyMainMethod:cond;
            cond = appStatus ? cond+'&app_status='+appStatus:cond;
            cond = issueDate ? cond+'&issue_date='+issueDate:cond;
            cond = dueDate ? cond+'&due_date='+dueDate:cond;
            return $http.get(base_url+'/adjustment/query?'+cond);
        },
        submit:function(data){
            return $http.put(base_url+'/adjustment/submit/',data);
        },
        save_submit:function(data){
            return $http.post(base_url+'/adjustment/submit/',data);
        },
        query_by_id:function(application_id){
            return $http.get(base_url+'/adjustment/query/'+application_id);
        },
    }
});
ysp.service('AuditsaleService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/auditsale/save/',data);
        },
        update:function(data){
            return $http.post(base_url+'/auditsale/update/',data);
        },
        query:function(cateType,cateId,cusId,gtyMainMethod,appStatus,transactionId,issueDate,dueDate){
            var cond = '';
            cond = cond+'cate_id='+cateId;
            cond = cateType ? cond+'&cate_type='+cateType:cond;
            cond = transactionId ? cond+'&transaction_id='+transactionId:cond;
            cond = cusId ? cond+'&cus_id='+cusId:cond;
            cond = gtyMainMethod ? cond+'&gty_main_method='+gtyMainMethod:cond;
            cond = appStatus ? cond+'&app_status='+appStatus:cond;
            cond = issueDate ? cond+'&issue_date='+issueDate:cond;
            cond = dueDate ? cond+'&due_date='+dueDate:cond;
            return $http.get(base_url+'/auditsale/query?'+cond);
        },
        submit:function(data){
            return $http.put(base_url+'/auditsale/submit/',data);
        },
        save_submit:function(data){
            return $http.post(base_url+'/auditsale/submit/',data);
        },
        query_by_id:function(application_id){
            return $http.get(base_url+'/auditsale/query/'+application_id);
        },
    }
});
ysp.service('FiveCategoryService', function($http){
    return {
        save:function(data){
            return $http.post(base_url+'/five_category/save/',data);
        },
        query:function(cateType,cateId,cusId,gtyMainMethod,appStatus,transactionId,issueDate,dueDate){
            var cond = '';
            cond = cond+'cate_id='+cateId;
            cond = cateType ? cond+'&cate_type='+cateType:cond;
            cond = transactionId ? cond+'&transaction_id='+transactionId:cond;
            cond = cusId ? cond+'&cus_id='+cusId:cond;
            cond = gtyMainMethod ? cond+'&gty_main_method='+gtyMainMethod:cond;
            cond = appStatus ? cond+'&app_status='+appStatus:cond;
            cond = issueDate ? cond+'&issue_date='+issueDate:cond;
            cond = dueDate ? cond+'&due_date='+dueDate:cond;
            return $http.get(base_url+'/five_category/query?'+cond);
        },
        submit:function(data){
            return $http.put(base_url+'/five_category/submit/',data);
        },
        save_submit:function(data){
            return $http.post(base_url+'/five_category/submit/',data);
        },
        update:function(id,data){
            return $http.put(base_url+'/five_category/update/'+id,data);
        },
        query_by_id:function(application_id){
            return $http.get(base_url+'/five_category/query/'+application_id);
        },
        deleteById:function(id){
            return $http.get(base_url+'/five_category/deleteById?app_id='+id);
        },
        denyById:function(id){
            return $http.get(base_url+'/five_category/denyById?app_id='+id);
        },
    }
});
ysp.service('standBookService', function($http){
    return {
        query_list:function(){
            return $http.get(base_url+'/standing_book/query_list/');
        },
        query_repossession:function(){
            return $http.get(base_url+'/standing_book/query_repossession/');
        },
        query_debt:function(){
            return $http.get(base_url+'/standing_book/debt/query/');
        },
        save:function(data){
            return $http.post(base_url+'/standing_book/save/',data);
        },
        save_repossession:function(data){
            return $http.post(base_url+'/standing_book/repossession/save/',data);
        },
        query:function(litigation_book_id){
            return $http.get(base_url+'/standing_book/query/'+litigation_book_id);
        },
        update:function(data){
            return $http.post(base_url+'/standing_book/update/',data);
        },
        update_repossession:function(data){
            return $http.post(base_url+'/standing_book/update_repossession/',data);
        },
        export_book:function(data){
            return $http.post(base_url+'/standing_book/export/',data);
        },
        export_repossession_book:function(data){
            return $http.post(base_url+'/standing_book/export_repossession/',data);
        },
     }
});




/**
 * 客户信息服务
 */

function customerService($http){
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
    };
};

customerService.$inject = ['$http'];

angular.module('YSP').service('customerService', customerService);
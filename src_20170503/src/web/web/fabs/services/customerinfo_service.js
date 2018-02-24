/**
 * Customer Info Service
 */
ysp.service('customerInfoService', customerInfoService);
customerInfoService.$inject = ['$http'];

function customerInfoService($http) {
    return {
        info: function () {
            return $http.get("http://192.168.100.48:8990/report_proxy/cognos/NX01_%E5%AE%A2%E6%88%B7%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF%E6%8A%A5%E8%A1%A8?p_P_DATE=20130904&p_P_SALEID=8080000");
        },
        action: function(conversation_id,action) {
            return $http.get("http://192.168.100.48:8990/report_proxy/cognos/"+conversation_id+"/"+action);
        }
    };
};


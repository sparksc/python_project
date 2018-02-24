/**
 *account_rank Service
*/
ysp.service('international_levelService', international_levelService);
international_levelService.$inject = ['$http'];

function  international_levelService($http) {
    return {
        conunt_del: function(data){
            return $http.post(base_url + '/international_level/conunt_del',data);
        },
        calculate:function(data){
            return $http.post(base_url+'/international_level/calculate',data);
        },
        change_save:function(data){
            return $http.post(base_url+'/international_level/change_save',data);
        },
        affirm:function(data){
            return $http.post(base_url+'/international_level/affirm',data);
        }
    };
};


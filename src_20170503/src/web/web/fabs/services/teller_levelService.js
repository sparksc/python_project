/**
 *account_rank Service
*/
ysp.service('teller_levelService', teller_levelService);
teller_levelService.$inject = ['$http'];

function  teller_levelService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/teller_level/add_save', data);
        },
        change_save: function (data){
            return $http.post(base_url + '/teller_level/change_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/teller_level/delete',data);
        },
        calculate:function(data){
            return $http.post(base_url+'/teller_level/calculate',data);
        },
        affirm:function(data){
            return $http.post(base_url+'/teller_level/affirm',data);
        }
    };
};


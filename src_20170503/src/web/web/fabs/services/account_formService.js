/**
 *account_form Service
*/
ysp.service('account_formService', account_formService);
account_formService.$inject = ['$http'];

function  account_formService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/account_form/add_save', data);
        },
        change_save: function (data){
            return $http.post(base_url + '/account_form/change_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/account_form/delete',data);
        },
        calculate:function(data){
            return $http.post(base_url+'/account_form/calculate',data);
        },
        affirm:function(data){
            return $http.post(base_url+'/account_form/affirm',data);
        }

    };
};


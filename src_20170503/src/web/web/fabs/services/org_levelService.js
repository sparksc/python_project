/**
 *account_rank Service
*/
ysp.service('org_levelService', org_levelService);
org_levelService.$inject = ['$http'];

function  org_levelService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/org_level/add_save', data);
        },
        change_save: function (data){
            return $http.post(base_url + '/org_level/change_save' ,data);
        },
        count_save: function (data){
            return $http.post(base_url + '/org_level/count_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/org_level/delete',data);
        },
        conunt_del: function(data){
            return $http.post(base_url + '/org_level/conunt_del',data);
        },
        calculate:function(data){
            return $http.post(base_url+'/org_level/calculate',data);
        },
        count_edit_save:function(data){
            return $http.post(base_url+'/org_level/count_edit_save',data);
        },
        affirm:function(data){
            return $http.post(base_url+'/org_level/affirm',data);
        }
    };
};


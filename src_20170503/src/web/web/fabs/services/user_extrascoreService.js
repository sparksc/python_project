/**
 *user_extrascore Service
*/
ysp.service('user_extrascoreService', user_extrascoreService);
user_extrascoreService.$inject = ['$http'];

function user_extrascoreService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/user_extrascore/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/user_extrascore/edit_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/user_extrascore/delete',data);
        },
        credentials:function(data){
            return $http.post(base_url+'/user_extrascore/credentials',data);
        },
        calculate:function(data){
            return $http.post(base_url+'/user_extrascore/calculate',data);
        }
    };
};


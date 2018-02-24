/**
 *user_levelService
*/
ysp.service('user_levelService', user_levelService);
user_levelService.$inject = ['$http'];

function user_levelService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/user_level/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/user_level/edit_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/user_level/delete',data);
        },
        credentials:function(data){
            return $http.post(base_url+'/user_level/credentials',data);
        }
    };
};


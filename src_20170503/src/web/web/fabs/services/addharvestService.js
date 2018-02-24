/**
 * Service
*/
ysp.service('addharvestService',addharvestService);
addharvestService.$inject = ['$http'];

function addharvestService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/addharvest/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/addharvest/edit_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/addharvest/delete',data);
        }
    };
};


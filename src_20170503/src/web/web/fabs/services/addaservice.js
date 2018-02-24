/**
 * Permission Service
 */
ysp.service('addaService', addaService);
addaService.$inject = ['$http'];

function addaService($http) {
    return {
        type_save: function (data) {
            return $http.post(base_url + '/idda/idda_save', data);
        },
        type_delete:function(data){
            return $http.post(base_url + '/idda/type_delete',data)
        },
        type_update: function (data) {
            return $http.post(base_url + '/idda/type_update', data);
        }
    };
};


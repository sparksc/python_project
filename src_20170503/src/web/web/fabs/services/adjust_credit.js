/**
 * Permission Service
 */
ysp.service('adjusttypeService', adjusttypeService);
adjusttypeService.$inject = ['$http'];

function adjusttypeService($http) {
    return {
        type_save: function (data) {
            return $http.post(base_url + '/adjusttype/type_save', data);
        },
        type_delete:function(data){
            return $http.post(base_url + '/adjusttype/type_delete',data)
        },
        type_update: function (data) {
            return $http.post(base_url + '/adjusttype/type_update', data);
        }
   
    };
};


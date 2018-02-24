/**
 * Permission Service
 */
ysp.service('parameterService', parameterService);
parameterService.$inject = ['$http'];

function parameterService($http) {
    return {
        
        parameters: function (data) {
            return $http.post(base_url + '/parameterpermission/parameters', data);
        },
        parameter_save:function(data){
            return $http.post(base_url + '/parameterpermission/parameter_save',data);
        },
        parameter_delete:function(data){
            return $http.post(base_url + '/parameterpermission/parameter_delete',data);
        },
        parameter_edit_save:function(data){
            return $http.post(base_url + '/parameterpermission/parameter_edit_save',data);
        }

    };
};


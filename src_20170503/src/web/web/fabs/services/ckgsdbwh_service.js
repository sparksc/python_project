/**
 * Permission Service
 */
ysp.service('ckgsdbwhService', ckgsdbwhService);
ckgsdbwhService.$inject = ['$http'];

function ckgsdbwhService($http) {
    return {
        
        add_save: function (data) {
            return $http.post(base_url + '/dkgsgxxzpermission/add_save', data);
        }

    };
};


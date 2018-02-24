/**
 * Permission Service
 */
ysp.service('dkgsgxxzService', dkgsgxxzService);
dkgsgxxzService.$inject = ['$http'];

function dkgsgxxzService($http) {
    return {
        
        add_save: function (data) {
            return $http.post(base_url + '/dkgsgxxzpermission/add_save', data);
        },
        do_batch_move: function(data){
            return $http.post(base_url + '/dkgsgxxzpermission/do_batch_move', data);
        }
    };
};


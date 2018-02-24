/**
 * Permission Service
 */
ysp.service('cdgggxService', cdgggxService);
cdgggxService.$inject = ['$http'];

function cdgggxService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/cdgggx/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/cdgggx/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/cdgggx/update', data);
        },       
        delete: function (data) {
            return $http.post(base_url + '/cdgggx/delete', data);
        },
        batch_pass: function (data) {
            return $http.post(base_url + '/cdgggx/batch_pass', data);
        },
        batch_refuse: function (data) {
            return $http.post(base_url + '/cdgggx/batch_refuse', data);
        },
        move: function (data) {
            return $http.post(base_url + '/cdgggx/move', data);
        }
    };
};


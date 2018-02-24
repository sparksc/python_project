/**
 * Permission Service
 */
ysp.service('gsgxdkService', gsgxdkService);
gsgxdkService.$inject = ['$http'];

function gsgxdkService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/gsgxdk/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/gsgxdk/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/gsgxdk/update', data);
        },
        batch_move: function (data) {
            return $http.post(base_url + '/gsgxdk/batch_move', data);
        },
        move: function (data) {
            return $http.post(base_url + '/gsgxdk/move', data);
        }
    };
};


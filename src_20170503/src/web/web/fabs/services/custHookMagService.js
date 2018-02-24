/**
 * Permission Service
 */
ysp.service('custHookMagService', custHookMagService);
custHookMagService.$inject = ['$http'];

function custHookMagService($http) {
    return {
        batch_cust_move: function (data) {
            return $http.post(base_url + '/custHookMag/batch_cust_move', data);
        },
        batch_cust_move_before: function (data) {
            return $http.post(base_url + '/custHookMag/batch_cust_move_before', data);
        },
        batch_cust_move_delete: function (data) {
            return $http.post(base_url + '/custHookMag/batch_cust_move_delete', data);
        },
        distribute: function (data) {
            return $http.post(base_url + '/custHookMag/distribute', data);
        },
        cust_move: function (data) {
            return $http.post(base_url + '/custHookMag/cust_move', data);
        },
        single_move: function (data) {
            return $http.post(base_url + '/custHookMag/single_move', data);
        },
        single_move_cust: function (data) {
            return $http.post(base_url + '/custHookMag/single_move_cust', data);
        },
        single_approve: function (data) {
            return $http.post(base_url + '/custHookMag/single_approve', data);
        },
        get_top: function (data) {
            return $http.post(base_url + '/custHookMag/get_top', data);
        }
    };
};


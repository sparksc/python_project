/**
 * Permission Service
 */
ysp.service('tparaService', tparaService);
tparaService.$inject = ['$http'];

function tparaService($http) {
    return {
        type_save: function (data) {
            return $http.post(base_url + '/tpara/type_save', data);
        },
        type_update: function (data) {
            return $http.post(base_url + '/tpara/type_update', data);
        },
        header_save: function (data) {
            return $http.post(base_url + '/tpara/header_save', data);
        },
        header_update: function (data) {
            return $http.post(base_url + '/tpara/header_update', data);
        },
        para_save: function (data) {
            return $http.post(base_url + '/tpara/para_save', data);
        },
        row_update: function (data) {
            return $http.post(base_url + '/tpara/row_update', data);
        },
        detail_update: function (data) {
            return $http.post(base_url + '/tpara/detail_update', data);
        }
    };
};


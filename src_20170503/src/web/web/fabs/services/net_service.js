/**
 * Net Service
 */
ysp.service('netService', netService);
netService.$inject = ['$http'];

function netService($http) {
    return {
        nets: function () {
            return $http.post(base_url + '/net/nets');
        },
        net_add_save: function (data) {
            return $http.post(base_url + '/net/net_add_save', data);
        },
        net_edit_save: function (data) {
            return $http.post(base_url + '/net/net_edit_save', data);
        },
        net_del: function (data) {
            return $http.post(base_url + '/net/net_del', data);
        }
    };
};


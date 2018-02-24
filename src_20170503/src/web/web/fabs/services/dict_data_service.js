/**
 * Permission Service
 */
ysp.service('dictdataService', dictdataService);
dictdataService.$inject = ['$http'];

function dictdataService($http) {
    return {
        save: function (data) {
            return $http.post(base_url + '/dictdata/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/dictdata/update', data);
        },
        simple_select: function (data) {
            return $http.post(base_url + '/dictdata/simple_select', data);
        },
        get_dict: function (data) {
            return $http.post(base_url + '/dictdata/get_dict', data);
        },
        get_dicts: function (data) {
            return $http.post(base_url + '/dictdata/get_dicts', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/dictdata/delete', data);
        }
    };
};


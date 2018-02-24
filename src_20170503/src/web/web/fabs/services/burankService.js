/**
 * burank Service
 */
ysp.service('burankService', burankService);
burankService.$inject = ['$http'];

function burankService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/burank/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/burank/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/burank/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/burank/update', data);
        }
    };
};


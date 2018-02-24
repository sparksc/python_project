/**
 * Performance Service
 */
ysp.service('perConService', perConService);
perConService.$inject = ['$http'];
function perConService($http) {
     return {
        load: function () {
            return $http.post(base_url + '/performance/load');
        },
        add: function (data) {
            return $http.post(base_url + '/performance/add',data);
        },
        targets: function (data) {
            return $http.post(base_url + '/performance/targets',data);
        },
        set_load: function (data) {
            return $http.post(base_url + '/performance/find',data);
        },
        objects: function () {
            return $http.post(base_url + '/performance/objects');
        },
        persons: function (data) {
            return $http.post(base_url + '/performance/persons',data);
        },
        add_save: function (data) {
            return $http.post(base_url + '/performance/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/performance/save', data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/performance/edit_save', data);
        },
        del: function (data) {
            return $http.post(base_url + '/performance/del', data);
        }
       
    };
};


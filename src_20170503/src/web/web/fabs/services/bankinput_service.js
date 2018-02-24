/**
 * BankInput Service
 */
ysp.service('bankInputService', bankInputService);
handInputService.$inject = ['$http'];
function bankInputService($http) {
     return {
        load: function () {
            return $http.post(base_url + '/bankinput/load');
        },
        e_load: function () {
            return $http.post(base_url + '/bankinput/e_load');
        },
        branches: function () {
            return $http.post(base_url + '/bankinput/branches');
        },
        add_save: function (data) {
            return $http.post(base_url + '/bankinput/add_save',data);
        },
        e_add_save: function (data) {
            return $http.post(base_url + '/bankinput/e_add_save',data);
        },
        persons: function (data) {
            return $http.post(base_url + '/bankinput/persons',data);
        },
        branch_order: function (data) {
            return $http.post(base_url + '/bankinput/branch_order',data);
        },
        person_order: function (data) {
            return $http.post(base_url + '/bankinput/person_order',data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/bankinput/edit_save',data);
        },
        e_edit_save: function (data) {
            return $http.post(base_url + '/bankinput/e_edit_save',data);
        },
        del: function (data) {
            return $http.post(base_url + '/bankinput/delete',data);
        }
    };
};


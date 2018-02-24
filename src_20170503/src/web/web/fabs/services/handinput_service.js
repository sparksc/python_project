/**
 * HandInput Service
 */
ysp.service('handInputService', handInputService);
handInputService.$inject = ['$http'];
function handInputService($http) {
     return {
        load: function () {
            return $http.post(base_url + '/handinput/load');
        },
        branches: function () {
            return $http.post(base_url + '/handinput/branches');
        },
        add_save: function (data) {
            return $http.post(base_url + '/handinput/add_save',data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/handinput/edit_save',data);
        },
        del: function (data) {
            return $http.post(base_url + '/handinput/delete',data);
        },
        loan_load: function () {
            return $http.post(base_url + '/handinput/loan_load');
        },
        loan_add_save: function (data) {
            return $http.post(base_url + '/handinput/loan_add_save',data);
        },
        loan_edit_save: function (data) {
            return $http.post(base_url + '/handinput/loan_edit_save',data);
        }
    };
};


/**
 * Permission Service
 */
ysp.service('custhkService', custhkService);
custhkService.$inject = ['$http'];

function custhkService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/custhk/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/custhk/save', data);
        },
        ssave: function (data) {
            return $http.post(base_url + '/custhk/ssave', data);
        },
        hk_acct: function (data) {
            return $http.post(base_url + '/custhk/hk_acct', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/custhk/delete', data);
        },
        sdelete: function (data) {
            return $http.post(base_url + '/custhk/sdelete', data);
        },
        ebk_delete: function (data) {
            return $http.post(base_url + '/custhk/ebk_delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/custhk/update', data);
        },
        ebk_update: function (data) {
            return $http.post(base_url + '/custhk/ebk_update', data);
        },
        supdate: function (data) {
            return $http.post(base_url + '/custhk/supdate', data);
        },
        batch_move: function (data) {
            return $http.post(base_url + '/custhk/batch_move', data);
        },
        get_staff_name: function (data) {
            return $http.post(base_url + '/custhk/get_staff_name', data);
        },
        get_manlist: function (data) {
            return $http.post(base_url + '/custhk/get_manlist', data);
        },
        change_main: function (data) {
            return $http.post(base_url + '/custhk/change_main', data);
        },
        account_move: function (data) {
            return $http.post(base_url + '/custhk/account_move', data);
        },
        approve: function (data) {
            return $http.post(base_url + '/custhk/approve', data);
        },
        check_manager: function (data) {
            return $http.post(base_url + '/custhk/check_manager', data);
        },
        ssave_with_cust_hook: function (data) {
            return $http.post(base_url + '/custhk/ssave_with_cust_hook', data);
        },
        deny: function (data) {
            return $http.post(base_url + '/custhk/deny', data);
        }
    };
};


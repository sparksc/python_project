/**
 * Permission Service
 */
ysp.service('gsgxckService', gsgxckService);
gsgxckService.$inject = ['$http'];

function gsgxckService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/gsgxck/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/gsgxck/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/gsgxck/update', data);
        },
        batch_account_move_before: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_before', data);
        },
        batch_account_move_before_all: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_before_all', data);
        },
        batch_account_move_delete: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_delete', data);
        },
        batch_account_move_all_delete: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_all_delete', data);
        },
        batch_account_move: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move', data);
        },
        batch_account_move_all: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_all', data);
        },
        batch_account_move_check: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_check', data);
        },
        batch_account_move_sum: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_sum', data);
        },
        batch_account_move_sum_with_hook: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_sum_with_hook', data);
        },
        batch_account_move_sum_with_hook_all: function (data) {
            return $http.post(base_url + '/gsgxck/batch_account_move_sum_with_hook_all', data);
        },
        batch_cust_move: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move', data);
        },
        batch_cust_move_before: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_before', data);
        },
        batch_cust_move_before_all: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_before_all', data);
        },
        batch_cust_move_delete: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_delete', data);
        },
        batch_cust_move_before_all_delete: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_before_all_delete', data);
        },
        batch_cust_move: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move', data);
        },
        batch_cust_move_all: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_all', data);
        },
        batch_cust_move_check: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_check', data);
        },
        staff_all_hook_batch_move: function (data) {
            return $http.post(base_url + '/gsgxck/staff_all_hook_batch_move', data);
        },
        staff_all_hook_batch_move_cancel: function (data) {
            return $http.post(base_url + '/gsgxck/staff_all_hook_batch_move_cancel', data);
        },
        batch_cust_move_sum: function (data) {
            return $http.post(base_url + '/gsgxck/batch_cust_move_sum', data);
        },
        get_top: function (data) {
            return $http.post(base_url + '/gsgxck/get_top', data);
        },
        get_top_cust: function (data) {
            return $http.post(base_url + '/gsgxck/get_top_cust', data);
        },
        account_move: function (data) {
            return $http.post(base_url + '/gsgxck/account_move', data);
        },
    };
};


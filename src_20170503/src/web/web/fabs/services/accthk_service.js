/**
 * Permission Service
 */
ysp.service('accthkService', accthkService);
accthkService.$inject = ['$http'];

function accthkService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/accthk/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/accthk/save', data);
        },
        ssave: function (data) {
            return $http.post(base_url + '/accthk/ssave', data);
        },
        sssave: function (data) {
            return $http.post(base_url + '/accthk/sssave', data);
        },
        parent_save: function (data) {
            return $http.post(base_url + '/accthk/parent_save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/accthk/delete', data);
        },
        sdelete: function (data) {
            return $http.post(base_url + '/accthk/sdelete', data);
        },
        parent_delete: function (data) {
            return $http.post(base_url + '/accthk/parent_delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/accthk/update', data);
        },
        supdate: function (data) {
            return $http.post(base_url + '/accthk/supdate', data);
        },
        batch_move: function (data) {
            return $http.post(base_url + '/accthk/batch_move', data);
        },
        account_move: function (data) {
            return $http.post(base_url + '/accthk/account_move', data);
        },
        check_manager: function (data) {
            return $http.post(base_url + '/accthk/check_manager', data);
        },
        check_lr: function (data) {
            return $http.post(base_url + '/accthk/check_lr', data);
        },
        approve: function (data) {
            return $http.post(base_url + '/accthk/approve', data);
        },
        parent_approve: function (data) {
            return $http.post(base_url + '/accthk/parent_approve', data);
        },
        parent_deny: function (data) {
            return $http.post(base_url + '/accthk/parent_deny', data);
        },
        switch_pri: function (data) {
            return $http.post(base_url + '/accthk/switch_pri', data);
        },
        deny: function (data) {
            return $http.post(base_url + '/accthk/deny', data);
        }
    };
};


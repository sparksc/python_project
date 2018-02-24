/**
 * Permission Service
 */
ysp.service('hallManagerHanderServer', hallManagerHanderServer);
hallManagerHanderServer.$inject = ['$http'];

function hallManagerHanderServer($http) {
    return {
        manager_num_save: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_num_save', data);
        },
        manager_num_delete: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_num_delete', data);
        },
        manager_num_update: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_num_update', data);
        },
       
        manager_sal_hander_save: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_sal_hander_save', data);
        },
        manager_sal_hander_delete: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_sal_hander_delete', data);
        },
        manager_sal_hander_update: function (data) {
            return $http.post(base_url + '/hall_manager_hander/manager_sal_hander_update', data);
        },
 
        other_save: function (data) {
            return $http.post(base_url + '/hall_manager_hander/other_save', data);
        },
        other_delete: function (data) {
            return $http.post(base_url + '/hall_manager_hander/other_delete', data);
        },
        other_update: function (data) {
            return $http.post(base_url + '/hall_manager_hander/other_update', data);
        },


        lieve_save: function (data) {
            return $http.post(base_url + '/hall_manager_hander/lieve_save', data);
        },
        lieve_delete: function (data) {
            return $http.post(base_url + '/hall_manager_hander/lieve_delete', data);
        },
        lieve_update: function (data) {
            return $http.post(base_url + '/hall_manager_hander/lieve_update', data);
        },

         branch_atm_save: function (data) {
            return $http.post(base_url + '/hall_manager_hander/branch_atm_save', data);
        },
        branch_atm_delete: function (data) {
            return $http.post(base_url + '/hall_manager_hander/branch_atm_delete', data);
        },
        branch_atm_update: function (data) {
            return $http.post(base_url + '/hall_manager_hander/branch_atm_update', data);
        }

       

    };
};


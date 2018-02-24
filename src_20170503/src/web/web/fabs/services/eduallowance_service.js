/**
 * EduAllowance Service
 */
ysp.service('eduAllowanceService', eduAllowanceService);
eduAllowanceService.$inject = ['$http'];

function eduAllowanceService($http) {
    return {
        edu_load: function () {
            return $http.post(base_url + '/eduallowance/edu_load');
        },
        add_save: function (data) {
            return $http.post(base_url + '//_add_save', data);
        },
        edu_edit_save: function (data) {
            return $http.post(base_url + '/eduallowance/edu_edit_save', data);
        },
        del: function (data) {
            return $http.post(base_url + '/net/net_del', data);
        }
    };
};


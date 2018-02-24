/**
 * staff_status Service
 */
ysp.service('staff_statusService', staff_statusService);
staff_statusService.$inject = ['$http'];
function staff_statusService($http) {
    return {
        update_ws: function (data) {
            return $http.post(base_url + '/users/update_ws', data);
        },
        get_group_type: function (data) {
            return $http.post(base_url + '/users/get_group_type', data);
        },
        get_group_department: function (data) {
            return $http.post(base_url + '/users/get_group_department', data);
        },
    };
};


/**
 * Branch Group User Service
 */
ysp.service('bgsService', bgsService);
bgsService.$inject = ['$http'];

function bgsService($http) {
    return {
        load: function () {
            return $http.post(base_url + '/bgs/load');
        },
        f_branches: function () {
            return $http.post(base_url + '/bgs/f_branches');
        },
        groups: function () {
            return $http.post(base_url + '/bgs/groups');
        },
        find_user: function (data) {
            return $http.post(base_url + '/bgs/find_user',data);
        },
        find_users: function (data) {
            return $http.post(base_url + '/bgs/find_users',data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/bgs/edit_save', data);
        },
        add_save: function (data) {
            return $http.post(base_url + '/bgs/add_save', data);
        }
    };
};


/**
 * Branch Group User Service
 */
ysp.service('bguService', bguService);
bguService.$inject = ['$http'];

function bguService($http) {
    return {
        load: function () {
            return $http.post(base_url + '/bgu/load');
        },
        f_branches: function () {
            return $http.post(base_url + '/bgu/f_branches');
        },
        groups: function () {
            return $http.post(base_url + '/bgu/groups');
        },
        find_user: function (data) {
            return $http.post(base_url + '/bgu/find_user',data);
        },
        find_users: function (data) {
            return $http.post(base_url + '/bgu/find_users',data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/bgu/edit_save', data);
        },
        add_save: function (data) {
            return $http.post(base_url + '/bgu/add_save', data);
        }
    };
};


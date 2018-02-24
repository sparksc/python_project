/**
 * Permission Service
 */
ysp.service('branchmanageService', branchmanageService);
branchmanageService.$inject = ['$http'];

function branchmanageService($http) {
    return {
        branchs: function (data) {
            return $http.post(base_url + '/branchmanagepermission/branchs', data);
        },
        get_branch_list: function (data) {
            return $http.post(base_url + '/branchmanagepermission/get_branch_list', data);
        },
        branch: function (data) {
            return $http.post(base_url + '/branchmanagepermission/branch', data);
        },
        branch_save:function(data){
            return $http.post(base_url + '/branchmanagepermission/branch_save',data);
        },
        branch_delete:function(data){
            return $http.post(base_url + '/branchmanagepermission/branch_delete',data);
        },
        branch_edit_save:function(data){
            return $http.post(base_url + '/branchmanagepermission/branch_edit_save',data);
        },
        check_branchs: function (data) {
            return $http.post(base_url + '/branchmanagepermission/check_branchs', data);
        },
        ords: function (data) {
            return $http.post(base_url + '/branchmanagepermission/ords', data);
        },
        users: function (data) {
            return $http.post(base_url + '/branchmanagepermission/users', data);
        },
        get_staff: function (data) {
            return $http.post(base_url + '/branchmanagepermission/get_staff', data);
        },
        find_users_by_branches: function (data) {
            return $http.post(base_url + '/branchmanagepermission/find_users_by_branches', data);
        },
        find_users_by_branch: function (data) {
            return $http.post(base_url + '/branchmanagepermission/find_users_by_branch', data);
        },
        add_save: function (data) {
            return $http.post(base_url + '/branchmanagepermission/add_save', data);
        },
        get_user_permission: function (data) {
            return $http.post(base_url + '/branchmanagepermission/get_user_permission', data);
        },
        branchgroup: function (data) {
            return $http.post(base_url + '/branchmanagepermission/branchgroup', data);
        },
        hide: function (data) {
            return $http.post(base_url + '/branchmanagepermission/hide', data);
        },
        do_allot: function (data) {
            return $http.post(base_url + '/branchmanagepermission/do_allot', data);
        },
        show: function (data) {
            return $http.post(base_url + '/branchmanagepermission/show', data);
        },
        show_org: function (data) {
            return $http.post(base_url + '/branchmanagepermission/show_org', data);
        },
        permission: function (data) {
            return $http.post(base_url + '/branchmanagepermission/permission', data);
        }
    };
};


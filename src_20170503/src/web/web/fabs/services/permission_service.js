/**
 * Permission Service
 */
ysp.service('permissionService', permissionService);
permissionService.$inject = ['$http'];

function permissionService($http) {
    return {
        init_user_pwd: function (data) {
            return $http.post(base_url + '/permission/init_user_pwd', data);
        },
        groups: function (data) {
            return $http.post(base_url + '/permission/groups', data);
        },
        groups_permission: function (data) {
            return $http.post(base_url + '/permission/groups_permission', data);
        },
        group_menus_select: function (data) {
            return $http.post(base_url + '/permission/group_menus_select', data);
        },
        user_permission_group_select: function (data) {
            return $http.post(base_url + '/permission/user_permission_group_select', data);
        },
        user_permission_group_save: function (data) {
            return $http.post(base_url + '/permission/user_permission_group_save', data);
        },
        group_menus_save: function (data) {
            return $http.post(base_url + '/permission/group_menus_save', data);
        },
        users: function (data) {
            return $http.post(base_url + '/permission/users', data);
        },
        user_groups:function(user_id){
            return $http.post(base_url + '/permission/user_groups',{'user_id':user_id});
        },
        user_groups_save:function(data){
            return $http.post(base_url + '/permission/user_groups_save',data);
        },
        user_menu_dump: function () {
            return $http.get(base_url + '/permission/user_menus');
        },
        user_permission_menu_dump: function () {
            return $http.get(base_url + '/permission/user_permission_menus');
        },
        para_menu_save: function (data) {
            return $http.post(base_url + '/permission/para_menu_save',data);
        },
        user_branches: function () {
            return $http.get(base_url + '/permission/user_branches');
        },
        menu_update: function (data) {
            return $http.post(base_url + '/permission/menu_update',data);
        },
        menu_save: function (data) {
            return $http.post(base_url + '/permission/menu_save',data);
        },
        user_update: function (data) {
            return $http.post(base_url + '/permission/user_update',data);
        },
        user_save: function (data) {
            return $http.post(base_url + '/permission/user_save',data);
        },
        get_permission_list: function (data) {
            return $http.post(base_url + '/permission/get_permission_list', data);
        },
        save_permission_list: function (data) {
            return $http.post(base_url + '/permission/save_permission_list', data);
        },
        groupdata_save:function (data) {
            return $http.post(base_url + '/permission/groupdata_save',data);
        },
        groupdata_edit:function (data) {
            return $http.post(base_url + '/permission/groupdata_edit',data);
        },
        groupdata_delete:function (data) {
            return $http.post(base_url + '/permission/groupdata_delete',data);
        }
    };
};


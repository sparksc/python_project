/**
 * Permission Service
 */
ysp.service('postmanageService', postmanageService);
postmanageService.$inject = ['$http'];

function postmanageService($http) {
    return {
        
        posts: function (data) {
            return $http.post(base_url + '/postmanagepermission/posts', data);
        },
        get_post_list: function (data) {
            return $http.post(base_url + '/postmanagepermission/get_post_list', data);
        },
        post: function (data) {
            return $http.post(base_url + '/postmanagepermission/post', data);
        },
        post_save:function(data){
            return $http.post(base_url + '/postmanagepermission/post_save',data);
        },
        post_delete:function(data){
            return $http.post(base_url + '/postmanagepermission/post_delete',data);
        },
        post_edit_save:function(data){
            return $http.post(base_url + '/postmanagepermission/post_edit_save',data);
        },
        check_posts: function (data) {
	    console.log(data)
            return $http.post(base_url + '/postmanagepermission/check_posts', data);
        },
        ords: function (data) {
            return $http.post(base_url + '/postmanagepermission/ords', data);
        },
        users: function (data) {
            return $http.post(base_url + '/postmanagepermission/users', data);
        },
        find_users_by_postes: function (data) {
            return $http.post(base_url + '/postmanagepermission/find_users_by_postes', data);
        },
        add_save: function (data) {
            return $http.post(base_url + '/postmanagepermission/add_save', data);
        }

    };
};


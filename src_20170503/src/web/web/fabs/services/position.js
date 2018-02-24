/**
 * Position Service
 */
ysp.service('poConService', poConService);
poConService.$inject = ['$http'];
function poConService($http) {
        return {

        groups: function () {
            return $http.post(base_url + '/position/groups');
        },
        department_save:function(data){
            return $http.post(base_url + '/position/department_add',data);
        },
        group_save:function(data){
            return $http.post(base_url + '/position/add',data);
        },
        type_add:function(data){
            return $http.post(base_url + '/position/type_add',data);
        },
        group_delete:function(data){
            return $http.post(base_url + '/position/group_delete',data);
        },
        department_delete:function(data){
            return $http.post(base_url + '/position/department_delete',data);
        },
        group_edit_save:function(data){
            return $http.post(base_url + '/position/group_edit_save',data);
        },
        department_edit_save:function(data){
            return $http.post(base_url + '/position/department_edit_save',data);
        },
        check_groups: function (data) {
            console.log(data)
            return $http.post(base_url + '/position/check_groups', data);
        },
        ords: function (data) {
            return $http.post(base_url + '/position/ords', data);
        }

    };

       
    
};


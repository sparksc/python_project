/**
 *ebills_managerService
*/
ysp.service('ebills_managerService', ebills_managerService);
ebills_managerService.$inject = ['$http'];

function ebills_managerService($http) {
    return {
        edit_save: function (data){ //ebills_manager
            return $http.post(base_url + '/ebills_manager/edit_save' ,data);
        },
        internation_count: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/internation_count' ,data);
        },
        hook_edit_save: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/hook_edit_save' ,data);
        },
        total_sum_save: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/total_sum_save' ,data);
        },
        total_cust_info: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/total_cust_info' ,data);
        },

        org_stand_update: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/org_stand_update' ,data);
        },

        org_stand_delete: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/org_stand_delete' ,data);
        },
        org_cunkuan_update: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/org_cunkuan_update' ,data);
        },

        org_cunkuan_delete: function (data){//ebills_hook
            return $http.post(base_url + '/ebills_manager/org_cunkuan_delete' ,data);
        }





    };
};


/**
 * Permission Service
 */
ysp.service('targetService', targetService);
targetService.$inject = ['$http'];

function targetService($http) {
    return {
        
        targets: function (data) {
            return $http.post(base_url + '/targetpermission/targets', data);
        },
        target_save:function(data){
            return $http.post(base_url + '/targetpermission/target_save',data);
        },
        target_delete:function(data){
            return $http.post(base_url + '/targetpermission/target_delete',data);
        },
        target_edit_save:function(data){
            return $http.post(base_url + '/targetpermission/target_edit_save',data);
        }

    };
};


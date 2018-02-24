/**
 *  Service
 */
ysp.service('parasetService', parasetService);
parasetService.$inject = ['$http'];

function parasetService($http) {
    return {
        
        parasets: function (data) {
            return $http.post(base_url + '/parasetpermission/parasets', data);
        },
        edit_save:function(data){
            return $http.post(base_url + '/parasetpermission/edit_save',data);
        }

    };
};


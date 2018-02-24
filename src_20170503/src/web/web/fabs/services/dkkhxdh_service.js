/**
 * dkkhxdh Service
 */
ysp.service('dkkhxdhService', dkkhxdhService);
dkkhxdhService.$inject = ['$http'];

function dkkhxdhService($http) {
    return {
        khh_save: function (data) {
            return $http.post(base_url + '/dkkhxdh/khh_save', data);
        },
        khh_delete:function(data){
            return $http.post(base_url + '/dkkhxdh/khh_delete',data)
        },
        khh_update: function (data) {
            return $http.post(base_url + '/dkkhxdh/khh_update', data);
        }
   
    };
};


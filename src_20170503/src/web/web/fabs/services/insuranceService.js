/**
 * Service
*/
ysp.service('insuranceService',insuranceService);
insuranceService.$inject = ['$http'];

function insuranceService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/insurance/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/insurance/edit_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/insurance/delete',data);
        }
    };
};


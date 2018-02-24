/**
 * Permission Service
 */
ysp.service('depappointService', depappointService);
depappointService.$inject = ['$http'];

function depappointService($http) {
    return {
        save: function (data) {
          
            return $http.post(base_url + '/depappoint/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/depappoint/update', data);
        },
        exist: function (data) {
            return $http.post(base_url + '/depappoint/exist', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/depappoint/delete', data);
        }
    };
};


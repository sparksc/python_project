/**
 * Permission Service
 */
ysp.service('reportmagService', reportmagService);
reportmagService.$inject = ['$http'];

function reportmagService($http) {
    return {
        type_save: function (data) {
            return $http.post(base_url + '/reportmag/type_save', data);
        },
        type_update: function (data) {
            return $http.post(base_url + '/reportmag/type_update', data);
        },
        menu_save: function (data) { 
            return $http.post(base_url + '/reportmag/menu_save', data);
        }
    };
};


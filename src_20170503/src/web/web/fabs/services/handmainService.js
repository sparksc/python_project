/**
 * Permission Service
 */
ysp.service('handmainService', handmainService);
handmainService.$inject = ['$http'];

function handmainService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/handmain/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/handmain/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/handmain/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/handmain/update', data);
        }
    };
};


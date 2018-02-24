/**
 * Permission Service
 */
ysp.service('subbranchdepfeeinputService', subbranchdepfeeinputService);
subbranchdepfeeinputService.$inject = ['$http'];

function subbranchdepfeeinputService($http) {
    return {
        save: function (data) {
            return $http.post(base_url + '/depstockmtfinput/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/depstockmtfinput/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/depstockmtfinput/update', data);
        }
    };
};


ysp.service('con_checkService', con_checkService);
con_checkService.$inject = ['$http'];

function con_checkService($http) {
    return {

        con_checks: function (data) {
            return $http.post(base_url + '/con_check/con_checks', data);
        }

    };
};

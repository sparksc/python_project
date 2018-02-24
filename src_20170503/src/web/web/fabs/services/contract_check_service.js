/**
 * Permission Service
 */
ysp.service('contract_checkService', contract_checkService);
contract_checkService.$inject = ['$http'];

function contract_checkService($http) {
    return {
        
        contract_checks: function (data) {
            return $http.post(base_url + '/contract_check/contract_checks', data);
        },
        objects: function () {
            return $http.post(base_url + '/contract_check/objects');
        }

    };
};


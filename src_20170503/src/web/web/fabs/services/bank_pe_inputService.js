/**
 * Permission Service
 */
ysp.service('bank_pe_inputService', bank_pe_inputService);
bank_pe_inputService.$inject = ['$http'];

function bank_pe_inputService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/bank_pe_input/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/bank_pe_input/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/bank_pe_input/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/bank_pe_input/update', data);
        }
    };
};


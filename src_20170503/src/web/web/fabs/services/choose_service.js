ysp.service('chooseService', chooseService);
chooseService.$inject = ['$http'];

function chooseService($http) {
    return {
            choose_depcpremove: function (data) {
                    return $http.post(base_url + '/chooseservice/choose_depcpremove', data);
             },
             choose_ebankpremove: function (data) {
                return $http.post(base_url + '/chooseservice/choose_ebankpremove', data);
             },
             choose_loanpremove: function (data) {
                return $http.post(base_url + '/chooseservice/choose_loanpremove', data);
             }

    }
}

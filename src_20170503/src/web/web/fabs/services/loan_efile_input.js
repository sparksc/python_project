/**
 * Permission Service
 */
ysp.service('loaninputService', loaninputService);
loaninputService.$inject = ['$http'];

function loaninputService($http) { return {
        tsave: function (data) {
            return $http.post(base_url + '/loaninput/tsave', data);
        },
        edit: function (data) {
            return $http.post(base_url + '/loaninput/edit', data);
        },
        delt: function (data) {
            return $http.post(base_url + '/loaninput/delt', data);
        },
        save:function(data){
            return $http.post(base_url + '/loaninput/save',data)
        },
        loanpersonseach:function(data){
            return $http.post(base_url + '/loaninput/loanpersonseach',data)
        },
        tdelt:function(data){
            return $http.post(base_url + '/loaninput/tdelt',data)
        },
        tedit: function (data) {
            return $http.post(base_url + '/loaninput/tedit', data);
        }
   
    };
};


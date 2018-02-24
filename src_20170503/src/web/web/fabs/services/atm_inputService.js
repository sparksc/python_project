/**
 * Permission Service
 */
ysp.service('atm_inputService', atm_inputService);
atm_inputService.$inject = ['$http'];

function atm_inputService($http) {
    return {        
        add_save: function (data) {
            return $http.post(base_url + '/atm_input/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/atm_input/edit_save' ,data);
        }
    };
};


/**
 * Permission Service
 */
ysp.service('pos_inputService', pos_inputService);
pos_inputService.$inject = ['$http'];

function pos_inputService($http) {
    return {        
        add_save: function (data) {
            return $http.post(base_url + '/pos_input/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/pos_input/edit_save' ,data);
        }
    };
};


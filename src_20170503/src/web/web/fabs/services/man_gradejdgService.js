ysp.service('man_gradejdgService', man_gradejdgService);
man_gradejdgService.$inject = ['$http'];

function man_gradejdgService($http) {
    return {
        save: function (data) {
            return $http.post(base_url + '/man_gradejdg/add_save', data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/man_gradejdg/edit_save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/man_gradejdg/update', data);
        },
        del: function (data) {
            return $http.post(base_url + '/man_gradejdg/delete', data);
        },
        delete_man: function (data) {
            return $http.post(base_url + '/man_gradejdg/delete_man', data);
        },
        get_grade_param: function (data) {
            return $http.post(base_url + '/man_gradejdg/get_grade_param', data);
        },
        grade_param: function (data) {
            return $http.post(base_url + '/man_gradejdg/grade_param', data);
        },
        get_weight: function (data) {
            return $http.post(base_url + '/man_gradejdg/get_weight', data);
        },
        get_score: function (data) {
            return $http.post(base_url + '/man_gradejdg/get_score', data);
        },
        add_grade: function (data) {
            return $http.post(base_url + '/man_gradejdg/add_grade', data);
        }
    };
};

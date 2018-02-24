ysp.service('branch_grade_reportService', branch_grade_reportService);
branch_grade_reportService.$inject = ['$http'];

function branch_grade_reportService($http) {
    return {
        update: function (data) {
            return $http.post(base_url + '/branch_grade_report/update', data);
        },
        get_grade_param: function (data) {
            return $http.post(base_url + '/branch_grade_report/get_grade_param', data);
        },
        grade_param: function (data) {
            return $http.post(base_url + '/branch_grade_report/grade_param', data);
        },
        get_weight: function (data) {
            return $http.post(base_url + '/branch_grade_report/get_weight', data);
        },
        get_score: function (data) {
            return $http.post(base_url + '/branch_grade_report/get_score', data);
        },
        add_grade: function (data) {
            return $http.post(base_url + '/branch_grade_report/add_grade', data);
        }
    };
};

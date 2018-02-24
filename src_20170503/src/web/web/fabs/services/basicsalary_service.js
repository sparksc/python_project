/**
 * BasicSalary Service
 */
ysp.service('basicSalaryService', basicSalaryService);
basicSalaryService.$inject = ['$http'];

function basicSalaryService($http) {
    return {
        posname_load: function () {
            return $http.post(base_url + '/basicsalary/posname_load');
        },
        posname_edit_save: function (data) {
            return $http.post(base_url + '/basicsalary/posname_edit_save', data);
        },
        poslev_load: function () {
            return $http.post(base_url + '/basicsalary/poslev_load');
        },
        poslev_edit_save: function (data) {
            return $http.post(base_url + '/basicsalary/poslev_edit_save', data);
        },
        salary_load: function () {
            return $http.post(base_url + '/basicsalary/salary_load');
        },
        salary_edit_save: function (data) {
            return $http.post(base_url + '/basicsalary/salary_edit_save', data);
        },
        edu_load: function () {
            return $http.post(base_url + '/basicsalary/edu_load');
        },
        edu_edit_save: function (data) {
            return $http.post(base_url + '/basicsalary/edu_edit_save', data);
        },
        del: function (data) {
            return $http.post(base_url + '/basicsalary/del', data);
        }
    };
};


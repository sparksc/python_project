/**
 * Permission Service
 */
ysp.service('StaffSalNewService', StaffSalNewService);
StaffSalNewService.$inject = ['$http'];

function StaffSalNewService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/staff_sal_input/add_save', data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/staff_sal_input/edit_save', data);
        },
        ssdelete: function (data) {
            console.log('aaaaa')
            return $http.post(base_url + '/staff_sal_input/sdelete', data);
        }
    };
};


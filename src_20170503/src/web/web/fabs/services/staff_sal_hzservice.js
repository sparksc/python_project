/**
 * Permission Service
 */
ysp.service('StaffSalHzService', StaffSalHzService);
StaffSalHzService.$inject = ['$http'];

function StaffSalHzService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/staff_sal_hzinput/add_save', data);
        },
        edit_save: function (data) {
            return $http.post(base_url + '/staff_sal_hzinput/edit_save', data);
        },
        ssdelete: function (data) {
            console.log('aaaaa')
            return $http.post(base_url + '/staff_sal_hzinput/sdelete', data);
        }
    };
};


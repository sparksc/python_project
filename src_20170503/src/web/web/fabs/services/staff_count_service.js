/**
 * Permission Service
 */
ysp.service('StaffConutSalService', StaffConutSalService);
StaffConutSalService.$inject = ['$http'];

function StaffConutSalService($http) {
    return {
        add_count:function(data){
            console.log(data)
            return $http.post(base_url + '/staff_count_input/add_count', data);
        },
        edit_save:function(data){
        console.log(data)
        return $http.post(base_url + '/staff_count_input/edit_save', data);
        }

    };
};


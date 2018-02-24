/**
 * Permission Service
 */
ysp.service('monsalaryService', monsalaryService);
monsalaryService.$inject = ['$http'];

function monsalaryService($http) {
    return {
        
        update: function (data) {
            return $http.post(base_url + '/monsalary/update', data);
        },
    	save: function (data){
	        return $http.post(base_url + '/monsalary/save' ,data);
     	}
    };
};


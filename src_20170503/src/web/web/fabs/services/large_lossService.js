/**
 * Permission Service
 */
ysp.service('large_lossService', large_lossService);
large_lossService.$inject = ['$http'];

function large_lossService($http) {
    return {
        save: function (data){
	    return $http.post(base_url + '/large_loss/save' ,data);
   	}
    };
};


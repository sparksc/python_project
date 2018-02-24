/**
 *account_rank Service
*/
ysp.service('account_rankService', account_rankService);
account_rankService.$inject = ['$http'];

function account_rankService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/account_rank/add_save', data);
        },
        edit_save: function (data){
            return $http.post(base_url + '/account_rank/edit_save' ,data);
        },
        del: function(data){
            return $http.post(base_url + '/account_rank/delete',data);
        }
    };
};


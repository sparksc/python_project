/**
 * Permission Service
 */
ysp.service('staffrelationService', staffrelationService);
staffrelationService.$inject = ['$http'];

function staffrelationService($http) {
    return {
        save: function (data) {
            return $http.post(base_url + '/staffrelation/save', data);
        },
        update: function (data) {
            return $http.post(base_url + '/staffrelation/update', data);
        },
        simple_select: function (data) {
            return $http.post(base_url + '/staffrelation/simple_select', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/staffrelation/delete', data);
        },
        tsave: function (data) {
            return $http.post(base_url + '/staffrelation/tsave', data);
        },
        tdelt: function (data) {
            return $http.post(base_url + '/staffrelation/tdelt', data);
        },
        update_his: function (data) {
            return $http.post(base_url + '/staffrelation/update_his', data);
        },
        newupdate: function (data){
            return $http.post(base_url+'/staffrelation/newupdate', data);
        },
        edit_his: function (data){
            return $http.post(base_url+'/staffrelation/edit_his', data);
        },
        delete_his: function (data){
            return $http.post(base_url+'/staffrelation/delete_his', data);
         }

    };
};


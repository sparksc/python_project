/**
 *ebank_replace Service
*/
ysp.service('ebank_replaceService', ebank_replaceService);
ebank_replaceService.$inject = ['$http'];

function ebank_replaceService($http) {
    return {
        edit_save: function (data){
            return $http.post(base_url + '/ebank_replace/edit_save',data);
        },
        del: function(data){
            return $http.post(base_url + '/ebank_replace/delete',data);
        },

        credentials:function(data){
            return $http.post(base_url+'/ebank_replace/credentials',data);
        }
    };
};


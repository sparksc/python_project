/**
 * mbox Service
 */
ysp.service('mboxService', mboxService);
mboxService.$inject = ['$http'];

function mboxService($http) {
    return {
        user:function(id){
            return $http.get(base_url+'/mbox/user?id='+id);
        },
        branch:function(){
            return $http.get(base_url+'/mbox/branch');
        }, 
        save:function(data){
            return $http.post(base_url+'/mbox/send_mbox/',data);
        },
        mbox_send_group:function(data){
            return $http.post(base_url+'/mbox/mbox_send_group/',data);
        },
        query:function(data){
            return $http.get(base_url+'/mbox/query/',data);
        },
        sent_to_teller:function(application_id,data){
            return $http.post(base_url+'/mbox/credit/'+application_id,data);
        },
        update:function(id){
            return $http.get(base_url+'/mbox/update?id='+id);
        },
        del:function(id){
            return $http.get(base_url+'/mbox/del?id='+id);
        },
    }
};

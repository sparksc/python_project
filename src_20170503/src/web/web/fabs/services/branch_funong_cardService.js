/**
 *account_rank Service
*/
ysp.service('branch_funong_cardService', branch_funong_cardService);
branch_funong_cardService.$inject = ['$http'];

function  branch_funong_cardService($http) {
    return {
        count_save: function (data){
            return $http.post(base_url + '/branch_funong_card/count_save' ,data);
        },
        conunt_del: function(data){
            return $http.post(base_url + '/branch_funong_card/conunt_del',data);
        },
        count_edit_save:function(data){
            return $http.post(base_url+'/branch_funong_card/count_edit_save',data);
        }
    };
};


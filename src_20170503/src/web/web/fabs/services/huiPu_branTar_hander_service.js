/**
 * Permission Service
 */
ysp.service('huiPuBranchTargeTService', huiPuBranchTargeTService);
huiPuBranchTargeTService.$inject = ['$http'];

function huiPuBranchTargeTService($http) {
    return {
       branchhander_save: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/branchhander_save', data);
        },
        branchhander_delete: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/branchhander_delete', data);
        },
        branchhander_update: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/branchhander_update', data);
        },

       credit_save: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/credit_save', data);
        },
        credit_delete: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/credit_delete', data);
        },
        credit_update: function (data) {
            return $http.post(base_url + '/huiPu_branchTarget_hander/credit_update', data);
        }



   };
};

//branchhander  支行目标任务手工
//credit 授信:

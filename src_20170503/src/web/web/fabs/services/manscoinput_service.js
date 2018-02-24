/**
 * Permission Service
 */
ysp.service('manscoinputService', manscoinputService);
manscoinputService.$inject = ['$http'];

function manscoinputService($http) {
    return {
        add_save: function (data) {
            return $http.post(base_url + '/manaddsco/add_save', data);
        },
        save: function (data) {
            return $http.post(base_url + '/manaddsco/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/manaddsco/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/manaddsco/update', data);
        },
        batch_move: function (data) {
            return $http.post(base_url + '/manaddsco/batch_move', data);
        },
        account_move: function (data) {
            return $http.post(base_url + '/manaddsco/account_move', data);
        }
    };
};


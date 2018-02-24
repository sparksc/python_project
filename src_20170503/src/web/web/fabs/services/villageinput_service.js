/**
 * Permission Service
 */
ysp.service('villageinputService', villageinputService);
villageinputService.$inject = ['$http'];

function villageinputService($http) {
    return {
        save: function (data) {
            return $http.post(base_url + '/villageinput/save', data);
        },
        delete: function (data) {
            return $http.post(base_url + '/villageinput/delete', data);
        },
        update: function (data) {
            return $http.post(base_url + '/villageinput/update', data);
        },
        deposit_save: function (data) {
            return $http.post(base_url + '/villageinput/deposit_save', data);
        },
        deposit_delete: function (data) {
            return $http.post(base_url + '/villageinput/deposit_delete', data);
        },
        deposit_update: function (data) {
            return $http.post(base_url + '/villageinput/deposit_update', data);
        },
        loan_save: function (data) {
            return $http.post(base_url + '/villageinput/loan_save', data);
        },
        loan_delete: function (data) {
            return $http.post(base_url + '/villageinput/loan_delete', data);
        },
        loan_update: function (data) {
            return $http.post(base_url + '/villageinput/loan_update', data);
        },
        ebank_save: function (data) {
            return $http.post(base_url + '/villageinput/ebank_save', data);
        },
        ebank_delete: function (data) {
            return $http.post(base_url + '/villageinput/ebank_delete', data);
        },
        ebank_update: function (data) {
            return $http.post(base_url + '/villageinput/ebank_update', data);
        },
        transaction_save: function (data) {
            return $http.post(base_url + '/villageinput/transaction_save', data);
        },
        transaction_delete: function (data) {
            return $http.post(base_url + '/villageinput/transaction_delete', data);
        },
        etc_data_delete: function (data) {
            return $http.post(base_url + '/villageinput/etc_data_delete', data);
        },
        etc_data_edit: function (data) {
            return $http.post(base_url + '/villageinput/etc_data_edit', data);
        },
        transaction_update: function (data) {
            return $http.post(base_url + '/villageinput/transaction_update', data);
        },
        ebank_add_save: function (data) {
            return $http.post(base_url + '/villageinput/ebank_add_save', data);
        },
        ebank_add_delete: function (data) {
            return $http.post(base_url + '/villageinput/ebank_add_delete', data);
        },
        ebank_add_update: function (data) {
            return $http.post(base_url + '/villageinput/ebank_add_update', data);
        }
    };
};

/*
存款业务计划数参数     deposit
贷款业务计划数参数     loan
电子银行业务计划数参数 ebank
交易码折算率           transaction_code
电子银行得分附加分导入 ebank_add
*/

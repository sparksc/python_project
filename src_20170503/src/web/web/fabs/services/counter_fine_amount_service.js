/**
 * Permission Service
 */
ysp.service('counterFineAmountService', counterFineAmountService);
counterFineAmountService.$inject = ['$http'];

function counterFineAmountService($http) {
    return {
        fine_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/fine_save', data);
        },
        fine_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/fine_delete', data);
        },
        fine_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/fine_update', data);
        },
       
        dot_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/dot_save', data);
        },
        dot_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/dot_delete', data);
        },
        dot_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/dot_update', data);
        },
 
        pay_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/pay_save', data);
        },
        pay_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/pay_delete', data);
        },
        pay_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/pay_update', data);
        },
 
        business_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/business_save', data);
        },
        business_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/business_delete', data);
        },
        business_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/business_update', data);
        },


        exam_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/exam_save', data);
        },
        exam_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/exam_delete', data);
        },
        exam_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/exam_update', data);
        },


        other_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/other_save', data);
        },
        other_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/other_delete', data);
        },
        other_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/other_update', data);
        },

        adjust_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/adjust_save', data);
        },
        adjust_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/adjust_delete', data);
        },
        adjust_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/adjust_update', data);
        },


        lieve_save: function (data) {
            return $http.post(base_url + '/counter_fine_amount/lieve_save', data);
        },
        lieve_delete: function (data) {
            return $http.post(base_url + '/counter_fine_amount/lieve_delete', data);
        },
        lieve_update: function (data) {
            return $http.post(base_url + '/counter_fine_amount/lieve_update', data);
        }


        

    };
};

/*
1.柜员扣罚金额手工维护 fine
2.网点自助设备 dot

3.柜员业务量代收代付手工维护 pay

4.柜员业务量计酬手工维护 business

5.柜员参与考核人数的手工维护 counter_adjust_num

6.柜员担任其他工作天数的手工维护 other

7.柜员计酬调整值手工维护 adjust
8.员工请假天数 lieve
*/

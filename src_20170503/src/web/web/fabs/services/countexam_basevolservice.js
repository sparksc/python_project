/**
 * Permission Service
 */
ysp.service('countexam_basevolservice', countexam_basevolservice);
countexam_basevolservice.$inject = ['$http'];

function countexam_basevolservice($http) {
    return {
        count_exam_base_vol_save: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/count_exam_base_vol_save', data);
        },
        count_exam_base_vol_delete: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/count_exam_base_vol_delete', data);
        },
        count_exam_base_vol_update: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/count_exam_base_vol_update', data);
        },
       
         ocr_org_rate_error_save: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/ocr_org_rate_error_save', data);
        },
        ocr_org_rate_error_delete: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/ocr_org_rate_error_delete', data);
        },
        ocr_org_rate_error_update: function (data) {
            return $http.post(base_url + '/countexam_basevol_hander/ocr_org_rate_error_update', data);
        }
 

    };
};


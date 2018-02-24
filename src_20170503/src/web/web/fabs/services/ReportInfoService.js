/**
 * Report Info Service
 */
ysp.service('ReportInfoService', ReportInfoService);
ReportInfoService.$inject = ['$http'];

function ReportInfoService($http) {
    return {
        info: function (report_name,params) {
            // delete params["e_p_P_DATE"];
            return $http({
                method:"GET",
                url:rpt_base_url+"/report_proxy/cognos/"+report_name,
                params:params
            });
        },
        action: function(conversation_id,action) {
            return $http.get(rpt_base_url+"/report_proxy/cognos/"+conversation_id+"/"+action);
        }
    };
};
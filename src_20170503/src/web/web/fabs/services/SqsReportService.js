/**
 * SqsReportService
 */
ysp.service('SqsReportService', SqsReportService);
SqsReportService.$inject = ['$http'];

function SqsReportService($http) {
    return {
        info: function (report_code,params) {
           //  delete params["e_p_P_DATE"];
            return $http({
                method:"GET",
                url:rpt_base_url+"/report_proxy/sqs/"+report_code,
                params:params
            });
        },
        action: function(conversation_id,action) {
            return $http.get(rpt_base_url+"/report_proxy/sqs/"+conversation_id);
        }
    };
};

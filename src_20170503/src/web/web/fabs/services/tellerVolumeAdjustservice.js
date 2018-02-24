/**
 * Permission Service
 */
ysp.service('tellerVolumeAdjustservice', tellerVolumeAdjustservice);
tellerVolumeAdjustservice.$inject = ['$http'];

function tellerVolumeAdjustservice($http) {
    return {
        teller_Volume_Adjust_save: function(data) {
            return $http.post(base_url + '/teller_Volume_Adjust/teller_V_Adjust_save', data);
        },
        teller_Volume_Adjust_delete: function(data) {
            return $http.post(base_url + '/teller_Volume_Adjust/teller_V_Adjust_delete', data);
        },
        teller_Volume_Adjust_update: function(data) {
            return $http.post(base_url + '/teller_Volume_Adjust/teller_V_Adjust_update', data);
        }
       
        }
 

    };


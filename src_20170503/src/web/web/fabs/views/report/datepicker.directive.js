function datePicker() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {
            $(element).daterangepicker({
                singleDatePicker: false,
                showDropdowns: true
            });

            $(element).on("apply.daterangepicker", function(ev, picker) {
                scope.$apply(function() {
                    var val = picker.startDate.format('MM/DD/YYYY');
                    ngModel.$setViewValue(val);
                    $(element).val(val);
                });
            });
        }
    };
}
angular.module('YSP').directive('datePicker', datePicker);
function app_date_ch2(data){
    if(data == undefined){
        return;
    }
    if(data == null){
        return "";
    }
    if(data == ''){
        return "";
    }
    data = data.replace(/-/g,'');
    var dat = "";
    if(data.length == 8){
        dat = data.substring(0,4);
        dat += '-';
        var month = data.substring(4,6);
        if(month >= 1 && month <= 12){
            dat += month;
        }else{
            return ""
        }
        dat += '-';
        var day = data.substring(6,8);
        end_day=Number(new Date(data.substring(0,4),month,0).getDate());
        if(day >= 1 && day <= end_day){
            dat += day;
        }else{
            return ""
        }
    }
    return dat;
}
function app_money_char(data){
    if(data === undefined || data === null || data === ''||data==='undefined'|| data==='null'){
        return ['', ''];
    }
    data = data + "";
    data = data.replace(/,/g,'');
    var data_in = data;
    if (data.indexOf('.') == -1){
        data = data + '.00';
    }
    var small = data.split('.')[1];
    if(small.length<2){
        small = small + '0'
        data_in = (data_in*1).toFixed(2)
    }else{
        data_in = (data_in*1).toFixed(small.length)
    }
    if (data.split('.')[0]=='-0'){
       var data_ch = (data.split('.')[0]).toLocaleString();
    }else{
      var data_ch = (data.split('.')[0]*1).toLocaleString();
    }
    if (data.indexOf('.') == -1){
        data_ch = data_ch + '.00';
    }else{
        data_ch = data_ch + '.'+ small;
    }
    return [data_in, data_ch]
}


angular.module('YSP').directive('textTransform', ['$filter',function($filter) { 
    var transformConfig = {
     amount:function(input){ },
     date:function(input){ },
     uppercase: function(input){
       a=input.toUpperCase();
        return  a;
     },
     capitalize: function(input){
       return input.replace(
         /([a-zA-Z])([a-zA-Z]*)/gi,
         function(matched, $1, $2){
          return $1.toUpperCase() + $2;
        });
     },
     lowercase: function(input){
       return input.toLowerCase();
     }
   };
    function amount_formatter(val) {
        if( val  === "" ||val === undefined || val === null ||val==='undefined'|| val==='null' ) vals = ["",""]
        else vals = app_money_char(val)
        return vals[1];
    }
    function date_formatter(val) {
        vals = app_date_ch2(val)
        return vals;
    }
    function date_parser(val) {
        if( val  == "" )  return null;
        var from_date = new Date(Date.parse(val.replace(/-/g,'/')));
        return from_date ;
    }
    function amount_parser(val) {
        if( val  === "" ||val === undefined || val === null ||val==='undefined'|| val==='null' )vals = ["",""]
        else vals = app_money_char(val)
        return vals[0];
    }
    return {
        require: 'ngModel',
        link: function(scope, element, iAttrs, modelCtrl) {
            var transform = transformConfig[iAttrs.textTransform];
            if(transform){
                if( iAttrs.textTransform  =="amount"){
                    modelCtrl.$formatters.push(amount_formatter);
                    modelCtrl.$parsers.unshift(amount_parser);
                    $(element).bind("blur", function(e) {
                        val =  $(this).val() 
                        if( val  == "" ) vals = ["",""]
                        else vals = app_money_char(val)
                        if(/^[-+]?\d+(\.\d+)?$/.test(vals[0]) ==false) {
                            vals[1]=''
                        }
                        $(this).val(vals[1]); 
                        $(this).trigger("input");
                    });
                    $(element).bind( "mousedown", function(e) {
                        val =  $(this).val()
                        if( val  == "" ) vals = ["",""]
                        else vals = app_money_char(val)
                        $(this).val(vals[0]);
                        $(this).trigger("input");
                    });
                    /*
                    $(element).bind("focus", function(e) {
                        val =  $(this).val()
                        if( val  == "" ) vals = ["",""]
                        else vals = app_money_char(val)
                        $(this).val(vals[0]); 
                        $(this).trigger("input");
                    });
                    */
                    //$(element).bind("keydown", function(e) {
                    //    ss=window.event||e;
                    //    k = e.keyCode ;
                    //    if( k == 37 || k == 39 || ( k>=48 && k<=57 ) || k == 8 || k ==190 || k == 46
                    //            || ( k>=96 && k<=105 ) || k == 110 || k ==13 || k==17 || k==90
                    //            || k==88 || k==67 || k==86 || k==65){

                    //    }else{
                    //      ss.preventDefault();
                    //    }
                    //});
                    element.css("text-transform", iAttrs.textTransform);
                }else if( iAttrs.textTransform  =="date"){
                    modelCtrl.$formatters.push(date_formatter);
                    $(element).bind( "blur", function(e) {
                        val =  $(this).val() 
                        val = app_date_ch2(val)
                        $(this).val(val) 
                        $(this).trigger("input");
                    });
                    element.css("text-transform", iAttrs.textTransform);
                }else if( iAttrs.textTransform  =="date2"){
                    modelCtrl.$formatters.push(date_formatter);
                    modelCtrl.$parsers.unshift(date_parser);
                    $(element).bind( "blur", function(e) {
                        val =  $(this).val() 
                        val = app_date_ch2(val)
                        if( val !=  "" ) {
                            $(this).val(val) 
                            $(this).trigger("input");
                        }else{
                        }
                    });
                    element.css("text-transform", iAttrs.textTransform);
                }else{
                    modelCtrl.$parsers.push(function(input) {
                        return transform(input || "");
                    });
                    element.css("text-transform", iAttrs.textTransform);
                }
            }
        }
    };
}]);

angular.module('YSP').directive('fdate',function(){
    return {
        restrict: 'A',
        link: function(scope,element, attrs){
                    $(element).bind( "blur", function(e) {
                        val =  $(this).val() 
                        val = app_date_ch(val)
                        if( val !=  "" ) {
                            $(this).val(val) 
                            $(this).trigger("input");
                        }
                    });
        },
    };
}) ; 

angular.module('YSP').directive('famount', ['$filter',function($filter) { 
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, elm, attrs, ctrl) {
            function formatter(val) {
                if( val  == "" ) vals = ["",""]
                else vals = app_money_char(val)
                return vals[1];
            }
            function parser(val) {
                if( val  == "" ) vals = ["",""]
                else vals = app_money_char(val)
                return vals[0];
            }
            ctrl.$formatters.push(formatter);
            ctrl.$parsers.unshift(parser);
            $(elm).bind( "blur", function(e) {
                val =  $(this).val() 
                if( val  == "" ) vals = ["",""]
                else vals = app_money_char(val)
                $(this).val(vals[1]); 
                $(this).trigger("input");
            });
        },
    };
}]) ; 

/*
 * 下拉组件
 */
function select_emplate(opt,attr){
            var istr;
            if ( attr.fclass == undefined || attr.fclass == null ){
                istr = ' <select class="form-control   "  '
            }else{
                istr = ' <select class="'+ attr.fclass+'"  '
            }
            if ( attr.fname != undefined && attr.fname != null ){
                istr = istr + ' name="' + attr.fname + '" '
            }
            if ( attr.fmodel != undefined && attr.fmodel != null ){
                istr = istr + ' ng-model="' + attr.fmodel + '" '
            }
            if ( attr.fdisabled != undefined && attr.fdisabled != null ){
                istr = istr + ' ng-disabled="' + attr.fdisabled + '" '
            }
            if ( attr.ftitle != undefined && attr.ftitle != null ){
                istr = istr + ' title="' + attr.ftitle + '" '
            }
            if ( attr.fchange != undefined && attr.fchange != null ){
                istr = istr + ' ng-change="' + attr.fchange + '" '
            }
            if ( attr.fblur!= undefined && attr.fblur != null ){
                istr = istr + ' ng-blur ="' + attr.fblur + '" '
            }
            if (  attr.frequired == 'true'){
                istr = istr + ' required> '
            }else{
                istr = istr + ' > '
            }
            opts = "<option></option>"
            for(var i=0;i<opt.length;i++){
                opts = opts + "<option>" + opt[i] + "</option>"
            }

            istr = istr + opts + '</select> '
            return istr
}

function selectx(opt){
    return {
        restrict: 'E',
        replace: 'true',
        template:function(element, attr) {
            return select_emplate(opt,attr);
        },
    };
}

angular.module('YSP').directive('fidtype', function(){
    opt = [ "身份证","户口本","护照","军官证","士兵证","其他个人证件","香港身份证","澳门身份证","台湾身份证","港澳居民来往内地通行证","台湾同胞来往内地通行证","临时身份证","外国人居留证","警官证","组织机构代码证","营业执照","其他企业证件"]
    return selectx(opt) ;
} );

angular.module('YSP').directive('fnation', function(){
    opt = [ "汉族","满族","蒙古族", "回族", "其他"]
    return selectx(opt) ;
} );

angular.module('YSP').directive('fprelation', function(){
    opt = [ "配偶","父母","子女", "其他血亲", "其他嫡亲"]
    return selectx(opt) ;
} );
angular.module('YSP').directive('fbool', function(){
    opt = [ "是","否"]
    return selectx(opt) ;
} );

function log(obj) {
    var props = "";
    for (var p in obj) {
        if (typeof ( obj [p]) == " function ") {
            obj [p]();
        } else {
            props += p + " = " + obj [p] + " \n\t\n  ";
        }
    }
    console.log(props);
}

/**
 * console.log(form_serializable(document.getElementById(form_id)));
 * @param form_element
 * @returns {{form dict}}
 */
function form_serializable(form_element){
    var form_dict = {};
    $(form_element).find('label').each(function (idx, label) {
        $(label).next().find('select').each(function(idx,select){
            form_dict[$(label).text()] = $(select).val();
        });
        $(label).next().find('input').each(function(idx,input){
            form_dict[$(label).text()] = $(input).val();
        });
    });
    return form_dict;
}

var ysp = angular.module("YSP", [
    "ui.router",
    "oc.lazyLoad",
    "ui.bootstrap",
    "ngSanitize",
    'daterangepicker',
    "checklist-model"
]);



//############################################
//   Application Configuration
//############################################

base_url = 'http://154.188.1.104:3007'
rpt_base_url = 'http://154.188.1.104:8082';



var server_out = true;
var error_out = true;

ysp.constant('ENDPOINT_URI', base_url);

ysp.config(['$controllerProvider', '$compileProvider', '$filterProvider', '$provide',
    function ($controllerProvider, $compileProvider, $filterProvider, $provide) {
        $provide.decorator('$exceptionHandler', ['$log', '$delegate',
            function ($log, $delegate) {
                return function (exception, cause) {
                    $delegate(exception, cause);
                };
            }
        ]);
    }
]);


ysp.config(['$ocLazyLoadProvider', function ($ocLazyLoadProvider) {
    $ocLazyLoadProvider.config({});
}]);

ysp.config(['$controllerProvider', function ($controllerProvider) {
    $controllerProvider.allowGlobals();
}]);


ysp.factory('store', ['$window', function ($window) {
    return {
        setLocal: function (key, value) {
            try {
                if ($window.Storage) {
                    $window.localStorage.setItem(key, value);
                    return true;
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        getLocal: function (key) {
            try {
                if ($window.Storage) {
                    return $window.localStorage.setItem(key);
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        removeLocal: function (key) {
            try {
                if ($window.Storage) {
                    $window.localStorage.removeItem(key);
                    return true;
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        setSession: function (key, value) {
            try {
                if ($window.Storage) {
                    $window.sessionStorage.setItem(key, value);
                    return true;
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        getSession: function(key) {
            try {
                if ($window.Storage) {
                    return $window.sessionStorage.getItem(key);
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        removeSession: function(key) {
            try {
                if ($window.Storage) {
                    $window.sessionStorage.removeItem(key);
                    return true;
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }
        },
        clear: function(key){
            try {
                if ($window.Storage) {
                    $window.sessionStorage.clear();
                    return true;
                } else {
                    return false;
                }
            } catch (error) {
                console.error(error, error.message);
            }

        }
    }
}]);


ysp.factory('settings', ['$rootScope', function ($rootScope) {
    var settings = {
        layout: {
            pageSidebarClosed: false,
            pageBodySolid: false,
            pageAutoScrollOnLoad: 1000
        },
        layoutImgPath: Fabs.getAssetsPath() + 'admin/layout/img/',
        layoutCssPath: Fabs.getAssetsPath() + 'admin/layout/css/'
    };
    $rootScope.settings = settings;
    return settings;
}]);

var deal_branch_list_nodes = function(branch_list){
    var data = [];
    var Nodes = [];
    data = branch_list
    for(var i = 0 ; i < data.length ; ++i)
    {
        var One = new Object();
        pro_arr = data[i].child_branch;
        One.children=new Array();
        if(pro_arr.length>0)
        {
            One.name = pro_arr[0].parent_branch.branch_name.trim();
            One.id = pro_arr[0].parent_branch.branch_code;
            One.pId = data[i].parent_branch.branch_code;
            for (var j = 0 ; j < pro_arr.length; ++j)
            {
                var Two = new Object();
                Two.name=pro_arr[j].child_branch.branch_name.trim();
                Two.id=pro_arr[j].child_branch.branch_code;
                Two.pId=pro_arr[j].parent_branch.branch_code;
                Two.click="choose_branch_type(this, '"+pro_arr[j].child_branch.branch_code+"', '"+Two.name+"','"+pro_arr[j].child_branch.branch_level+"')";
                One.children.push(Two);
            }
        }
        else
        {
            One.name = data[i].child_branch.branch_name.trim();
            One.id = data[i].child_branch.branch_code;
            One.pId = data[i].parent_branch.branch_code;
            One.click="choose_branch_type(this, '"+data[i].child_branch.branch_code+"', '"+One.name+"','"+data[i].child_branch.branch_level+"')";
        }
        Nodes.push(One);

    }
    console.log("application Nodes:");
    console.log(Nodes);
    return Nodes;
}

ysp.controller("loginCtrl",["$rootScope","$scope","$state","SessionService","store",function($rootScope,$scope, $state,SessionService,store){
    $scope.username='';
    $scope.password='';

    $scope.doLogin = function(){
        SessionService.login({
            'username':$scope.username,
            'password':$scope.password
        }).then(function(data){
            if(data){
                if(data.error){
                    alert(data.error);
                }else{
                    store.setSession("token",data.token);
                    store.setSession("is_login",true);
                    angular.forEach(data.data , function(v, k) {
                        if (k == 'branch_list')
                        { 
                            vv = deal_branch_list_nodes(v);
                            store.setSession(k,angular.toJson(vv));
                            // $rootScope.branch_list =  vv;
                            // console.log($rootScope.branch_list);
                        }
                        else
                        {
                            store.setSession(k,v);
                        }
                    });
                    $rootScope.user_session={
                        'branch_code':store.getSession("branch_code"),
                        'branch_name':store.getSession("branch_name"),
                        'user_code':store.getSession("user_name"),
                        'user_name':store.getSession("name"),
                        'user_id':store.getSession("role_id")
                    };
                    $rootScope.message_count =  store.getSession("message_count");
                    $rootScope.current_date = store.getSession("current_date");
                    $rootScope.is_login =  store.getSession("is_login");
                    //登陆成功跳转到汇总页面
                    setTimeout(function() {
                        $rootScope.forward('我的工作台','views/base/workbench.html');
                    }, 10);
                }
            }
        });
    };
}]);


ysp.controller('AppController', ['$scope', '$rootScope', '$compile', "store", function ($scope, $rootScope, $compile, store) {
    $scope.$on('$viewContentLoaded', function () {
        Fabs.initComponents();
    });
    $rootScope.user_session={
        'branch_code':store.getSession("branch_code"),
        'branch_name':store.getSession("branch_name"),
        'user_code':store.getSession("user_name"),
        'user_name':store.getSession("name"),
        'user_id':store.getSession("role_id")
    };
    $rootScope.current_date = store.getSession("current_date");
    $rootScope.is_login =  store.getSession("is_login");
    $rootScope.message_count =  store.getSession("message_count");
    //$rootScope.branch_list =  store.getSession("branch_list");
    var tmp_branch_list = store.getSession("branch_list");
    $rootScope.isObject = function(v){
        return typeof(v)=="object";
    }
    try{
        console.log(angular.fromJson(tmp_branch_list))
        $rootScope.branch_list = tmp_branch_list ? angular.fromJson(tmp_branch_list) : tmp_branch_list
    }catch(e){ console.log(e)}


    //var date = new Date();
    //$scope.current_date = $filter('date')(new Date(), 'yyyy-MM-dd');

    $rootScope.pattern = {
        "idcard":'\\d{15}$|^\\d{18}$|^\\d{17}(\\d|X|x)',  //身份证
        "card":'\\d{16}|\\d{19}',   //银行卡号
        "icc":'\\d{18}$|^\\w{18}',             //信用代码
        "oic":'(\\d{9}$|^\\w{9})|((\\d{9}|\\w{8})-(\\d{1}|\\w{1}))',//组织机构代码
        "ntrn":'(\\d{15}$|^\\w{15})|(\\d{18}$|^\\w{18})',            //国税登记证号
        "ltrn":'(\\d{15}$|^\\w{15})|(\\d{18}$|^\\w{18})',            //地税登记证号
        "aol":'\\d{14}$|^\\w{14}',            //开户许可证号
        "postalcode":'\\d{6}',            //邮政编码
        "telephone":'(\\d{3}-?\\d{8})|(\\d{4}-?\\d{7})|(\\d{7})',            //电话号码
        "mobilephone":'1\\d{10}',            //手机号码
        "amount":'(([0-9,]|([1-9,][0-9,]{0,15}))((\\.\\d{1,2})?))', //金额
        "date":'(\\d{4}-\\d{2}-\\d{2})|(\\d{8})',
        "num":'^[0-9]*$',
        "bank":'\\d{12}'                   //票据开户行行号
    };
    
    $rootScope.date_opts  = {
        singleDatePicker: true, 
        locale: {
            daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
            monthNames: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'
            ]
        },
    };
 

    // 添加
    $rootScope.tabIndex = 0;
    $rootScope.currIndex = 0;
    $rootScope.tab = {};

    var defaultEvent = {
        'on':function(){
            return true;
        }
    };

    var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':''};


    $rootScope.menuForward = function(menu,$event){
        if(menu && 'active' in menu && menu.active == true){
            menu.active = false;
        }else if(menu){
            menu.active = true;
        }
        if(menu.children == null){
            $rootScope.forward(menu.name,menu.location,{},$event);
        }
    };

    $rootScope.forward = function(name,url,params,$event){
        $rootScope.appendTab(name,url,params);
    };

    $rootScope.appendTab = function(name,src,params){
        if(!src){
            return;
        }
        var htmlContent = '<div ng-include="\''+ src  +'\'"></div>';
        $rootScope.addTab(name, htmlContent, eventObj, true, params);
    };


    $rootScope.addTab = function(tabName, htmlContent, eventObj, autoFocus, tabData){
        var t = null;
        for(var tb_idx in $rootScope.tab){
            var item_tab = $rootScope.tab[tb_idx];
            if(item_tab.tabName === tabName){
                t = item_tab;
            }
        }
        if(t==null){
            t = new Object();
            t.index = $rootScope.tabIndex;
            t.tabName = tabName;
            t.htmlContent = htmlContent;
            t.createEvent = eventObj.create? eventObj.create:defaultEvent;
            t.closeEvent = eventObj.close? eventObj.close:defaultEvent;
            t.focusEvent = eventObj.focus? eventObj.focus:defaultEvent;
            t.loseFocusEvent = eventObj.loseFocus? eventObj.loseFocus:defaultEvent;

            $rootScope.tab[t.index] = t;
            $rootScope.tabCreate(t, tabData);
            $rootScope.tabIndex = $rootScope.tabIndex + 1;
        }
        // auto change focus
        if (autoFocus == true){
            $rootScope.changeFocus(t.index);
        }
        return t.index
    };


    $rootScope.tabCreate = function(tabObj, tabData){
        succ_flag = $rootScope.tab[tabObj.index].createEvent.on();
        if(succ_flag==true){
            var tabId = 'tab_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            // var tabHtml = '<li ng-click="changeFocus('+ tabObj.index+ ')"><a href="#'+ tabContentId +'" data-toggle="tab">'+ tabName +' <span class="glyphicon glyphicon-remove-circle" ng-click="tabClose(\''+tabObj.index+'\')"></span></a></li>';
            // var tabContentHtml = '<div class="tab-pane" id="'+ tabContentId +'"></div>';
            var tabHtml = '<button type="botton"  id="'+ tabId +'"  ng-click="changeFocus(\''+ tabObj.index+ '\')" class="btn xd-on">'+ tabName +' <a href="#" ng-click="tabClose(\''+tabObj.index+'\')" class="btn iconfont icon-guanbi xd-ml5"></a></button>';
            var tabContentHtml = '<div  id="'+ tabContentId +'" ></div>';


            baseScope = angular.element(document.getElementById('main-page-content')).scope();
            scope = baseScope.$new();
            scope['tabId'] = tabObj.index;
            for(var i in tabData){
                scope[i] = tabData[i];
            }

            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);

            angular.element(document.getElementById('navtab')).append(tabElement);
            angular.element(document.getElementById('TabContent')).append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);
        }else{
            alert("tab 创建失败");
        };
    };

    $rootScope.changeFocus = function(focus_tab_id){
        if ($rootScope.tab[$rootScope.currIndex] != undefined){
            $rootScope.tabLoseFocus($rootScope.currIndex);
        }
        $rootScope.tabFocus(focus_tab_id);
        $rootScope.currIndex = focus_tab_id;
        //$rootScope.changeSubFocus(0)

        $rootScope.curSubIndex = focus_tab_id;
    };
    $rootScope.changeSubFocus = function(focus_tabId){
        $rootScope.subTabLoseFocus($scope.currSubIndex);
        $rootScope.subTabFocus(focus_tabId);
        $rootScope.curSubIndex = focus_tabId;
    };     
    $rootScope.tabLoseFocus = function(index){
        succ_flag = $rootScope.tab[index].loseFocusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('tab_'+ index)).removeClass("ng-scope xd-on").addClass("ng-scope");
            angular.element(document.getElementById('tab_'+ index + '_content')).hide();
            angular.element(document.getElementById('sub_navtab_'+index)).hide();
        }else{
            alert("失焦失败！");
        };
    };

    $rootScope.tabFocus = function(index){
        succ_flag = $rootScope.tab[index].focusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('tab_'+ index)).removeClass("ng-scope").addClass("ng-scope xd-on");
            angular.element(document.getElementById('tab_'+ index + '_content')).show();
            angular.element(document.getElementById('sub_navtab_'+index)).show();
        }else{
            alert("聚焦失败！");
        };
    }

    /* TODO: 现判断是否为当前focus页面, 寻找左右最近的tab进行聚焦，是否需要用堆栈回退最近操作的tab页面*/
    $rootScope.tabClose = function(index){
        succ_flag = $rootScope.tab[index].closeEvent.on();
        if(succ_flag==true){
            if(index == $rootScope.currIndex){
                var prevElement = angular.element(document.getElementById('tab_'+ index)).prev();
                var nextElement = angular.element(document.getElementById('tab_'+ index)).next();
                if (prevElement.length > 0){
                    $rootScope.changeFocus(prevElement.attr('id').split('_')[1]);
                }else if(nextElement.length > 0 ){
                    $rootScope.changeFocus(nextElement.attr('id').split('_')[1]);
                }
            }
            angular.element(document.getElementById('tab_'+index)).remove();
            angular.element(document.getElementById('tab_'+index+'_content')).remove();
            angular.element(document.getElementById('sub_navtab_'+index)).remove();
            delete $rootScope.tab[index];
        }else{
            alert("关闭失败！");
        }
    };
    $rootScope.subTabIndex = 0;
    $rootScope.currSubIndex = 0;
    $rootScope.subTab = {}; //check if open the same tab
    $rootScope.addSubTab = function(index,tabName, htmlContent, eventObj, autoFocus,tabData){
        var t = new Object();
        t.index = index;
        t.tabName = tabName;
        t.htmlContent = htmlContent;
        t.createEvent = eventObj.create? eventObj.create:defaultEvent;
        t.closeEvent = eventObj.close? eventObj.close:defaultEvent;
        t.focusEvent = eventObj.focus? eventObj.focus:defaultEvent;
        t.loseFocusEvent = eventObj.loseFocus? eventObj.loseFocus:defaultEvent;
        $rootScope.subTab[t.index] = t;
        var tabContentId = $rootScope.subTabCreate(t,tabData);
        if (autoFocus == true){
            $rootScope.changeFocus(t.index);
        }
        return t.index;
    }; 
    
    $rootScope.subTabCreate = function(tabObj,tabData){
        var subindex= $rootScope.tabIndex-1;
        succ_flag = $rootScope.subTab[tabObj.index].createEvent.on();
        if(succ_flag==true){
            var tabId = 'loan_tab_' + subindex + '_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            // var tabHtml = '<li id="'+ tabId +'" ng-click="changeSubFocus('+tabObj.index+')"> <a href="#'+ tabContentId +'" data-toggle="tab"></a></li>';
            var tabHtml = '<a  href="#'+ tabContentId +'" data-toggle="tab"  id="'+ tabId +'" ng-click="changeSubFocus('+tabObj.index+')" class="xd-barBtn xd-txt-white pull-left">'+ tabName +'</a>';
            var tabContentHtml = '<div class="tab-pane" id="'+ tabContentId +'"></div>';
            baseScope = angular.element(document.getElementById('tab_'+subindex + '_content')).find("div[name='tabContent']").scope();
            var scope = baseScope.$new();
            scope.subTabId = tabContentId;
            for(var i in tabData){
                scope[i] = tabData[i];
            }


            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);

            var sub_navtab = angular.element(document.getElementById('xd-bar')).find('#sub_navtab_'+ subindex +'');
            if(sub_navtab.length==0){
                var sub_navtab = '<div class="xd-bar" id="sub_navtab_'+ subindex +'" ><div class="xd-clr"></div></div>';
                sub_navtab = angular.element(document.getElementById('xd-bar')).append(sub_navtab);
            }
            sub_navtab = angular.element(document.getElementById('xd-bar')).find('#sub_navtab_'+ subindex +'');
            sub_navtab.prepend(tabElement);
            angular.element(document.getElementById('tab_'+ subindex + '_content')).find("div[name='tabContent']").append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);

            return tabContentId;
        }else{
            alert("tab 创建失败");
        };
    };
    $rootScope.subTabLoseFocus = function(index){
        succ_flag = $rootScope.subTab[index].loseFocusEvent.on();
        var currindex=$rootScope.currIndex;
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ currindex + '_' + index)).removeClass("ng-scope active").addClass("ng-scope");
            angular.element(document.getElementById('loan_tab_'+ currindex + '_' + index + '_content')).removeClass("tab-pane active").addClass("tab-pane");
        }else{
            alert("失焦失败！");
        }
    };

    $rootScope.subTabFocus = function(index){
        $rootScope.currSubIndex =index;
        var currindex=$rootScope.currIndex;
        succ_flag = $rootScope.subTab[index].focusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ currindex + '_' + index)).addClass("active");
            angular.element(document.getElementById('loan_tab_'+ currindex + '_' + index + '_content')).removeClass("tab-pane").addClass("tab-pane active");
        }else{
            alert("聚焦失败！");
        }
    };
    $rootScope.subTabClose = function(index){
        succ_flag = $rootScope.subTab[index].closeEvent.on();
        if(succ_flag==true){
            if(index == $scope.currSubIndex){
                var prevElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).prev();
                var nextElement = angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).next();
                if (prevElement.length > 0){
                    $rootScope.changeSubFocus(prevElement.attr('id').split('_')[3]);
                }else if(nextElement.length > 0 ){
                    $rootScope.changeSubFocus(nextElement.attr('id').split('_')[3]);
                }else{
                    $rootScope.changeSubFocus(0);
                }
            }
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index)).remove();
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' +index+'_content')).remove();
            delete $rootScope.subTab[index];
        }else{
            alert("关闭失败！");
        }
    };
}]);


ysp.controller('GeneralPageController', ['$rootScope', '$scope', 'settings', function ($rootScope, $scope, settings) {
    $scope.$on('$viewContentLoaded', function () {
        // initialize core components
        Fabs.initAjax();

        // set default layout mode
        $rootScope.settings.layout.pageBodySolid = false;
        $rootScope.settings.layout.pageSidebarClosed = false;
    });
}]);

ysp.factory('httpRequest', ['$http', function ($http) {
        return $http;
    }]
);

ysp.factory("httpInterceptor",function($rootScope,$q,store){
    return {
        'request': function(config) {
            var token = store.getSession("token");
            //var data = store.getSession("data");
            //config.data ={"data": config.data , "token":token ? "" : token };
            config.headers['x-session-token'] = (token== null ? "" : token) ;
            return config;
        },
        'requestError': function(rejection) {
            return $q.reject(rejection);
        },
        'response': function(response) {
            /**
            data = [object Object]
            status = 200
            headers = function (c){a||(a=bd(b));return c?(c=a[L(c)],void 0===c&&(c=null),c):a}
            config = [object Object]
            statusText = OK
            **/
            return response;
        },
        'responseError': function(errorResponse) {
            switch (errorResponse.status){
                case 0:
                    if(server_out){
                        server_out = false;
                        alert('服务器连接失败!请联系管理员!');
                        window.setTimeout(function(){
                            server_out = true;
                        },20000);
                    }
                    return $q.reject(errorResponse);
                case 400:
                    /**
                    var errorMsg = errorResponse.data.message;
                    if(errorResponse.data.errors && errorResponse.data.errors.length > 0) {
                        for(var i=0; i<errorResponse.data.errors.length; i++) {
                            errorMsg += errorResponse.data.errors[i];
                        }
                    }
                    **/
                    console.log('error 400');
                    break;
                case 401:
                    var token = store.getSession("token");
                    if(token){
                        store.clear();
                    }
                    if($rootScope.is_login){
                        $rootScope.is_login = false;
                        window.location.reload();
                        alert('登录超时,请重新登录！');
                    }
                    return $q.reject(errorResponse);
                case 403:
                    console.log('error 403');
                    break;
                case 404:
                    //alert("需要跟业务确定要素！");
                    break;
                case 461:
                    alert("请修改初始密码!");
                    angular.element('#logout_modal').modal('show')
                    break;
                case 405:
                    console.log('HTTP verb not supported [405]');
                    break;
                case 500:
                    if(error_out){
                        error_out = false;
                        alert(errorResponse.data.error);
                        window.setTimeout(function(){
                            error_out = true;
                        },100);
                    }
                    return $q.reject(errorResponse);
                default :
                    //console.log(JSON.parse(JSON.stringify(errorResponse.data)));
                    console.log('error default');
                    break;
            }
            return $q.reject(errorResponse);
        }
    };
});



ysp.service('SessionService',["$q","$http",function($q,$http){
    return  {
        login:function(data){
            var deferred = $q.defer();
            $http.post(base_url+'/users/login',data).
            success(function(data) {
                deferred.resolve(data);
            }).
            error(function(data) {
                deferred.reject(data);
            });
            return deferred.promise;
        }
    };
}]);



ysp.config(['$stateProvider', '$urlRouterProvider', '$httpProvider', '$locationProvider',
    function ($stateProvider, $urlRouterProvider, $httpProvider, $locationProvider) {

        $httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
        $httpProvider.interceptors.push('httpInterceptor');


        $urlRouterProvider.otherwise("/credit");



        $stateProvider

            .state('credit', {
                abstract: true,
                url: '/credit',
                template: '<div ui-view></div>',
                resolve: {
                    deps: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            name: 'YSP',
                            insertBefore: '#ng_load_plugins_before',
                            files: [
                                'views/credit/loanService.js',
                                'views/credit/loanController.js'
                            ]
                        }])
                    }]
                }
                ,resolve: {
                    deps: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            name: 'YSP',
                            insertBefore: '#ng_load_plugins_before',
                            files: [
                                'views/credit/loanController.js',
                                'views/credit/loanService.js'
                            ]
                        }])
                    }]
                }
            })

            .state('credit.list', {
                url: '',
                templateUrl: 'views/credit/index.html',
                controller: 'loanController',
                data: {pageTitle: '绩效管理系统'}
            })


            .state('user', {
                abstract: true,
                url: '/user',
                template: '<div ui-view></div>',
                resolve: {
                    deps: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            name: 'YSP',
                            insertBefore: '#ng_load_plugins_before',
                            files: [
                                'views/role/roleService.js',
                                'views/user/userService.js',
                                'views/user/userController.js'
                            ]
                        }])
                    }]
                }
            })

            .state('user.list', {
                url: '',
                templateUrl: 'views/user/list.html',
                controller: 'userController',
                data: {pageTitle: '用户列表'}
            })

            .state('user.add', {
                url: '/add',
                templateUrl: 'views/user/add.html',
                controller: 'userAddController',
                data: {pageTitle: '用户新增'}
            })

            .state('user.edit', {
                url: '/edit/:id',
                templateUrl: 'views/user/edit.html',
                controller: 'userEditController',
                data: {pageTitle: '用户修改'}
            })


            .state('role', {
                abstract: true,
                url: '/role',
                template: '<div ui-view></div>',
                resolve: {
                    deps: ['$ocLazyLoad', function ($ocLazyLoad) {
                        return $ocLazyLoad.load([{
                            name: 'YSP',
                            insertBefore: '#ng_load_plugins_before',
                            files: [
                                'views/role/roleController.js',
                                'views/role/roleService.js'
                            ]
                        }])
                    }]
                }
            })
            .state('role.list', {
                url:'',
                templateUrl: 'views/role/list.html',
                controller: 'roleController',
                data: {pageTitle: '角色管理'}
            })

    }]);


/********************************************
 YSP Pagination:
 *********************************************/
ysp.controller('YSPPaginationController', ['$scope', '$attrs', '$parse', function ($scope, $attrs, $parse) {
    var self = this,
        ngModelCtrl = {$setViewValue: angular.noop},
        setNumPages = $attrs.numPages ? $parse($attrs.numPages).assign : angular.noop;

    this.init = function (ngModelCtrl_, config) {
        ngModelCtrl = ngModelCtrl_;
        this.config = config;

        ngModelCtrl.$render = function () {
            self.render();
        };

        if ($attrs.itemsPerPage) {
            $scope.$parent.$watch($parse($attrs.itemsPerPage), function (value) {
                self.itemsPerPage = parseInt(value, 10);
                $scope.totalPages = self.calculateTotalPages();
            });
        } else {
            this.itemsPerPage = config.itemsPerPage;
        }

        $scope.$watch('totalItems', function () {
            $scope.totalPages = self.calculateTotalPages();
        });

        $scope.$watch('totalPages', function (value) {
            setNumPages($scope.$parent, value);

            if ($scope.page > value) {
                $scope.selectPage(value);
            } else {
                ngModelCtrl.$render();
            }
        });
    };

    this.calculateTotalPages = function () {
        var totalPages = this.itemsPerPage < 1 ? 1 : Math.ceil($scope.totalItems / this.itemsPerPage);
        return Math.max(totalPages || 0, 1);
    };

    this.render = function () {
        $scope.page = parseInt(ngModelCtrl.$viewValue, 10) || 1;
    };

    $scope.selectPage = function (page, evt) {
        if ($scope.page !== page && page > 0 && page <= $scope.totalPages) {
            if (evt && evt.target) {
                evt.target.blur();
            }
            ngModelCtrl.$setViewValue(page);
            ngModelCtrl.$render();
        }
    };

    $scope.getText = function (key) {
        return $scope[key + 'Text'] || self.config[key + 'Text'];
    };
    $scope.noPrevious = function () {
        return $scope.page === 1;
    };
    $scope.noNext = function () {
        return $scope.page === $scope.totalPages;
    };
}])

    .constant('YSPPaginationConfig', {
        itemsPerPage: 10,
        boundaryLinks: false,
        directionLinks: true,
        firstText: '首页',
        previousText: '上一页',
        nextText: '下一页',
        lastText: '尾页',
        rotate: true
    })

    .directive('yspPagination', ['$parse', 'YSPPaginationConfig', function ($parse, paginationConfig) {
        return {
            restrict: 'EA',
            scope: {
                totalItems: '=',
                firstText: '@',
                previousText: '@',
                nextText: '@',
                lastText: '@'
            },
            require: ['yspPagination', '?ngModel'],
            controller: 'YSPPaginationController',
            templateUrl: 'assets/template/pagination/pagination.html',
            replace: true,
            link: function (scope, element, attrs, ctrls) {
                var paginationCtrl = ctrls[0], ngModelCtrl = ctrls[1];

                if (!ngModelCtrl) {
                    return;
                }

                var maxSize = angular.isDefined(attrs.maxSize) ? scope.$parent.$eval(attrs.maxSize) : paginationConfig.maxSize,
                    rotate = angular.isDefined(attrs.rotate) ? scope.$parent.$eval(attrs.rotate) : paginationConfig.rotate;
                scope.boundaryLinks = angular.isDefined(attrs.boundaryLinks) ? scope.$parent.$eval(attrs.boundaryLinks) : paginationConfig.boundaryLinks;
                scope.directionLinks = angular.isDefined(attrs.directionLinks) ? scope.$parent.$eval(attrs.directionLinks) : paginationConfig.directionLinks;

                paginationCtrl.init(ngModelCtrl, paginationConfig);

                if (attrs.maxSize) {
                    scope.$parent.$watch($parse(attrs.maxSize), function (value) {
                        maxSize = parseInt(value, 10);
                        paginationCtrl.render();
                    });
                }

                function makePage(number, text, isActive) {
                    return {
                        number: number,
                        text: text,
                        active: isActive
                    };
                }

                function getPages(currentPage, totalPages) {
                    var pages = [];

                    var startPage = 1, endPage = totalPages;
                    var isMaxSized = ( angular.isDefined(maxSize) && maxSize < totalPages );

                    if (isMaxSized) {
                        if (rotate) {
                            startPage = Math.max(currentPage - Math.floor(maxSize / 2), 1);
                            endPage = startPage + maxSize - 1;

                            if (endPage > totalPages) {
                                endPage = totalPages;
                                startPage = endPage - maxSize + 1;
                            }
                        } else {
                            startPage = ((Math.ceil(currentPage / maxSize) - 1) * maxSize) + 1;

                            endPage = Math.min(startPage + maxSize - 1, totalPages);
                        }
                    }

                    for (var number = startPage; number <= endPage; number++) {
                        var page = makePage(number, number, number === currentPage);
                        pages.push(page);
                    }

                    if (isMaxSized && !rotate) {
                        if (startPage > 1) {
                            var previousPageSet = makePage(startPage - 1, '...', false);
                            pages.unshift(previousPageSet);
                        }

                        if (endPage < totalPages) {
                            var nextPageSet = makePage(endPage + 1, '...', false);
                            pages.push(nextPageSet);
                        }
                    }

                    return pages;
                }

                var originalRender = paginationCtrl.render;
                paginationCtrl.render = function () {
                    originalRender();
                    if (scope.page > 0 && scope.page <= scope.totalPages) {
                        scope.pages = getPages(scope.page, scope.totalPages);
                    }
                };
            }
        };
    }]);

ysp.directive("template", function() {
    return {
        template: '<ng-include src="getTemplateUrl()"/>',
        scope: {
            user: '@src'
        },
        restrict: 'E',
        controller: function ($scope) {
            $scope.getTemplateUrl = function () {
                console.log($scope.user);
                return "a.html";
            }
        }
    };
});







/**********************************
 * YSP Core Function
 **********************************/
ysp.length = function (obj) {
    if (obj) {
        return Object.keys(obj).length
    }
    return -1;
};

ysp.forEach = angular.forEach;
ysp.isArray = angular.isArray;
ysp.copy = angular.copy;


function isNullOrUndefined(obj) {
    if (obj === undefined || obj === null) {
        return true;
    }
    return false;
};

function trim(str) {
    return str.replace(/(^\s*)|(\s*$)/g, "");
}

function ltrim(str) {
    return str.replace(/(^\s*)/g, "");
}

function rtrim(str) {
    return str.replace(/(\s*$)/g, "");
}

function isBlank(obj) {
    if (isNullOrUndefined(obj) || (typeof(obj) == 'string' && trim(obj) === '')) {
        return true;
    }
    return false;
}
function serializableParams(obj) {
    var queryParams = {};
    ysp.forEach(obj, function (value, key) {

        if (!ysp.isBlank(value)) {
            if(value instanceof Array && !value.length>0){

            }else{
                queryParams[key] = value;
            }
        }
    });
    log(queryParams);
    return queryParams;
}

function extend() {
    var target = arguments[0] || {}, i = 1, length = arguments.length, deep = false, options;
    if (target.constructor == Boolean) {
        deep = target;
        target = arguments[1] || {};
        i = 2;
    }
    if (typeof target != "object" && typeof target != "function") {
        target = {};
    }
    if (length == i) {
        target = this;
        --i;
    }
    for (; i < length; i++) {
        if ((options = arguments[i]) != null)
            for (var name in options) {
                var src = target[name], copy = options[name];
                if (target === copy) {
                    continue;
                }
                if (deep && copy && typeof copy == "object" && !copy.nodeType) {
                    target[name] = extend(deep,
                        src || ( copy.length != null ? [] : {} )
                        , copy);
                } else if (copy !== undefined) {
                    target[name] = copy;
                }
            }
    }
    return target;
};


ysp.isNullOrUndefined = isNullOrUndefined;
ysp.trim = trim;
ysp.ltrim = ltrim;
ysp.rtrim = rtrim;
ysp.isBlank = isBlank;
ysp.serializableParams = serializableParams;
ysp.extend = extend;



ysp.directive('ngSpinnerBar', ['$rootScope',
    function($rootScope) {
        return {
            link: function(scope, element, attrs) {
                element.addClass('hide');

                $rootScope.$on('$stateChangeStart', function() {
                    element.removeClass('hide');
                });

                $rootScope.$on('$stateChangeSuccess', function() {
                    element.addClass('hide');
                    $('body').removeClass('page-on-load');
                    //Layout.setSidebarMenuActiveLink('match');

                    setTimeout(function () {
                        Fabs.scrollTop();
                    }, $rootScope.settings.layout.pageAutoScrollOnLoad);
                });

                $rootScope.$on('$stateNotFound', function() {
                    element.addClass('hide');
                });

                $rootScope.$on('$stateChangeError', function() {
                    element.addClass('hide');
                });
            }
        };
    }
]);


ysp.directive('a', function() {
    return {
        restrict: 'E',
        link: function(scope, elem, attrs) {
            if (attrs.ngClick || attrs.href === '' || attrs.href === '#') {
                elem.on('click', function(e) {
                    e.preventDefault();
                });
            }
        }
    };
});

ysp.directive('dropdownMenuHover', function () {
    return {
        link: function (scope, elem) {
            elem.dropdownHover();
        }
    };
});


ysp.run(["$rootScope", "settings", "$state", function ($rootScope, settings, $state) {
    $rootScope.$state = $state;
}]);


jQuery.prototype.serializeObject=function(){
    var a,o,h,i,e;
    a=this.serializeArray();
    o={};
    h=o.hasOwnProperty;
    for(i=0;i<a.length;i++){
        e=a[i];
        if(!h.call(o,e.name)){
            o[e.name]=e.value;
        }
    }
    return o;
};
/*
function app_money_ch(data){
    if(data == undefined || data == null){
        return"0.00";
    }
    data = data + "";
    if(data.length < 4){
        return data + ".00";
    }
    var num = data.length-2;
    if(data.substring(num-1,num) == "."){
        return data;
    }
    num = (data.length % 3);
    var mon = "";
    if(num != 0){
        mon = data.substring(0, num);
        mon = mon + ',';
    }
    var j =1;
    for(var i = num; i < data.length; i++){

        mon = mon + data.substring(i, i+1)
        if(j%3 == 0 && j!=(data.length-num)){
            mon = mon + ',';
        }
        j++;
    }
    return mon+".00";
}

function app_date_ch(data){
    if(data == undefined){
        return;
    }
    if(data == null){
        return "";
    }
    var num1 = data.substring(4,5);
    var num2 = data.substring(7,8);
    if(data.length==10 && num1=="-" && num2=="-"){
        return data;
    }
    var dat = "";
    if(data.length == 8){
        dat = data.substring(0,4);
        dat += '-';
        var month = data.substring(4,6);
        if(month >= 1 && month <= 12){
            dat += month;
        }else{
            alert("请输入合法日期");
            return "";
        }
        dat += '-';
        var day = data.substring(6,8);
        if(day >= 1 && day <= 31){
            dat += day;
        }else{
            alert("请输入合法日期");
            return "";
        }
    }else{
        alert("请输入合法日期");
    }
    return dat;
}

*/

var choose_branch_type = function(elem, typeCode, typeName,typePage){
   angular.element($(elem)).scope().choose_branch_type(typeCode, typeName,typePage);
}

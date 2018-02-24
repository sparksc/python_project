ysp.controller('customerCompanyController', function($scope,store, $rootScope,customerCompanyService,reportService){
    $scope.modal_data={};
    $scope.dict={};
	$scope.dataList = {};
        $scope.displayInfo= function(tabName){
        $scope.display_info = tabName;
    };
    $scope.customer_list=[];
    $scope.query_customer = function(){
        var data = $("#quick_sidebar_cust_query").val();
    };
    //  Search
    $scope.List1 = ['项目', '行次', '期初数', '期末数'];
    $scope.List2 = ['项目', '行次', '本月数', '本年累计数'];
    $scope.List3 = ['项目', '行次', '金额'];
    $scope.List4 = ['项目', '行次', '指标值（比率：%）', '行业标准值'];
     
	 $scope.report_datalist1=[];
	$scope.query_report_data = function(){
		var data = $("#report_record").val();
		reportService.query_report_data(data).success(function(resp){
			$scope.report_datalist1=resp.data;
		});
	};
    $scope.init = function(){
        $scope.display_info= "companyInformation";
         $scope.query_customer();
		 $scope.query_report_data();
    };
    $scope.init();
    /* 财务报表 */
    $scope.Listreport = ['报表年月', '报表类型', '删除' , '查看',  '上传'];
	$scope.upload = function(record_id,report_id){
       // $('#file_btn').click(function(){
           var token = store.getSession("token");
           var file = $('#insertFileForm').find('input[name="'+record_id+'"]').prop('files');
            var form = new FormData();
            form.append('file',file[0]);
            form.append('record_id', record_id);
            form.append('report_id', report_id);
            $.ajax({
                type: "POST",
                url : base_url+"/reports/upload/",
                data: form,
                processData: false,
                contentType: false,
                beforeSend: function(request) {
                    request.setRequestHeader("x-session-token", token);
                },
                success: function(msg){
                    alert("上传成功");
                }
            });
      //  });
    };
    //计算
	$scope.compute = function(){

        alert("计算完成");
        }

    $scope.formual_eval = function(value){
        return eval(value);
    }
	//添加数据
	$scope.updatereadonly = function(){
	$scope.disabled_flag = true;
	$('input[name=start]').attr("readonly","readonly");
 	$('input[name=end]').attr("readonly","readonly");
 	alert("保存成功"); 
		 reportService.updatereadonly({'report_lists':$scope.rl});
	};
	//暂存数据
	$scope.temporary_storage = function(){
	$('input[name=start]').attr("readonly","readonly");
 	$('input[name=end]').attr("readonly","readonly");
 	alert("暂存成功"); 
	};
	//修改
	$scope.disabled_flag=true;
	$scope.movereadonly =function(){ 
	$scope.disabled_flag = false;
	$('input[name=start]').removeAttr("readonly");
 	$('input[name=end]').removeAttr("readonly");
}
    //保存report_data
    $scope.save_report_record = function(){
        var  ty=$scope.modal_data.report_period;
        var  num=$scope.modal_data.year_month;
        if( ty == null){
            alert("请输入报表类型");
            return false;
        }
        if(num == null){
            alert("请输入报表年月");
           return false;
        }
            regtextNum0=/^\d{6}$/;
        if(num.search(regtextNum0) ==-1){
            alert("报表年月位6位数字(例如：201411)");
            return false;
        }
        num1=num.substring(num.length-6, num.length-2);
        num2=num.substring(num.length-2, num.length);
        if(ty=="月报"){
            regtextNum=/^01|02|03|04|05|06|07|08|09|10|11|12$/;
            if(num2.search(regtextNum) ==-1){
                alert("月份为（01-12）");
                return false;
            }else{
                $scope.modal_data.company_id = $scope.customer.id;
                var myDate=new Date();
                report_date= myDate.toLocaleDateString(); //获取当前日期
                $scope.modal_data.report_date = report_date;
                reportService.save_report_record($scope.modal_data);
                alert("新增成功");
            }
        }
        if(ty=="季报"){
            regtextNum1=/^03|06|09|12$/;
            if(num2.search(regtextNum1) ==-1){
                alert("季报的月份为（03,06,09,12）");
                return false;
            }else{
                $scope.modal_data.company_id = $scope.customer.id;
                var myDate=new Date();
                report_date= myDate.toLocaleDateString(); //获取当前日期
                $scope.modal_data.report_date = report_date;
                reportService.save_report_record($scope.modal_data);
                alert("新增成功");
            }
        }
        if(ty=="半年报"){
            regtextNum2=/^06|12$/;
            if(num2.search(regtextNum2) ==-1){
                alert("半年报的月份为（06,12）");
                return false;
            }else{
                $scope.modal_data.company_id = $scope.customer.id;
                var myDate=new Date();
                report_date= myDate.toLocaleDateString(); //获取当前日期
                $scope.modal_data.report_date = report_date;
                reportService.save_report_record($scope.modal_data);
                alert("新增成功");
            }
        }if(ty=="年报"){
            regtextNum3=/^12$/;
            if(num2.search(regtextNum3) ==-1){
                alert("年报的月份位（12）");
                return false;
            }else{
                $scope.modal_data.company_id = $scope.customer.id;
                var myDate=new Date();
                report_date= myDate.toLocaleDateString(); //获取当前日期
                $scope.modal_data.report_date = report_date;
                reportService.save_report_record($scope.modal_data);
                alert("新增成功");
            }
        }

    };
    $scope.find_statement = function(record_id){
        var tabName="财务报表";
        $rootScope.forward(tabName,'views/customer/company/findstatement.html',{'record_id':record_id});
    };
    $scope.delete_report_record = function(id,company_id){
    
	if(!confirm("确认要删除？")){ 
         window.event.returnValue = false; 
		 
    }else{
	reportService.delete_report_record(id).success(function(){
			  $scope.query_report_record(company_id)
        });
	alert("删除成功");}
		

		
    };
    $scope.report_datalist=[];
    $scope.query_report_record = function(id){
        var data = $("#report_record").val();
        //查询report_data
        reportService.query_report_record(id,data).success(function(resp){
              $scope.report_datalist=resp.data;
        });
    };
    $scope.displayInfo= function(tabName){
        $scope.display_info = tabName;
    };
    $scope.customer_list=[];
    $scope.query_customer = function(){
        var data = $("#quick_sidebar_cust_query").val();
    };

    $scope.init = function(){
        return;
        $scope.display_info= "companyInformation";
        $scope.query_customer();

    };
    $scope.init();
    //关联个人
    $scope.associPerson = function(associate,party_id){
    var tabName = '个人客户'
        var htmlContent = '<div ng-include="'+'\'views/customer/person/pre_add.html' +'\'"></div>'; 
        var tab_id = $rootScope.addTab(tabName, htmlContent, {}, true, {'associate':associate,'party_id':party_id});   
    }


    //关联对公
    $scope.associCompany = function(associate,party_id){
        var tabName = '对公客户'; 
        var htmlContent = '<div ng-include="'+'\'views/customer/company/com_add.html' +'\'"></div>';
        var tab_id = $rootScope.addTab(tabName, htmlContent, {}, true, {'associate':associate,'party_id':party_id}); 
        tabScope = angular.element(document.getElementById('tab_'+ tab_id + '_content')).scope();
    }
   
})
ysp.controller('reportsController', function($scope, $compile, creditService,userService,reportService,$rootScope){
    /*tab动态增加功能*/
    userService.query_groups().success(function(resp){
        $scope.user_groups=resp.groups;
/*         $scope.init1(); */
    });;

    $scope.subTabIndex = 0;
    $scope.currIndex = 0;
    $scope.subTab = {}; //check if open the same tab

    var defaultEvent = {
        'on':function(){
            return true;
        }
    };
    $scope.addSubTab = function(tabName, htmlContent, eventObj, autoFocus){
        var t = new Object();
        t.index = $scope.subTabIndex;
        t.tabName = tabName;
        t.htmlContent = htmlContent;
        t.createEvent = eventObj.create? eventObj.create:defaultEvent;
        t.closeEvent = eventObj.close? eventObj.close:defaultEvent;
        t.focusEvent = eventObj.focus? eventObj.focus:defaultEvent;
        t.loseFocusEvent = eventObj.loseFocus? eventObj.loseFocus:defaultEvent;

        $scope.subTab[t.index] = t;
        var tabContentId = $scope.subTabCreate(t);
        $scope.subTabIndex = $scope.subTabIndex + 1;

        if (autoFocus == true){
            $scope.changeFocus(t.index);
        }
        return t.index;
    };
     $scope.subTabCreate = function(tabObj){
        succ_flag = $scope.subTab[tabObj.index].createEvent.on();
            var tabId = 'loan_tab_' + $scope.$id + '_' + tabObj.index;
            var tabName = tabObj.tabName;
            var tabContentId = tabId + '_content';
            var tabHtml = '<li id="'+ tabId +'" ng-click="changeFocus('+tabObj.index+')"> <a href="#'+ tabContentId +'" data-toggle="tab">'+ tabName +'</a></li>';
            var tabContentHtml = '<div class="tab-pane" id="'+ tabContentId +'"></div>';
            baseScope = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent1']").scope();
            scope = baseScope.$new();
            var tabTemplate = angular.element(tabHtml);
            var tabElement = $compile(tabTemplate)(scope);
            var contentTemplate = angular.element(tabObj.htmlContent);
            var contentElement = $compile(contentTemplate)(scope);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("ul[name='tab']").append(tabElement);
            angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("div[name='tabContent1']").append(tabContentHtml);
            angular.element(document.getElementById(tabContentId)).append(contentElement);
            return tabContentId;
    };
    $scope.changeFocus = function(focus_tabId){
        $scope.subTabLoseFocus($scope.currIndex); 
        $scope.subTabFocus(focus_tabId);
        $scope.currIndex = focus_tabId;
    };
	 $scope.subTabLoseFocus = function(index){
        succ_flag = $scope.subTab[index].loseFocusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).removeClass("ng-scope active").addClass("ng-scope");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane active").addClass("tab-pane");
        }else{
            alert("失焦失败！");
        }
    };
    $scope.subTabFocus = function(index){
        succ_flag = $scope.subTab[index].focusEvent.on();
        if(succ_flag==true){
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index)).addClass("active");
            angular.element(document.getElementById('loan_tab_'+ $scope.$id + '_' + index + '_content')).removeClass("tab-pane").addClass("tab-pane active");
        }else{
            alert("聚焦失败！");
        }
    }; 
        $scope.init1 = function(){ 
        $scope.rl=[];
        $scope.query_report_items = function(record_id) {
            var data = $("#reportbalanceSheet").val();
            reportService.query_report_items($scope.record_id, data).success(function (resp) {
                $scope.rl = resp.data;
                $scope.showData();
                $scope.dc = {};
                for (i in resp.data) {
                    r = resp.data[i];
                    $scope.dc[r[3]] = i;
                }
            });
        }
			
            $scope.showData = function() {
                var rl = $scope.rl;
                $scope.models = $scope.rl;
                //格式化金额
                  $scope.formatNum = function(str) {
                      if (!(!str)) {
                          var newStr = "";
                          var count = 0;
                          str = parseFloat(str).toFixed(2);
                          str = parseFloat(str).toLocaleString();

                          if (str.indexOf('.') == -1) {
                              str = str + ".0";
                          }
                          return str;

                      } else {
                          str = 0.0;
                          return str;
                      }
                  }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 1 && r[3] < 2000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\"  ng-model=\"rl[" + d + "][4]\"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#balanceSheet').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 1 && r[3] >= 2000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}}\"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#balanceSheet1').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 9 && r[3] < 73000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#BbalanceSheet').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 9 && r[3] >= 73000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}}\"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#BbalanceSheet1').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 6 && r[3] < 42000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#NbalanceSheet').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 6 && r[3] >= 42000000) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#NbalanceSheet1').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 2) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
//                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
//                            tr_html = tr_html +"<td  style=\"color:#0000FF;\">" + "</td>";
//                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
//                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
//                            tr_html = tr_html +"<td  style=\"color:#0000FF;\">" + "</td>";
//                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#incomeStatement').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 7) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
//                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
//                            tr_html = tr_html +"<td  style=\"color:#0000FF;\">" + "</td>";
//                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
//                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
//                            tr_html = tr_html +"<td  style=\"color:#0000FF;\">" + "</td>";
//                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"end\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][5]=" + r[11] + ")}} \"   /></td>";
                        }

                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#NincomeStatement').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 3) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#cashFlowStatement').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 8) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#NcashFlowStatement').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 10) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#incomeSpending').append(contentElement);
                    }
                }
                for (var d in rl) {
                    var r = rl[d]
                    if (r[1] == 4) {
                        var tr_html = "<tr>";
                        tr_html = tr_html + "<td  style=\"color:#0000FF;display:none;\" >" + r[0] + "</td>" +
                            "<td  style=\"color:#0000FF;display:none;\">" + r[3] + "</td>";
                        if (r[3] % 10000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        if (r[3] % 10000 != 0 && r[3] % 100 != 0 && r[3] % 10 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + r[2] + "</td>";
                        }
                        tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + d + "</td>";
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }
                        if (r[10] == null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][4] \"   /></td>";
                        }
                        if (r[10] != null) {
                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" value=\"{{formatNum(rl[" + d + "][4]=" + r[10] + ")}} \"   /></td>";
                        }
                        if (r[3] % 10000 == 0 && r[3] % 100000 != 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">" + "</td>";
                        }
                        if (r[3] % 10000 != 0 || r[3] % 100000 == 0) {
                            tr_html = tr_html + "<td  style=\"color:#0000FF;\">";
                        }

                            tr_html = tr_html + "<input  name=\"start\" type=\"text\" readonly=\"readonly\" ng-model=\"rl[" + d + "][5] \"   /></td>";


                        tr_html = tr_html + "</tr>"
                        var contentTemplate = angular.element(tr_html);
                        var contentElement = $compile(contentTemplate)($scope);
                        angular.element(document.getElementById('tab_' + $scope.tabId + '_content')).find('#financialIndex').append(contentElement);
                    }
                }
            }

        console.log("进入财务报表初始化");
        $scope.addSubTab('资产负债表', '<div ng-include="'+'\'views/customer/company/reports/balanceSheet.html' +'\'"></div>', {}, false);
        $scope.addSubTab('资产负债表（新）', '<div ng-include="'+'\'views/customer/company/reports/NbalanceSheet.html' +'\'"></div>', {}, false);
        $scope.addSubTab('损益表', '<div ng-include="'+'\'views/customer/company/reports/incomeStatement.html' +'\'"></div>', {}, false);
        $scope.addSubTab('损益表（新）', '<div ng-include="'+'\'views/customer/company/reports/NincomeStatement.html' +'\'"></div>', {}, false);
        $scope.addSubTab('现金流量表', '<div ng-include="'+'\'views/customer/company/reports/cashFlowStatement.html' +'\'"></div>', {}, false);
        $scope.addSubTab('现金流量表（新）', '<div ng-include="'+'\'views/customer/company/reports/NcashFlowStatement.html' +'\'"></div>', {}, false);
        $scope.addSubTab('资产负债表（事业单位）', '<div ng-include="'+'\'views/customer/company/reports/BbalanceSheet.html' +'\'"></div>', {}, false);
        $scope.addSubTab('收入支出表（事业单位）', '<div ng-include="'+'\'views/customer/company/reports/incomeSpending.html' +'\'"></div>', {}, false);
        $scope.addSubTab('财务指标表', '<div ng-include="'+'\'views/customer/company/reports/financialIndex.html' +'\'"></div>', {}, false);
    };
    $scope.init1();
	$scope.query_report_items();
    $scope.subTabFocus(0);
}) 
.service('customerCompanyService', function($http){
})
.service('reportService', function($http){
return {
            query_report_items:function(id,data){
                return $http.get(base_url+'/reports/'+id);
            },
            save_report_record:function(data){
                        return $http.post(base_url+'/reports/save/',data);
            },
            query_report_record:function(id,data){
					return $http.get(base_url+'/reports/query?company_id='+id,data);
			},
			delete_report_record:function(id){
					return $http.get(base_url+'/reports/delete?id='+id);
			},
			updatereadonly:function(data){
					return $http.post(base_url+'/reports/updatereadonly/',data);
			},
			upload:function(data){
					return $http.post(base_url+'/reports/upload/',data);
			},
			query_report_data:function(data){
					return $http.get(base_url+'/reports/querydata/',data);
			},
			compute:function(data){
					return $http.post(base_url+'/reports/compute/',data);
			}
			
        }
})
//基本信息
.controller('companyInformationController', function($scope, companyInformationService, industryService, store){
    $scope.customer_id = null;
    $scope.customer={};
    $scope.money={};
    $scope.disabled_flag=true;
    $scope.credit_disabled_flag=true;
    $scope.save = function(){
        $scope.disabled_flag = true;
        $scope.credit_disabled_flag=true; //三证
        if($scope.customer_id){
            if($scope.industry_top && $scope.industry_big && $scope.industry_mid && $scope.industry_small){
                    $scope.customer.industry_class=$scope.industry_top;
                    $scope.customer.industry_large_class=$scope.industry_big;
                    $scope.customer.industry_mid_class=$scope.industry_mid;
                    $scope.customer.industry_small_class = $scope.industry_small;
            }
            companyInformationService.update($scope.customer_id, $scope.customer).success(function(resp){
                $scope.query($scope.customer_id);
                alert('操作成功！')
            });
        }
    };

    $scope.submit = function(d){
      if(!d){
        alert('填写完整信息')
      }else{
        $scope.disabled_flag = true;
        $scope.credit_disabled_flag=true;
        if($scope.customer_id){
            $scope.save();
        }else{
            companyInformationService.create($scope.customer).success(function(resp){
            });
        }
      }
    };
        
    $scope.edit = function(){
        //alert($scope.industryT_top);
        $scope.disabled_flag = false;
        industryService.query_cust($scope.customer.id).success(function(resp){
           console.log(resp.data)
           var ls = resp.data;
           if(ls.length == 4 && ls.indexOf(null) == -1){ 
               showIndustry(ls);
           }    
           else{
               $scope.initIndustry();
           }
        })
        if($scope.customer.org_credit_cert){
            $scope.credit_disabled_flag=true;
        }else{
            $scope.credit_disabled_flag=false;
        }
    }

    $scope.clear = function(){
        $scope.customer={}; 
    };

    $scope.query = function(customer_id){
        companyInformationService.query(customer_id).success(function(resp){
            $scope.customer = resp.data;
            $scope.money.hold_stock_amount =  app_money_char($scope.customer.hold_stock_amount)[1];
            $scope.money.asset_amount = app_money_char($scope.customer.asset_amount)[1];
            $scope.money.liability_amount = app_money_char($scope.customer.liability_amount)[1];
            $scope.money.reg_amount = app_money_char($scope.customer.reg_amount)[1];
            $scope.money.paid_amount = app_money_char($scope.customer.paid_amount)[1];
            console.log($scope.customer.industry_large_class)
            if($scope.customer != null){
                $scope.industryT_top = $scope.customer.industry_class;
                $scope.industry_big = $scope.customer.industry_large_class;
                $scope.industry_mid = $scope.customer.industry_mid_class;
                $scope.industry_small = $scope.customer.industry_small_class;
            }else{
                industryService.query_cust($scope.customer.id).success(function(resp){
                    var ls = resp.data;
                    if(ls.length == 4 && ls.indexOf(null) == -1){
                        showIndustry(ls);
                    }else{
                        $scope.initIndustry();
                    }
                });
            }
            if($scope.customer && $scope.customer.register_branch == null){
                $scope.customer.register_branch = store.getSession("branch_code")+ '-' + store.getSession("branch_name");
                $scope.customer.register_name = store.getSession("user_name")+ '-' +store.getSession("name");
             }
        });
    }

    $scope.initIndustry = function(){
       console.log('nknknkjnkjnkjnkjnkjnjk');
       $scope.industry_top=null;
       $scope.industry_big=null;
       $scope.industry_mid=null;
       $scope.industry_small=null;
       $scope.industry_topList=[];
       industryService.query('_').success(function(resp){
           $scope.industry_topList = resp.data;
       }); 
    
    }   
    //$scope.initIndustry();   
    function showIndustry(ls){
        industryService.query('_').success(function(resp){
            console.log(resp.data);
            $scope.industry_topList = resp.data;
            $scope.industryT_top= null;
            industryService.query(ls[0].substring(0,1)+'__').success(function(resp){
                console.log(resp.data);
                $scope.industry_bigList = resp.data;
                $scope.industry_big=null;
                industryService.query(ls[1].substring(0,3)+'_').success(function(resp){
                    console.log(resp.data);
                    $scope.industry_midList = resp.data;
                    $scope.industry_mid=null;
                    industryService.query(ls[2].substring(0,4)+'_').success(function(resp){
                        console.log(resp.data);
                        $scope.industry_smallList = resp.data;
                        $scope.industry_small=null;
                        window.setTimeout(function(){
                        $scope.industryT_top= ls[0];
                        $scope.industry_big=ls[1];
                        $scope.industry_mid=ls[2];
                        $scope.industry_small=ls[3];
                        },500);
                    });
                });

            });

        });
    }
    $scope.industry_select=function(para,which){
       if (which == 'big'){
            industryService.query(para.substring(0,1)+'__').success(function(resp){
                $scope.industry_bigList = resp.data;
                $scope.industry_top=para;
                $scope.industry_big=null;
                $scope.industry_mid=null;
                $scope.industry_small=null;
            });
            $scope.industry_midList = null;
            $scope.industry_smallList=null;
        }else if(which == 'mid'){
            industryService.query(para.substring(0,3)+'_').success(function(resp){
                $scope.industry_midList = resp.data;
                $scope.industry_big=para;
                $scope.industry_mid=null;
                $scope.industry_small=null;
            });
            $scope.industry_smallList=null;
        }else if(which == 'small'){
            industryService.query(para.substring(0,4)+'_').success(function(resp){
                $scope.industry_smallList = resp.data;
                $scope.industry_mid=para;
                $scope.industry_small=null;
             });
        }else{
            $scope.industry_small=para;
        }
    }
        
    //金额格式转换
    var list;
    $scope.hold_stock_amount = function(data){
        list = app_money_char(data);
        $scope.customer.hold_stock_amount = list[0];
        $scope.money.hold_stock_amount = list[1];
    }
    $scope.asset_amount = function(data){
        list = app_money_char(data);
        $scope.customer.asset_amount = list[0];
        $scope.money.asset_amount = list[1];
    }
    $scope.liability_amount = function(data){
        list = app_money_char(data);
        $scope.customer.liability_amount = list[0];
        $scope.money.liability_amount = list[1];
    }
    $scope.reg_amount = function(data){
        list = app_money_char(data);
        $scope.customer.reg_amount = list[0];
        $scope.money.reg_amount = list[1];
    }
    $scope.paid_amount = function(data){
        list = app_money_char(data);
        $scope.customer.paid_amount = list[0];
        $scope.money.paid_amount = list[1];
    }
    //日期格式转换
    $scope.reg_thru_date = function(){
        $scope.customer.reg_thru_date = app_date_ch($scope.customer.reg_thru_date);
    }
    $scope.last_check_date = function(){
        $scope.customer.last_check_date = app_date_ch($scope.customer.last_check_date);
    }
    $scope.out_rating_date = function(){
        $scope.customer.out_rating_date = app_date_ch($scope.customer.out_rating_date);
    }
    $scope.special_start_date =function(){
        $scope.customer.special_start_date = app_date_ch($scope.customer.special_start_date);
    }
    $scope.special_thru_date = function(){
        $scope.customer.special_thru_date = app_date_ch($scope.customer.special_thru_date);
    }
    $scope.init_account_date = function(){
        $scope.customer.init_account_date = app_date_ch($scope.customer.init_account_date);
    }
    $scope.init_loan_date = function(){
        $scope.customer.init_loan_date = app_date_ch($scope.customer.init_loan_date);
    }
    $scope.register_date = function(){
        $scope.customer.register_date = app_date_ch($scope.customer.register_date);
    }
    $scope.company_reg_date = function(){
        $scope.customer.company_reg_date =app_date_ch($scope.customer.company_reg_date);
    }

    // 新增或是查看
    if ($scope.$parent.customer != undefined){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id);
    }else{
        $scope.disabled_flag=false;
        if($scope.customer.org_credit_cert){
            $scope.credit_disabled_flag=true;
        }else{
            $scope.credit_disabled_flag=false;
        }  
    }

})

.service('companyInformationService', function($http){
    return {
        create:function(data){
            return $http.post(base_url+'/customers/company',data)
        },
        query:function(customer_id){
            return $http.get(base_url+'/customers/company/'+customer_id)
        },
        update:function(customer_id, data){
            return $http.put(base_url+'/customers/company/'+customer_id, data)
        },
        query_companys:function(custNo, custName, certType, certNo){
            return $http.get(base_url+'/customers/companys/?custNo='+custNo+'&custName='+custName+'&certType='+certType+'&certNo='+certNo)
        },
        query_assos:function(customer_id,asso){
            return $http.get(base_url+'/customers/assos/'+customer_id+'?asso='+asso)
        },
        update_socialInsu:function(customer_id,data){
            return $http.put(base_url+'/customers/socialInsu/'+customer_id,data)
        },
        update_principal:function(customer_id,data){
            return $http.put(base_url+'/customers/principal/'+customer_id,data)
        },
        update_contCom:function(customer_id,data){
            return $http.put(base_url+'/customers/contCom/'+customer_id,data)
        },
        update_invesMang:function(customer_id,data){
            return $http.put(base_url+'/customers/invesMang/'+customer_id,data)
        },
        update_capitStr:function(customer_id,data){
            return $http.put(base_url+'/customers/capitStr/'+customer_id,data)
        },
        update_clientCurr:function(customer_id,data){
            return $http.put(base_url+'/customers/clientCurr/'+customer_id,data)
        },
	update_companyStruct:function(customer_id,data){
            return $http.put(base_url+'/customers/companyStruct/update'+customer_id,data)
	},
	create_companyStruct:function(customer_id, data){
	    return $http.post(base_url+'/customers/companyStruct/create'+customer_id,data)
	},
	query_companyStruct:function(customer_id){
	    return $http.get(base_url+'/customers/companyStruct/create'+customer_id)
	},
    }
})


//董事会成员
.controller('socialInsuranceController', function($scope,companyInformationService){
    $scope.table_head=['姓名', '证件号码', '证件类型'];
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];
    $scope.new_record = function(){
        $scope.modal_title='董事会成员信息新增';
    };

    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
       $scope.disabled_flag = false;
       $scope.form_data = data;
    }
    $scope.display_record = function(index){
        $scope.modal_title='董事会成员信息查看';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#socialInsurance");
    };
    
    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             $scope.table_data = resp.data;
        });
    }
    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'socialInsurance');
    }
    
    $scope.save_data = function(){
        $scope.disabled_flag = true;
        if($scope.customer_id){
            companyInformationService.update_socialInsu($scope.customer_id, $scope.form_data).success(function(resp){
                companyInformationService.query_assos($scope.customer_id, 'socialInsurance').success(function(resp){
                    alert('保存成功');
                });
            });
        }
    }

    $scope.refresh = function(){
        companyInformationService.query_assos($scope.customer_id, 'socialInsurance').success(function(resp){
            $scope.table_data = resp.data;
        });
    }

    // 关联客户打开
    $scope.customer_tab={};
    var eventObj = {
        'create':'',
        'focus':'',
        'loseFocus':'',
        'close':{
            'message': "关闭页面提示",
            'on':function(){
                alert(this.message);
                return true;
            },
        }
    }

})

//主要负责人
.controller('principalController', function($scope,companyInformationService){
    $scope.table_head=['姓名', '证件号码', '负责类型'];
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];
    $scope.new_record = function(){
        $scope.modal_title='主要负责人信息新增';
    };
    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
       $scope.disabled_flag = false;
       $scope.form_data = data;
    }

    $scope.display_record = function(index){
        $scope.modal_title='主要负责人信息查看';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#principal");
    };

    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             $scope.table_data = resp.data;
        });
    }
    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'principal');
    }

    $scope.save_data = function(form_data){
        $scope.disabled_flag = true;
        if($scope.customer_id){
            companyInformationService.update_principal($scope.customer_id, $scope.form_data).success(function(resp){
                companyInformationService.query_assos($scope.customer_id, 'principal').success(function(resp){
                    alert('保存成功');
                });
            });
        }
    }
    $scope.refresh = function(){
        companyInformationService.query_assos($scope.customer_id, 'principal').success(function(resp){
            $scope.table_data = resp.data;
        });
    }

    // 关联客户打开
    $scope.customer_tab={};
    var eventObj = {
        'create':'',
        'focus':'',
        'loseFocus':'',
        'close':{
            'message': "关闭页面提示",
            'on':function(){
                alert(this.message);
                return true;
            },
        }
    }
})

//公司信息
.controller('controlledCompanyController', function($scope,companyInformationService){
    $scope.table_head=['公司代码', '公司名称','公司结构类型', '负责人名称', '联系人'];
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];

    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
       $scope.disabled_flag = false;     
       $scope.form_data = data;
    }
    $scope.display_record = function(index){
        $scope.modal_title='公司结构信息';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#controlledCompany");
    };
    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             $scope.table_data = resp.data;
        });
    }
    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'controlledCompany');
    }

    $scope.save_data = function(form_data){
        $scope.disabled_flag = true;
        if($scope.customer_id){
            companyInformationService.update_contCom($scope.customer_id, $scope.form_data).success(function(resp){
                companyInformationService.query_assos($scope.customer_id, 'controlledCompany').success(function(resp){
                    alert('保存成功');
                });
            });
        }
    }
    $scope.refresh = function(){
        companyInformationService.query_assos($scope.customer_id, 'controlledCompany').success(function(resp){
            $scope.table_data = resp.data;
        });
    }

})

//投资联营
.controller('investmentManagementController', function($scope,companyInformationService){
    $scope.table_head=['被投资客户代码', '被投资客户名称', '实际投资金额(元)', '占股权比例', '经营范围'];
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];
    $scope.new_record = function(){
        $scope.modal_title='投资联营';
    };

    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
       $scope.disabled_flag = false;     
       $scope.form_data = data;
    }
    $scope.display_record = function(index){
        $scope.modal_title='投资联营';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#investmentManagement");
    };
    $scope.display_customer = function(customer_in){
        
    };
    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             $scope.table_data = resp.data;
            // $scope.viewlittle()
        });
    }
    $scope.save_data = function(form_data){
        $scope.disabled_flag = true;
        if($scope.customer_id){
            companyInformationService.update_invesMang($scope.customer_id, $scope.form_data).success(function(resp){
                companyInformationService.query_assos($scope.customer_id, 'investmentManagement').success(function(resp){
                    alert('保存成功');
                }); 
            }); 
        }   
    }
    $scope.refresh = function(){
        companyInformationService.query_assos($scope.customer_id, 'investmentManagement').success(function(resp){
            $scope.table_data = resp.data;
        });
    }

    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'investmentManagement');
    }

})
//客户履历
.controller('clientCurriculumController', function($scope,companyInformationService){
    $scope.table_head=['事件名称', '事件类型', '发生日期', '曝光单位'];
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];
    $scope.new_record = function(){
        $scope.modal_title='客户履历';
    };

    $scope.view = function(selector){
       angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
       $scope.disabled_flag = false;
       $scope.form_data = data;
    }
    $scope.display_record = function(index){
        $scope.modal_title='客户履历';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#clientCurriculum");
    };
    $scope.display_customer = function(customer_in){

    };
    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             console.log('resp.data');
             console.log(resp.data);
             $scope.table_data = resp.data;
        });
    }
    $scope.save_data = function(form_data){
        $scope.disabled_flag = true;
        if($scope.customer_id){
            companyInformationService.update_clientCurr($scope.customer_id, $scope.form_data).success(function(resp){
                companyInformationService.query_assos($scope.customer_id, 'clientCurriculum').success(function(resp){
                    alert('保存成功');
                });
            });
        }
    }
    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'clientCurriculum');
    }
}
)
//相关文档
.controller('otherAssetController', function($scope){
    $scope.table_head=['文件标题', '文件类型', '重要级别', '编制单位', '编制日期', '附件内容'];
    $scope.table_data=[
        {
        }
    ]
})

//资本组成结构
.controller('capitalStructureController', function($scope,companyInformationService){
    $scope.table_head=['序号', '股东名称', '货币(元)', '实物(元)', '净资产(元)', '其他(元)', '合计(元)', '实缴注册资本(元)'];
    $scope.money = {};
    $scope.form_data = {};
    $scope.class1=[{'id':1,'value':'A-nnn'},{},];
    $scope.new_record = function(){
        $scope.modal_title='资本组成结构';
    };
    
    $scope.view = function(selector){
        angular.element(selector).find("input,select,textarea").attr("ng-disabled","true");
    }
    $scope.view_data = function(data){
        $scope.disabled_flag = false;
        $scope.form_data = {};
        $scope.form_data = data;
        $scope.money.invest_cur = app_money_char($scope.form_data.capitalStructure.invest_cur)[1];
        $scope.money.invest_pract = app_money_char($scope.form_data.capitalStructure.invest_pract)[1];
        $scope.money.invest_asset = app_money_char($scope.form_data.capitalStructure.invest_asset)[1];
        $scope.money.invest_other = app_money_char($scope.form_data.capitalStructure.invest_other)[1];
        $scope.money.fact_amount = app_money_char($scope.form_data.capitalStructure.fact_amount)[1];
        $scope.money.invest_amount = app_money_char($scope.form_data.capitalStructure.invest_amount)[1];
    }
    $scope.display_record = function(index){
        $scope.modal_title='资本组成结构';
        $scope.modal_data = $scope.table_data[index];
        $scope.view("#capitalStructure");
    };
    $scope.display_customer = function(customer_in){
        
    };
    var list;
    $scope.money_invest_cur = function(data){
        list = app_money_char(data);
        $scope.form_data.capitalStructure.invest_cur = list[0];
        $scope.money.invest_cur = list[1];
        $scope.amount_add();
    }
    $scope.money_invest_pract = function(data){
        list = app_money_char(data);
        $scope.form_data.capitalStructure.invest_pract = list[0];
        $scope.money.invest_pract = list[1]; 
        $scope.amount_add();
    }
    $scope.money_invest_asset = function(data){
        list = app_money_char(data);
        $scope.form_data.capitalStructure.invest_asset = list[0];
        $scope.money.invest_asset = list[1]; 
        $scope.amount_add();
    }
    $scope.money_invest_other = function(data){
        list = app_money_char(data);
        $scope.form_data.capitalStructure.invest_other = list[0];
        $scope.money.invest_other = list[1];
        $scope.amount_add();
    }
    $scope.money_fact_amount = function(data){
        list = app_money_char(data);
        $scope.form_data.capitalStructure.fact_amount = list[0];
        $scope.money.fact_amount = list[1];
        $scope.invest_percentage($scope.form_data.capitalStructure.fact_amount);
    }
    $scope.query = function(customer_id,asso){
        companyInformationService.query_assos(customer_id,asso).success(function(resp){
             $scope.table_data = resp.data;
        });
    }
    
    $scope.submit = function(v){
        if(v){
            $scope.disabled_flag = true;
            if($scope.customer_id){
                companyInformationService.update_capitStr($scope.customer_id, $scope.form_data).success(function(resp){
                    alert('保存成功！')
                    companyInformationService.query_assos($scope.customer_id, 'capitalStructure').success(function(resp){
                    });
                });
            }
        }
    }
    //刷新
    $scope.refresh = function(){
        companyInformationService.query_assos($scope.customer_id, 'capitalStructure').success(function(resp){
            $scope.table_data = resp.data;
        });
    }
    
    if ($scope.$parent.customer){
        $scope.customer_id = $scope.$parent.customer.id;
        $scope.query($scope.customer_id,'capitalStructure');
    }

    $scope.amount_add = function(){
        var invest_cur = parseInt('0');
        var invest_pract = parseInt('0');
        var invest_asset = parseInt('0');
        var invest_other = parseInt('0');
        if($scope.form_data.capitalStructure.invest_cur != null && $scope.form_data.capitalStructure.invest_cur != ""){
            invest_cur = parseInt($scope.form_data.capitalStructure.invest_cur);
        }
        if($scope.form_data.capitalStructure.invest_pract != null && $scope.form_data.capitalStructure.invest_pract != ""){
             
            invest_pract = parseInt($scope.form_data.capitalStructure.invest_pract);
        }
        if($scope.form_data.capitalStructure.invest_asset != null && $scope.form_data.capitalStructure.invest_asset != ""){
            invest_asset = parseInt($scope.form_data.capitalStructure.invest_asset);
        }
        if($scope.form_data.capitalStructure.invest_other != null && $scope.form_data.capitalStructure.invest_other != ""){
            invest_other = parseInt($scope.form_data.capitalStructure.invest_other);
        }
        var add = parseInt('0');
        add = add + invest_cur + invest_pract + invest_asset + invest_other;
        list = app_money_char(add);
        $scope.form_data.capitalStructure.invest_amount = list[0];
        $scope.money.invest_amount = list[1];
    }

    $scope.query_cust = function(customer_id){
        companyInformationService.query(customer_id).success(function(resp){
            $scope.customer = resp.data.customer;
        });
    }

    $scope.invest_percentage = function(fact_amount){
        if ($scope.$parent.customer != undefined){
            $scope.customer_id = $scope.$parent.customer.id;
            $scope.query_cust($scope.customer_id);
            var paid_amount = parseInt('0');
            if($scope.customer.paid_amount != null && $scope.customer.paid_amount != ""){
                paid_amount = parseInt($scope.customer.paid_amount);
            }
            var fact = parseInt('0');
            if(fact_amount != null && fact_amount !=""){
                fact = parseInt(fact_amount);
            } 
            $scope.form_data.capitalStructure.invest_percentage = (fact * 100 / paid_amount).toFixed(0);
        }
    }

})

.controller('companyController',function($scope,$http,$rootScope){
    $scope.company={}
   function isValidOrgCode(orgCode){
      var ret=false;
      var codeVal = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
      var intVal = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35];
      var crcs = [3,7,9,10,5,8,4,2];
      if (orgCode == null)
          return ret;
      if(orgCode.length==10){
         var sum=0;
         for(var i=0;i<8;i++){
            var codeI=orgCode.substring(i,i+1);
            var valI=-1;
            for(var j=0;j<codeVal.length;j++){
                if(codeI==codeVal[j]){
                   valI=intVal[j];
                   break;
                }
            }
            sum+=valI*crcs[i];
         }
         var crc=11- (sum%11);
         switch (crc){
             case 10:{
                crc="X";
                break;
             }default:{
                break;
             }
         }
         if(crc==orgCode.substring(9)){
             ret=true;
         }else{
             ret=false;
         }
      }else{
             ret=false;
      }
    
      return ret;
    }
    
    function isCode(data){
        if(data.length != 10){
            return false;
        }
    }

    $scope.org_check1 = function(){
    var code;
    if($scope.company.org_id1.length == 9){
        code = $scope.company.org_id1.substring(0,8);
        code = code+'-';
        code = code+$scope.company.org_id1.substring(8);
        $scope.company.org_id1 = code;
        $scope.company.credit_no = null;
    }
    if($scope.company.org_id1.length == 10){
        code = $scope.company.org_id1;
        $scope.company.credit_no = null;
    }
    if($scope.company.org_id1.length == 18){
        code = $scope.company.org_id1.substring(8,16);
        code = code+'-';
        code = code+$scope.company.org_id1.substring(16,17)
        $scope.company.credit_no = code;
    }
    if(isCode(code) == false){
            $scope.company.org_id1 = null;
            alert('请输入正确的组织机构代码!');
        }
    }

    $scope.name_check = function(){
        if($scope.company.name == null){
           alert('请输入客户名称');
        }
    }

    $scope.submit = function(){
        if($scope.company.name == null || $scope.company.org_id1 == null) {
        alert('请填写完信息');
    } else {
        if($scope.associate)
            $scope.company.associate = $scope.associate;
        if($scope.party_id)
            $scope.company.party_id = $scope.party_id;
        $scope.company.branch_code=$rootScope.user_session.branch_code;
        $http.post(base_url+'/customers/company', $scope.company).success(function(resp){
        var rt = resp.data;

        if (rt.success) {
            alert('客户添加成功！，客户编号:'+rt.success.cust_no);
            var cust_name = $scope.company.name;
            var tabName = cust_name + '的客户信息';
            $scope.forward(tabName, 'views/customer/company/index.html', {'customer': {id:rt.success.cust_id}});
        } else {
            alert('错误:'+rt.error);
        }
        })
    }
    }

    $scope.clear = function(){
        $scope.company = null;
    }

})
.controller('companyManageController', function($scope,$rootScope,companyInformationService){
    $scope.customer_tab={};
    $scope.loan_tab={};
    
    $scope.customerListTH = ['客户编号', '客户名称', '证件类型', '证件号码', '客户类型'];
    $scope.cust_search = {'cust_name':null,'cust_no':null,'cert_type':'组织机构代码证','cert_nu':null}; 
    $scope.custTableData = []
    var eventObj = { 'create':'', 'focus':'', 'loseFocus':'', 'close':'', };
    $scope.customerInfoDetail = function(cust){
        var cust_id = cust.id;
        var cust_name = cust.name;
        var cust_type = cust.type_code;
        var tabName = cust_name+'的客户信息';
        var htmlContent = '<div ng-include="'+'\'views/customer/company/index.html' +'\'" ></div>';       
        console.log(tabName);
        if($scope.customer_tab[cust_id] == undefined || $rootScope.tab[$scope.customer_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':cust});
            $scope.customer_tab[cust_id] = tab_id;
        }else{
            alert("用户信息标签已打开");
        }
    };
    // ------------- 加服务
    $scope.searchCustomer = function(){
        console.log('company');
        companyInformationService.query_companys($scope.cust_search.cust_no, $scope.cust_search.cust_name,$scope.cust_search.cert_type,$scope.cust_search.cert_nu).success(function(resp){
            $scope.custTableData =  resp.data;
        });
    };
    $scope.newCustomer = function(){
        $rootScope.forward('新增对公客户','views/customer/company/com_add.html'); 
    };
 
    $scope.loanApplication = function(cust){
        var cust_id = cust.id;
        var cust_name = cust.name;
        var apply_type='';
        apply_type='对公业务申请'
        var tabName = cust_name+'的贷款申请';
        var htmlContent = '<div ng-include="'+'\'views/credit/preCredit.html' +'\'"></div>';
        if($scope.loan_tab[cust_id] == undefined || $rootScope.tab[$scope.loan_tab[cust_id]] == undefined){
            var tab_id = $rootScope.addTab(tabName, htmlContent, eventObj, true, {'customer':cust,'apply_type':apply_type});
            $scope.loan_tab[cust_id] = tab_id;
        }else{
            alert("用户贷款标签已打开");
        }
    };
})

//身份证
var Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ];  
var ValideCode = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ];  
function IdCardValidate(idCard) {   
     idCard = trim(idCard.replace(/ /g, ""));  
     if (idCard.length == 15) { 
         console.log(idCard.length) 
         return isValidityBrithBy15IdCard(idCard);  
     } else if (idCard.length == 18) { 
         console.log(idCard.length)
         var a_idCard = idCard.split("");  
         if(isValidityBrithBy18IdCard(idCard)&&isTrueValidateCodeBy18IdCard(a_idCard)){                 //console.log("OK")
             return true;  
         }else {  
             alert('证件不合法')
             return false;  
         }       
     } else { 
             return false;  
     }       
 }

function isTrueValidateCodeBy18IdCard(a_idCard) {
     var sum = 0;
     if (a_idCard[17].toLowerCase() == 'x') {
         a_idCard[17] = 10;
     }
     for ( var i = 0; i < 17; i++) {
         sum += Wi[i] * a_idCard[i];
     }
     valCodePosition = sum % 11;
     if (a_idCard[17] == ValideCode[valCodePosition]) {
         return true;
     } else {
         return false;
     }
 }

function isValidityBrithBy18IdCard(idCard18){
     var year =  idCard18.substring(6,10);
     var month = idCard18.substring(10,12);
     var day = idCard18.substring(12,14);
     var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
     if(temp_date.getFullYear()!=parseFloat(year)
           ||temp_date.getMonth()!=parseFloat(month)-1
           ||temp_date.getDate()!=parseFloat(day)){
             return false;
     }else{
         return true;
     }
 }

function isValidityBrithBy15IdCard(idCard15){
      var year =  idCard15.substring(6,8);
      var month = idCard15.substring(8,10);
      var day = idCard15.substring(10,12);
      var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
      if(temp_date.getYear()!=parseFloat(year)
               ||temp_date.getMonth()!=parseFloat(month)-1
               ||temp_date.getDate()!=parseFloat(day)){
                 return false;
         }else{
             return true;
         }
  }

// --- 客户影像   ---
ysp.controller('companyImageService',function(imageService,$scope,store){
    $scope.party_id =null;
    if ($scope.$parent.customer != undefined){
        $scope.party_id = $scope.$parent.customer.id;
    }
    console.log('party_id',$scope.party_id);
    $scope.imgList=[];
    $scope.searchImage = function(){
        if([null,undefined,''].indexOf($scope.about)!=-1){
            alert('请选择照片类型')
            return;
        }
        imageService.query_cust($scope.party_id,$scope.about).success(function(resp){
            var imgs = resp.data;
            $scope.imgList=[];
            for (var i in imgs){
                $scope.imgList.push('.'+imgs[i].url.substring(11,imgs[i].url.length))
                //console.log(resp.data);
            }
        
        });

    }
        
    $scope.addImage = function(){
        if([null,undefined,''].indexOf($scope.about)!=-1){
            alert('请选择照片类型')
            return;
        }
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#custImage").prop('files');
            //console.log(file);
        var token = store.getSession("token");
        var form = new FormData();
        for(var i in files)
            form.append('file',files[i]);
        form.append('party_id',$scope.party_id)
        form.append('about',$scope.about)
        $.ajax({
            type: "POST",
            url : base_url+"/img/customer/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                console.log(msg);
                alert(msg.data.msg);
            }    
        });  
    }
});

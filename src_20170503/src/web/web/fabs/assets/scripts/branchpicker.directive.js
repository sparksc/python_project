function branchPicker(permissionService) {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {
            var menuContentID = "menuContent"+scope.tabId;
            var jqMenuContentID = "#"+menuContentID;

            var tabId = "tab_"+scope.tabId+"_content";
            var jqTabID = "#" + tabId;

            var zTreeID = "ztree" + scope.tabId;

            $(element).prop("readonly",true);
            var setting = {
                check: {
                    enable: true,
                    chkboxType: {"Y":"", "N":""}
                },
                view: {
                    dblClickExpand: false
                },
                data: {
                    key:{
                        name:"branch_name",
                        title:"branch_name",
                        children:"children"
                    }
                },
                callback: {
                    onCheck: function(){
                        var zTree = $.fn.zTree.getZTreeObj(zTreeID),
                        nodes = zTree.getCheckedNodes(true),
                        val = $.map(nodes,function(node){ return "'"+node.branch_code+"'"});
                        $(element).val(val.join(",")).trigger("input"); //angular linstens for "input" event.
                    }
                }
            };

            function onBodyDown(event) {
                if (!(event.target.id == menuContentID || $(event.target).parents(jqMenuContentID).length>0)) {
                    hideMenu();
                }
            }

            function hideMenu() {
                    $(jqMenuContentID).fadeOut("fast");
                    $("body").unbind("mousedown", onBodyDown);
            }

            var tc = '<div id="'+menuContentID+'" class="menuContent" style="display:none; position: absolute;background-color:white;border:1px solid gray;"><ul class="ztree" id="'+zTreeID+'"></ul></div>';
            // angular.element($(jqTabID).find("div:eq(0)>div")).append(tc);
            angular.element($("body")).append(tc);
            otree = $(jqMenuContentID).find(".ztree")
            permissionService.user_branches().success(function(resp) {
                $.fn.zTree.init(otree, setting, resp.data);
                $.fn.zTree.getZTreeObj(zTreeID).expandAll(true);
            });
            
            $(element).wrap('<div class="zTreeDemoBackground left"></div>');
            $(element).click(function(){
                var inputObj = $(this);
                var inputOffset = inputObj.offset();
                $(jqMenuContentID).css({left:inputOffset.left + "px", top:inputOffset.top + inputObj.outerHeight() + "px"}).show();
                $("body").bind("mousedown", onBodyDown);
            });

        }
    };
}
branchPicker.$inject=["permissionService"]
angular.module('YSP').directive('branchPicker', branchPicker);
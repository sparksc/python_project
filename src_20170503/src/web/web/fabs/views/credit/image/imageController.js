ysp.controller('commImageController',function($scope,imageService){
    
    console.log('comm Image');
    if($scope.applicationId){

    }else{
        return ;
    }    
    $scope.research=[];
    $scope.commInit = function(){
        // 贷前
        imageService.query($scope.applicationId).success(function(resp){
            $scope.research = resp.data.research;
            console.log('comm Image',$scope.research);
            if($scope.research){
                console.log($scope.research);
            }
        });
    }
    $scope.commInit();
    $scope.show_img=[];
    $scope.imgShow = function(show_type){
        
        if (show_type == 'research'){
            $scope.show_img = $scope.research
        }

    }
    console.log('over Image');

});


ysp.controller('imageController',function(BillService,$scope,store,imageService){
    console.log($scope.image_about);
    console.log($scope.applicationId);
    if($scope.applicationId){

    }else{
        return ;
    }    
   
    $scope.pdf_list = [];
    $scope.img_list=[];
    $scope.imageDelete = function(index,url){
        imageService.img_delete({'url_list':[url]}).success(function(resp){
            alert(resp.data.msg); 
            $scope.img_list.splice(index,1);
        });
    }
    $scope.pdfDelete = function(url){
        imageService.pdf_delete({'url_list':[url]}).success(function(resp){
            alert(resp.data.msg); 
            $scope.pdf_list.splice(index,1);
        });
    }

    //***********************************************************************
    // 电子档案
    //***********************************************************************
    $scope.searchEle = function(){
        imageService.pdfile_query($scope.applicationId,'elec_arch').success(function(resp){
                $scope.pdf_list  = resp.data;      
                console.log(resp.data);
        });
    }
    $scope.addPdf = function(){

        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#elec_arch").prop('files');
        var token = store.getSession("token");
        var form = new FormData();
        console.log(files)
        for(var i = 0 ; i < files.length ; ++i){
            console.log('---',files[i]);
            form.append('pdfs',files[i]);
        }
        form.append('application_id',$scope.applicationId)
        form.append('about','elec_arch')
        $.ajax({
            type: "POST",
            url : base_url+"/img/pdfile_upload/",
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


    //*********************************
    // 票据影像
    //********************************
    $scope.application_id =  $scope.applicationId;
    $scope.tableHead=['票据号码','正面', '背面','查询复查', '贴现凭证','操作','状态'];
    $scope.queryBillInfo = function(){
        if($scope.application_id != undefined){
            BillService.query_info($scope.application_id).success(function(resp){
                $scope.tableData=resp.data;
                if(resp.data.length >0){
                    $scope.tableMessage='';
                }else{
                    $scope.tableMessage='未查询到数据';
                }
            })
        }
    }
    $scope.billCheckDetail=function(d){
        if (d.img_check == null) d.img_check = '';
        if (d.img_remark == null) d.img_remark ='';
        console.log('状态:'+d.img_check+'<br>意见:'+d.img_remark);
        return '状态:'+d.img_check+' 意见:'+d.img_remark;

    }
    $scope.billUpload = function(d){
        var token = store.getSession("token");
        var ele = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#billImageInfo")
        var front = angular.element(ele).find('#'+d.bill_no+'front').prop('files');
        var back = angular.element(ele).find('#'+d.bill_no+'back').prop('files');
        var check = angular.element(ele).find('#'+d.bill_no+'check').prop('files');
        var cert = angular.element(ele).find('#'+d.bill_no+'cert').prop('files');
        var form = new FormData();
        form.append('front',front[0])
        form.append('back',back[0])
        form.append('check',check[0])
        form.append('cert',cert[0])

        //console.log(front,back,check,cert)
        form.append('bill_no',d.bill_no)
        $.ajax({
            type: "POST",
            url : base_url+"/img/bill/upload/",
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
    $scope.billQuery = function(d){
        imageService.bill_query(d.bill_no).success(function(resp){
            var imgs = resp.data.bill_img;
            console.log(imgs);
            for( var i in imgs){
                if (imgs[i].name == 'front'){
                    $scope.front_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
                }
                if (imgs[i].name == 'back'){
                    $scope.back_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
                }
                if (imgs[i].name == 'check'){
                    $scope.check_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
                }
                if (imgs[i].name == 'cert'){
                    $scope.cert_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
                }
            }
        });
    }


    //*********************************
    // 投资影像
    //********************************
   $scope.investUpload = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#invest_arch").prop('files');
        var token = store.getSession("token");
        var form = new FormData();
        console.log(files)
        if(['',null,undefined].indexOf($scope.invest_about)!=-1){
            alert('请选择择资料');
            return ;
        }
        if (['invest_con','gua_info'].indexOf($scope.invest_about)!=-1){
            for(var i = 0 ; i < files.length ; ++i){
                console.log('---',files[i]);
                form.append('pdfs',files[i]);
            }
            form.append('application_id',$scope.applicationId)
            form.append('about',$scope.invest_about)
            
            $.ajax({
                type: "POST",
                url : base_url+"/img/pdfile_upload/",
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
        }else{
            for(var i = 0 ; i < files.length ; ++i){
                console.log('+++',files[i]);
                form.append('upload_file',files[i]);
            }
            form.append('application_id',$scope.applicationId)
            form.append('img_about',$scope.invest_about)
            $.ajax({
                type: "POST",
                url : base_url+"/img/",
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
   }
   $scope.investSearch = function(){

        if(['',null,undefined].indexOf($scope.invest_about)!=-1){
            alert('请选择择资料');
            return ;
        }
        if(['invest_con','gua_info'].indexOf($scope.invest_about)!=-1){
            imageService.pdfile_query($scope.applicationId,$scope.invest_about).success(function(resp){
                    $scope.pdf_list = [];
                    $scope.img_list = [];
                    $scope.pdf_list  = resp.data;      
                    if (resp.data.length == 0){
                        alert('没查到,检查你输入的信息')
                    }
                    console.log(resp.data);
            });
        }else{
            imageService.query($scope.applicationId,$scope.invest_about).success(function(resp){
                    $scope.pdf_list = [];
                    $scope.img_list = [];
                    $scope.img_list  = resp.data;      
                    if (resp.data.length == 0){
                        alert('没查到,检查你输入的信息')
                    }
                    console.log(resp.data);
            });
        }
    }

});


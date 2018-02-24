ysp.controller('discountSearchController',function(BillService,$scope,store,imageService){

    // 签票查询    
    $scope.check_value = function (value){
        if(['',null,undefined].indexOf(value) !=-1){
            alert('请输入查询');
            return false;
        }
        return true;
    }
    var d = new Date();
    $scope.start_time = d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();
    $scope.end_time = $scope.start_time;
    $scope.discount_imgList=[];


    $scope.billDeal = function(bill){
        var imgs = bill.bill_img;
        var it = new Object();
        it.img_check = bill.img_check;
        it.img_remark = bill.img_remark;
        console.log(it);
        for( var i in imgs){
            it.bill_no = imgs[i].bill_no;
            if (imgs[i].name == 'front'){
                it.front_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
            }
            if (imgs[i].name == 'back'){
                it.back_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
            }
            if (imgs[i].name == 'check'){
                it.check_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
            }
            if (imgs[i].name == 'cert'){
                it.cert_url ='.'+ imgs[i].url.substring(11,imgs[i].length);
            }
        }
        $scope.discount_imgList.push(it);
    }
    $scope.table_show=false;
    $scope.searchDiscount = function(){
        console.log($scope.discount_about,$scope.discount_no)
        switch ($scope.discount_about)
        {
            case 'contract_no':
                break;
            case 'bill_no':
                if ($scope.check_value($scope.discount_no)){
                    imageService.bill_query($scope.discount_no).success(function(resp){
                        $scope.discount_imgList = [];
                        var bill = resp.data;
                        if (bill.bill_img.length ==0){
                            alert('票据号不存在');
                        }else{
                            $scope.table_show=true;
                            $scope.billDeal(bill);
                        }
                    });
                }
                break;
            case 'batch_no':
                break;
            default:
                alert('请选择查询方式');
                break;
        }
        
    }
    $scope.discountPrint = function(){
        if($scope.discount_imgList.length == 0){
            alert("请先查询要打印的图片");
        }else{
           imageService.discount_print({'disList':$scope.discount_imgList}).success(function(resp){
                var url = resp.data;
                console.log(url);
                $scope.printUrl = '.'+url.substring(11,url.length);
           });
        }

    }

    $scope.disBatch = function(bill_list){
        for (var id in bill_list){
            $scope.billDeal(bill_list[id])
        }
    }

    $scope.batchBill = function(){
        var files = angular.element(document.getElementById('tab_'+ $scope.tabId + '_content')).find("#batch_bill_search").prop('files');
        var token = store.getSession("token");
        var form = new FormData();
        console.log(files)
        form.append('billno_file',files[0]);
        $.ajax({
            type: "POST",
            url : base_url+"/img/billno_file/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(rsp){
                $scope.discount_imgList = [];
                console.log(rsp.data);
                var msg = rsp.data.msg
                if (msg!='0'){
                    alert(msg);
                }
                $scope.table_show=true;
                $scope.disBatch(rsp.data.billList);
            }    
        });  
    }    
    $scope.imgShow = function(url){

        $scope.img_show = url
        console.log('url:',url)

    }
    $scope.imgPrint = function(url){
        imageService.img_print({'img_list':[url]}).success(function(resp){
                var url = resp.data;
                console.log(url);
                $scope.printUrl = '.'+url.substring(11,url.length);
        });

    }

    $scope.checkImage = function(bill_no,check,remark,id){
        if (check == '不符' && ['',null].indexOf(remark)!=-1){
            alert('请填写不符合的理由');
            return ;
        }
        if(check == '同意'){
            remark = '';
        }

        var data = {'bill_no':bill_no,'img_check':check,'img_remark':remark}
        imageService.img_check(data).success(function(resp){
            $scope.discount_imgList[id].img_check = check;
            alert(resp.data.msg);
        });
    }
});

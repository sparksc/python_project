ysp.controller('listBillController', function($scope, store, $rootScope, loanService, BillService){
    //承兑汇票票据清单
    $scope.tableHead=['申请书号','票据号码', '编号', '票据种类'];
    $scope.application_id=$scope.$parent.applicationId;
    $scope.form_data={};
    $scope.money={};
    $scope.tableData=[];
    $scope.form_data.bill_kill = '银行承兑汇票';
    //表单查询
    $scope.queryInfo = function(){
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
    //行号长度校验
    $scope.check = function(data){
        if(data == undefined || data.length != 12){
            alert('请输入正确的12位行号')
        }
    }
    //票据类型校验
    $scope.bill_no = function(data){
        if($scope.form_data.bill_type == "电票"){
            if(data == undefined){
                alert("请输入正确的票据号码");
            }else if(data.length != 30){
                alert("请输入正确的30位票据号码");
                return -1;
            }
        }
    }
    //票据保存
    $scope.submit = function(v){
        if(v){
            if($scope.max_month($scope.form_data.bill_due_date) == -1
                ||$scope.bill_no($scope.form_data.bill_no)==-1){
                return ;
            } 
            $scope.form_data.product_type = '签发';
            if($scope.form_data.id == undefined){
                var bill_no;
                if($scope.form_data.bill_type == "纸票"){
                    bill_no = -1
                }else{
                    bill_no = $scope.form_data.bill_no;
                }
                    BillService.query($scope.application_id, {'bill_no':bill_no, 'product_type':$scope.form_data.product_type}).success(function(resp){
                        console.log(resp.data)
                        $scope.form_data.accptor_agreement_no = resp.data.count;
                        var sig = 1;
                        if(resp.data.msg == "err"){
                           sig = 0;
                           alert('该票据号已存在');
                        }
                        console.log(resp.data.bill_type)
                         if(resp.data.bill_type != null && resp.data.bill_type.bill_type != $scope.form_data.bill_type){
                            sig = 0;
                            alert('请录入统一的票据类型')
                         }
                         if(sig){
                            BillService.create($scope.application_id,$scope.form_data).success(function(resp){
                                $scope.disabled_flag=true;
                                alert('票据新增成功');
                                $scope.queryInfo();
                                $scope.disabled_flag = false;
                                $scope.form_data={};
                                $scope.money={};
                            })
                         }
                     })
            }else{
                BillService.update($scope.form_data.id,$scope.form_data).success(function(resp){
                    $scope.queryInfo();
                    alert('票据保存成功');
                })
            }
        }
    }
    //修改
    $scope.edit = function(){
        $scope.disabled_flag=false;
    }
    //详情
    $scope.billInfoDetail = function(data){
        $scope.disabled_flag=true;
        $scope.form_data=data;
        $scope.money.bill_amount = app_money_char($scope.form_data.bill_amount)[1];
    }
    //删除
    $scope.delbillInfo = function(bill_id){
        BillService.del(bill_id).success(function(resp){
            $scope.queryInfo();
            $scope.form_data={};
            $scope.money={};
            $scope.form_data.bill_kill = '银行承兑汇票';
        })
    }
    //详情删除
    $scope.delete = function(){
        console.log($scope.form_data.bill_id)
        if($scope.form_data.bill_id == undefined){
            $scope.form_data={};
            $scope.money={};
            $scope.form_data.bill_kill = '银行承兑汇票';
             
        }else{
            BillService.del($scope.form_data.bill_id).success(function(resp){
                $scope.queryInfo();
                $scope.disabled_flag=false;
                $scope.form_data={};
                $scope.money={};
                $scope.form_data.bill_kill = '银行承兑汇票';
            })
        }
    }
    $scope.bill_amount = function(data){
        var list = app_money_char(data);
        $scope.form_data.bill_amount = list[0];
        $scope.money.bill_amount = list[1];
    }
    $scope.bill_type = function(data){
        if(data == '纸票'){
            $scope.bill_no_disabled_flag = true;
            $scope.form_data.bill_no = '';
        }else{
            $scope.bill_no_disabled_flag = false;
        }
    }
   
    $scope.bill_from_date = function(data){
        $scope.form_data.bill_from_date = app_date_ch(data);
        if($scope.days($scope.form_data.bill_from_date, $scope.new_date())>0){
            alert('出票日期大于等于当前日期');
            $scope.form_data.bill_from_date = '';
        }
    }
    $scope.bill_due_date = function(data){
        $scope.form_data.bill_due_date = app_date_ch(data);
        if($scope.days($scope.new_date(), $scope.form_data.bill_due_date)>0){
            alert('到期日期小于当天');
            $scope.form_data.bill_due_date = '';
            return ;
        }
        $scope.max_month($scope.form_data.bill_due_date);
    }
    $scope.max_month = function(data){
        if($scope.form_data.bill_from_date == undefined || $scope.form_data.bill_from_date == ''){
            return -1;
        }
        if(data == undefined || data ==''){
            return -1;
        }
        from_date = $scope.form_data.bill_from_date;
        if($scope.days(from_date, data) >= 0){
            alert('票据到期日不能小于等于出票日期')
            $scope.form_data.bill_due_date = '';
            return -1;
        }
        if($scope.form_data.bill_type == "电票"){
            var year = from_date.substring(0,4)*1+1;
            var from_date = year + from_date.substring(4,10); 
            if($scope.days(from_date, data) < 0){
                alert('出票日期至票据到期日不能大于1年')
                $scope.form_data.bill_due_date = '';
                return -1;
            }
        }else{
            var month = from_date.substring(5,7)*1+6;
            console.log(month)
            if(month > 12){
                month = month - 12;
                var year = from_date.substring(0,4)*1+1;
                var from_date = year +'-'+ month + from_date.substring(7,10);
            }else{
                var year = from_date.substring(0,4);
                var from_date = year +'-'+ month + from_date.substring(7,10);
            }
            if($scope.days(from_date, data) < 0){
                alert('出票日期至票据到期日不能大于6个月')
                $scope.form_data.bill_due_date = '';
                return -1;
            }
        }
    }
    //获取当前日期
    $scope.new_date =function(){
        var newd = new Date();
        var year = newd.getFullYear()
        var month = newd.getMonth()+1
        var day = newd.getDate();
        if(month<10){
           month = '0'+month;
        }    
        if(day<10){
            day = '0'+day;
        }    
        return year+'-'+month+'-'+day;
    }
    $scope.days = function(date1, date2){
        if(date1 == undefined || date2 == undefined){
            return ;
        }
        var from_date = new Date(Date.parse(date1.replace(/-/g,'/')));
        var due_date = new Date(Date.parse(date2.replace(/-/g,'/')));
        var days = (from_date - due_date)/(24*60*60*1000);
        return days;
    }
    //文件上传
    $scope.upload = function(){
        var token = store.getSession("token");
        var file = $('#listBill').find('input[name="file"]').prop('files');
        var form = new FormData();
        if(file[0] == undefined){
            alert('请选择上传文件');
            return;
        }
        form.append('file',file[0]);
        form.append('application_id', $scope.application_id);
        $.ajax({
            type: "POST",
            url : base_url+"/bill/listBill/upload/",
            data: form,
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("x-session-token", token);
            },   
            success: function(msg){
                console.log(msg.data)
                if(msg.data == 'err'){
                    alert('文件数据有误，上传失败')   
                }else{
                    $scope.queryInfo();
                    alert("上传成功");
                }
            }    
        });  
    }
})













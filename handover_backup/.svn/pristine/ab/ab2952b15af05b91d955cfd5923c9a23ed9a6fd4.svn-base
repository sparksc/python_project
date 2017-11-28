$("a[href='aplbox_modal']").click(function(evt){
    evt.preventDefault();
    $("#cashapl_sel").html("");
    $.ajax({
        url : '/teller/getcashbox/',
        type : 'GET',
        dataType : 'json',
        success : function( data ){
            var cashboxs =  data.cashboxs;
            for ( var i = 0; i < cashboxs.length; i++ ){
                if (cashboxs[i][2] == '1'){
                    var cash_sel = "<option value='"+cashboxs[i][0]+"'>编号："+cashboxs[i][1]+"   </option>";
                }else{
                    var cash_sel = "<option value='"+cashboxs[i][0]+"' disabled>编号："+cashboxs[i][1]+"   已被领用</option>";
                }
                $("#cashapl_sel").append(cash_sel);
            }
            
        
        }
    
    });
    $("#aplbox_modal").modal('open');

});

//提交表单
$("#apl_box_form").submit(function(){
    var res = $("#cashapl_sel").select2("data");
    var date = $("#datepicker").val();
    console.log(date);
    var instock_nu = $("#instock_nu").val();
    var cids="";
    for (var i = 0; i < res.length; i++){
        if ( cids == "" ){
            cids = res[i].id ;
        }else{
            cids = cids + '-' + res[i].id;
        }
        
    }
    $(this).ajaxSubmit({
        url : '/teller/aplbox/',
        type : 'POST',
        dataType : 'json',
        async : false,
        data : {
            'date' : date,
            'instock_nu' : instock_nu,
            'cids' : cids
        },
        success : function(data){
            if (data.is_success){
             Materialize.toast('申请成功！', 4000);
            }
            else{
                Materialize.toast('申请失败！', 4000);
            }
            location.reload();
        }
    });
});


//指纹复核
$(".recheck").click(function(){

    var apl_id = $(this).attr('id');
    $.ajax({
        url : '/teller/recheck/',
        type : 'GET',
        dataType : 'json',
        data : {
            'apl_id' : apl_id
        },
        success : function(data){
            if ( data.is_success){
                Materialize.toast('指纹复核成功！', 4000);

            }else{
                Materialize.toast('指纹复核失败！', 4000);
            }
            location.reload(); 
        }
    
    });
    
});





//为实现
$(".alter_apl").click(function(){
    alert("dd")

});

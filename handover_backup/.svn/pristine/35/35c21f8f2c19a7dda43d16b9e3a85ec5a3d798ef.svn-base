$("a[href='arrage_aplroute']").click(function(){
    var ids = "";
    $("input[index='aplids']").each(function(){
        if ( ids == ""){
            ids = $(this).val();
        }else{
            ids = ids + '-' +$(this).val();
        }
    });
    window.open("/admin/arrage_aplroute/?ids="+ids);

});

$(".del_apl").click(function(){
    var apl_id = $(this).attr('id');
    $.get("/admin/delapl/",{'apl_id':apl_id},function(data){
        location.reload();
    });
    
});

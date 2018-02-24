function app_money_char(data){
    if(data == undefined || data == null || data == ''){
        return ['0.00', '0.00'];
    }
    data = data + "";
    data = data.replace(/,/g,''); 
    var data_in = data;
    if (data.indexOf('.') == -1){
        data = data + '.00';
    }
    var data_ch = (data*1).toLocaleString();
    if (data_ch.indexOf('.') == -1){
        data_ch = data_ch + '.00';
    }
    return [data_in, data_ch]
}

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



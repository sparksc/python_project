function merge_col_action(tbody, startRow, endRow, merge_cols, c){
    var col = merge_cols[c];

    if( c >= merge_cols.length )
        return;
    if ( c == 0 ){
        endRow = tbody.rows.length - 1;
    } 
    for ( var i = startRow; i < endRow; i++ ){
        //下一行相同
        s = col - c;
        if ( tbody.rows[startRow].cells[col].innerHTML == tbody.rows[i+1].cells[s].innerHTML){
            tbody.rows[i+1].removeChild( tbody.rows[i+1].cells[s] );
            tbody.rows[startRow].cells[col].rowSpan = (tbody.rows[startRow].cells[col].rowSpan|0)+1;
            //合并到边界
            if ( i == endRow - 1 && startRow != endRow ){
                merge_col_action(tbody, startRow, endRow, merge_cols, c+1);
            }
        }else{
            //下一行不同
            merge_col_action( tbody, startRow, i+0, merge_cols, c+1);
            startRow = i + 1;
        }
    }
}

tablename = null;
merge_cols = {}
function merge_table(){
    var tf = document.getElementById(tablename);
    tb = tf.getElementsByTagName('tbody')[0];
    merge_col_action(tb, 0, 0, merge_cols, 0)
    tf.style.display = "block"
}

function merge_table_show( name, mc ){
    tablename = name;
    merge_cols = mc;
    var tf = document.getElementById(tablename);
    tf.style.display = "none"
    setTimeout(merge_table,500)     
}

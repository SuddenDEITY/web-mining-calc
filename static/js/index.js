var jsonObject;

function dataInicialize(data) {
    jsonObject = JSON.parse(data);
    printData();
}

$(function(){
    $('span').click(function(){
       $('span').removeClass('active');
       let asc = ( $(this).attr('sortBy') );
       let className = ( $(this).attr('class') );
       $(this).addClass('active');
       sortData(className, asc);
       let sortByValue = (asc == 'asc') ? 'desc' : ((asc == 'desc') ? 'asc' : 'asc');
       $(this).attr('sortBy', sortByValue);
    });
 });

function sortData(prop, asc) {
    window.jsonObject.sort(function(a, b) {
        if (asc == 'asc') {
            return (a[prop] > b[prop]) ? 1 : ((a[prop] < b[prop]) ? -1 : 0);
        } else {
            return (b[prop] > a[prop]) ? 1 : ((b[prop] < a[prop]) ? -1 : 0);
        }
    });
    printData();
}

function printData() {
    $('.tbody-tr').remove();
    $.each(jsonObject, function(i, obj) {
        $('.tbody').append(`
        <tr class="tbody-tr">
        <td>${obj.shop}</td>
        <td><a href='${obj.link}'>${obj.title}</a></td>
        <td>${obj.price}</td>
        <td>${obj.eth_hashrate}</td>
        <td>${obj.ton_hashrate}</td>
        <td>${obj.day_profit}</td>
        <td>${obj.month_profit}</td>
        <td>${obj.day_profit_dual}</td>
        <td>${obj.month_profit_dual}</td>
        <td>${obj.payback}</td>
        <td>${obj.payback_dual}</td>
        </tr>`);
    });
}
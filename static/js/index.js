function dataPrint(data){
    let jsonObject = JSON.parse(data);
    $.each(jsonObject, function(i, obj) {
        console.log(obj);
        $('tbody').append(`
        <tr>
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

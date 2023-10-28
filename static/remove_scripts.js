function remove_location(id) {
    $.ajax({
        url: '/_remove_location',
        method: 'POST',
        data: String(id),
        success: function(){
            $.ajax({
            url: '/_remove_location',
            method: 'GET',
            dataType: 'html',
            success: function(data){
                $('.modal-body').html(data)
            }
        });
        },
        error: function(error){
            alert('Ошибка удаления \n' + error)
        }
    });
}

function remove_inventory(productId) {
    const locationId = $('#location-id').val()
    const quantity = $('#quantity').val()
    $.ajax({
        url: '/_remove_inventory',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({'product_id':productId, 
                              'location_id':locationId, 
                              'quantity':quantity}),
        success: function(){
        $.ajax({
            url: '/_remove_inventory',
            method: 'GET',
            data: {'product_id':productId},
            dataType: 'html',
            success: function(data){
                $('.modal-body').html(data)
            }
            });
        },
        error: function(error){
            alert('Ошибка удаления \n' + error)
        }
    });
}
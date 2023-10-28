function append_product() {
  const productName = $('#product_name').val()
  const productDescription = $('#product_description').val()
  const productPrice = $('#product_price').val()
  const locationId = $('#location_id').val()
  const quantity = $('#quantity').val()
  $.ajax({
    url: '/_append_product',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({'product_name':productName, 
                          'product_description':productDescription, 
                          'product_price':productPrice,
                          'location_id':locationId,
                          'quantity':quantity}),
    success: function(data){
      alert(data)
      $('.modal-body').load('_append_product')
    },
    error: function(error) {
      alert(error)
    }
  });
}

function append_location () {
  $.ajax({
    url: '/_append_location',
    method: 'POST',
    data: $('#location_name').val(),
    success: function(){
      $.ajax({
        url: '/_append_location',
        method: 'GET',
        dataType: 'html',
        success: function(data){
          $('.modal-body').load('_append_location')
        }
      });
    },
    error: function(error){
      alert('Ошибка добавления \n' + error)
    }
  });
}

function append_inventory(productId) {
  const locationId = $('#location-id').val()
  const quantity = $('#quantity').val()
  $.ajax({
    url: '/_append_inventory',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({'product_id':productId, 
                          'location_id':locationId, 
                          'quantity':quantity}),
    success: function(){
      $.ajax({
        url: '/_append_inventory',
        method: 'GET',
        data: {'product_id':productId},
        dataType: 'html',
        success: function(data){
          $('.modal-body').html(data)
        }
      });
    },
    error: function(error){
      alert('Ошибка добавления на склад \n' + error)
    }
  });
}
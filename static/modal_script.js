const baseModal = document.getElementById('baseModal')
if (baseModal) {
    baseModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget
    const recipient = button.getAttribute('data-bs-whatever')
    const modalTitle = baseModal.querySelector('.modal-title')
    const modalButton = baseModal.querySelector('#footer-button')

    if (recipient == 'append_product') {
    modalTitle.textContent = 'Добавление товара'
    modalButton.setAttribute('onclick', 'append_product()')
    $.ajax({
        url: '/_append_product',
        method: 'GET',
        success: function(data){
        $('.modal-body').load('_append_product')
        }
    });
    } else if (recipient == 'append_location') {
    modalTitle.textContent = 'Добавление локации'
    modalButton.setAttribute('onclick', 'append_location()')
    $.ajax({
        url: '/_append_location',
        method: 'GET',
        success: function(){
        $('.modal-body').load('_append_location')             
        }
    });
    } else if (recipient == 'append_inventory') {
        modalTitle.textContent = 'Добавление на склад'
        const productId = button.getAttribute('product-id')
        modalButton.setAttribute('onclick', `append_inventory(${productId})`)
        $.ajax({
        url: '/_append_inventory',
        method: 'GET',
        data: {'product_id':productId},
        dataType: 'html',
        success: function(data){
            $('.modal-body').html(data)             
        }
        });
    } else if (recipient == 'remove_inventory') {
        modalTitle.textContent = 'Удаление со склада'
        const productId = button.getAttribute('product-id')
        modalButton.setAttribute('onclick', `remove_inventory(${productId})`)
        $.ajax({
        url: '/_remove_inventory',
        method: 'GET',
        data: {'product_id':productId},
        dataType: 'html',
        success: function(data){
            $('.modal-body').html(data)             
        }
        });
    }
})
}

function updateTable() {
    $('#product_table').load('_table')
}
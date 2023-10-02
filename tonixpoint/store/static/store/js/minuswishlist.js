$('.minus-wishlist').click(function () {
    var id = $(this).attr("pid").toString();
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success: function (data) {
            // alert(data.message)
            window.location.href = 'http://localhost:8000/product-detail/${id}'
        }
    })
})
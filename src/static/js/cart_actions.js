$('.js-increase_amount_cart').click(function(ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        pid = $this.data('pid');
    data = {};
    data = {
        action: action,
        pid: pid,
        type: type,
        url: this.baseURI

    }
    $.ajax('/increase_amount_cart/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        } else {
            var count = $('.count_' + pid).contents()[0].textContent;
            var _count = parseInt(count, 10);
            _count = _count + 1;
            $('.count_' + pid).contents().last()[0].textContent = _count.toString(10);

            var cost = $('.cost_' + pid).contents()[0].textContent;
            var _cost = parseInt(cost, 10);

            var total = $('.total_' + pid).contents()[0].textContent;
            var _total = parseInt(total, 10);
            _total = _count * _cost;
            $('.total_' + pid).contents().last()[0].textContent = _total.toString(10);

            var total_price = $('.total_price').text();
            var _total_price = parseInt(total_price, 10);
            _total_price = _total_price + _cost;
            $('.total_price').text(_total_price.toString(10));
        }
    });
});

$('.js-reduce_amount_cart').click(function(ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        pid = $this.data('pid');
    data = {};
    data = {
        action: action,
        pid: pid,
        type: type,
        url: this.baseURI

    }
    $.ajax('/reduce_amount_cart/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        } else {
            var count = $('.count_' + pid).contents()[0].textContent;
            var _count = parseInt(count, 10);

            var cost = $('.cost_' + pid).contents()[0].textContent;
            var _cost = parseInt(cost, 10);

            var total_price = $('.total_price').text();
            var _total_price = parseInt(total_price, 10);

            if (_count == 1) {
                _total_price = _total_price - _cost;
                $('.total_price').text(_total_price.toString(10));

                document.getElementById("product_" + pid).remove();
            } else {
                _count = _count - 1;
                $('.count_' + pid).contents().last()[0].textContent = _count.toString(10);

                var total = $('.total_' + pid).contents()[0].textContent;
                var _total = parseInt(total, 10);
                _total = _count * _cost;
                $('.total_' + pid).contents().last()[0].textContent = _total.toString(10);

                _total_price = _total_price - _cost;
                $('.total_price').text(_total_price.toString(10));
            }
        }
    });
});
$('.js-add-to-cart').click(function(ev) {
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
    $.ajax('/add_to_cart/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        }
    });
});
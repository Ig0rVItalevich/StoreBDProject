$('.js-make-order').click(function(ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action');
    data = {};
    data = {
        action: action,
        url: this.baseURI
    }
    $.ajax('/make_order/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        }
    });
});
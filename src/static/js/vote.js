$('.js-vote-like').click(function(ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        pid = $this.data('pid'),
        rid = $this.data('rid');
    data = {};
    if (type == "review")
        data = {
            action: action,
            rid: rid,
            type: type,
            url: this.baseURI

        }
    else
        data = {
            action: action,
            pid: pid,
            type: type,
            url: this.baseURI

        }
    $.ajax('/grade/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        } else {
            id = 0
            if (type == "review")
                id = data.rid
            else
                id = data.pid
            var likes = $('.like_' + id).contents()[0].textContent;

            var bef = parseInt(likes, 10);
            if (Cookies.get('new') == 'True') {
                bef = bef + 1;
            } else {
                bef = bef + 2;
            }
            $('.like_' + id).contents().last()[0].textContent = bef.toString(10);
        }

    });
});

$('.js-vote-dislike').click(function(ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        pid = $this.data('pid'),
        rid = $this.data('rid');
    data = {};
    if (type == "review")
        data = {
            action: action,
            rid: rid,
            type: type,
            url: this.baseURI
        }
    else
        data = {
            action: action,
            pid: pid,
            type: type,
            url: this.baseURI
        }

    $.ajax('/grade/', {
        method: 'POST',
        data: data
    }).done(function(data) {
        if (data.redirect) {
            window.location.href = data.redirect
        } else {
            id = 0
            if (type == "review")
                id = data.rid
            else
                id = data.pid
            var likes = $('.like_' + id).contents()[0].textContent;

            var bef = parseInt(likes, 10);
            if (Cookies.get('new') == 'True') {
                bef = bef - 1;
            } else {
                bef = bef - 2;
            }
            $('.like_' + id).contents().last()[0].textContent = bef.toString(10);
        }

    });
});
from django.core.paginator import Paginator


def current_pages_range(paginator, page):
    count = paginator.num_pages
    try:
        page = int(page)
    except:
        page = 1
    if page < 1 or page > count:
        return (1, 1)
    if count < 5:
        return (1, count)
    d_start = page - 1
    d_end = count - page

    if d_start > 1 and d_end > 1:
        return (page - 2, page + 2)
    elif d_start > d_end:
        return (page - 2 - (2 - d_end), page + d_end)
    else:
        return (page - d_start, page + 2 + (2 - d_start))


def my_paginator(request, tasks, number):
    paginator = Paginator(tasks, number)
    page = request.GET.get('page')
    current_page = paginator.get_page(page)
    start, end = current_pages_range(paginator, page)
    pages = range(start, end + 1)
    return current_page, pages

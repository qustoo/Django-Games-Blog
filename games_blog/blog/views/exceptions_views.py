from django.shortcuts import render

# Errors


def handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(
        request=request,
        template_name="blog/errors/error_page.html",
        status=404,
        context={
            "title": "Страница не найдена: 404",
            "error_message": "К сожалению такая страница была не найдена, или перемещена",
        },
    )


def handler500(request):
    """
    Обработка ошибки 500
    """
    return render(
        request=request,
        template_name="blog/errors/error_page.html",
        status=500,
        context={
            "title": "Ошибка сервера: 500",
            "error_message": "Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта",
        },
    )


def handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(
        request=request,
        template_name="blog/errors/error_page.html",
        status=403,
        context={
            "title": "Ошибка доступа: 403",
            "error_message": "Доступ к этой странице ограничен",
        },
    )

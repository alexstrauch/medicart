from django.shortcuts import render

def handler404(request, exception):
    """
    Custom 404 page
    """
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """
    Custom 500 page
    """
    return render(request, 'errors/500.html', status=500)

def handler502(request):
    """
    Custom 502 page
    """
    return render(request, 'errors/502.html', status=502)

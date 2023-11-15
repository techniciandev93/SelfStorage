from django.shortcuts import render


def index(request):
    return render(
        request,
        'renta_warehouse/index.html',
    )


def get_boxes(request):
    return render(
        request,
        'renta_warehouse/boxes.html'
    )

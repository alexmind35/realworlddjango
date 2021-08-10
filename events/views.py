import datetime

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from events.models import Event, Category, Feature
from django.views.decorators.http import require_POST


def event_list(request):
    event_objects = Event.objects.all()
    category_objects = Category.objects.all()
    feature_objects = Feature.objects.all()
    context = {
        'event_objects': event_objects,
        'category_objects': category_objects,
        'feature_objects': feature_objects,
    }
    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    places_left = event.participants_number - event.enrolls.count()
    try:
        fullness_percent = int((event.enrolls.count() / event.participants_number) * 100)
    except ZeroDivisionError:
        fullness_percent = 0
    context = {
        'event': event,
        'places_left': places_left,
        'fullness_percent': fullness_percent,
    }
    return render(request, 'events/event_detail.html', context)


@require_POST
def create_review(request):
    data = {
        'ok': True,
        'msg': '',
        'rate': request.POST.get('rate'),
        'text': request.POST.get('text'),
        'created': datetime.date.today().strftime('%d.%m.%Y'),
        'user_name': ''
    }
    return JsonResponse(data)

from .models import Map


def get_template_name(url):
    try:
        return Map.objects.get(url=url).template_name
    except Map.DoesNotExist:
        return

import json

from django.http import HttpResponse


def json_response(x):
    return HttpResponse(json.dumps(x, indent=2), content_type='application/json; charset=UTF-8')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class BaseEnumerate(object):
    """
    The base class for creating enumerations
    """
    values = {}

    @classmethod
    def get_choices(cls):
        """
        """
        return cls.values.items()

    get_items = get_choices

    @classmethod
    def get_constant_value_by_name(cls, name):
        """
        """
        if not isinstance(name, basestring):
            raise TypeError("'name' must be a string")

        if not name:
            raise ValueError("'name' must not be empty")

        return cls.__dict__[name]

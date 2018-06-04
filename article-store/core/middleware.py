from typing import Callable
import uuid

from django.conf import settings
from django.http.request import HttpRequest
from django.http.response import HttpResponse


def ensure_run_id(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest):
        run_id = request.META.get(settings.RUN_ID_HEADER, str(uuid.uuid1()))

        request.META[settings.RUN_ID_HEADER] = run_id

        return get_response(request)

    return middleware

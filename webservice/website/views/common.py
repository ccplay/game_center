# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def cdn_feedback(request, slug, *args, **kwargs):
    from website.cdn.core import Feedback
    from website.cdn.parsers import OperationResponse
    ctx1 = request.GET.get('context')
    ctx2 = request.POST.get('context')
    if not(ctx1 or ctx2) or slug != 'ccsc':
        response = OperationResponse(OperationResponse.STATUS_CODE_FAILED,
                                     'Bad Requeset')
        return HttpResponseBadRequest(response.render(),
                                      mimetype='text/xml; charset=utf-8')
    context = ctx1 or ctx2
    feedback = Feedback()
    response = feedback.process(content=context)
    return HttpResponse(response.render(),
                        mimetype='text/xml; charset=utf-8')

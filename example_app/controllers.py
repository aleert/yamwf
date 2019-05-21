# -*- coding: utf-8 -*-

from webob import Response

from yamwf.routing import register


@register('')
def main(request):
    return Response(
        body='Hi there! Please, navigate to home/'
        + ' (or you can use just home to check permanent redirect).',
    )


@register('home/')
@register('home/{foo:int}')
def home(request, **kwargs):
    if 'foo' in kwargs:
        return Response(body='{0}, nice choice!'.format(kwargs.get('foo', '')))
    return Response(
        body='Well hello there, stranger. '
        + 'Please pick up your favorite integer and add it to path.',
    )

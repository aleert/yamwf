# -*- coding: utf-8 -*-

"""Module with utilities to register and load controllers, that use clever routing."""
import re
from typing import Callable, Dict, Tuple

from webob import exc

routes = {}


def register(path: str) -> Callable:
    """
    Decorator to register controllers in our apps.

    `path` can contain typed parameters: '/home/{foo:int}',
     default type is str.
    """
    def _register(controller: Callable) -> Callable:  # noqa: Z430

        path_regex, path_vars = path_to_regex(path)
        routes[re.compile(path_regex)] = controller, path_vars
        return controller
    return _register


# courteously to webob docs
var_regex = re.compile(
    r"""
    {                  # The exact character "{"
    (\w+)              # The variable name
    (?::([^}]+))?      # The optional :regex part
    }                  # The exact character "}"
    """, re.VERBOSE,
)


def path_to_regex(path: str) -> Tuple[str, Dict]:  # noqa: Z210
    """Convert path to regex with {variable: var_type} dict."""
    # accept both '' and '/' as root path
    if not path:
        return '^/$', {}
    regex = ''
    variables = {}
    last_pos = 0
    for match in var_regex.finditer(path):
        regex += re.escape(path[last_pos:match.start()])
        var_name = match.group(1)
        var_type = eval(match.group(2)) or str  # noqa: S307
        expr = '(?P<{0}>\w+)'.format(var_name)
        variables[var_name] = var_type
        regex += expr
        last_pos = match.end()
    regex += re.escape(path[last_pos:])

    if regex.endswith('/'):
        regex = '^/{0}$'.format(regex)
    else:
        regex = '^/{0}/$'.format(regex)

    return regex, variables


def load_controller(request, path: str) -> Callable:  # noqa: C901, Z210
    """Load controller as fixing path and extracting args from it."""
    issue_redirect = False
    if not path.endswith('/'):
        path = request.path + '/'
        issue_redirect = True

    for path_regex, (controller, args) in routes.items():  # noqa:Z446, Z460
        match = path_regex.match(path)

        if match and issue_redirect:
            return exc.HTTPPermanentRedirect(location=request.host_url + path)

        elif match and args:
            typed_args = {}
            try:
                for key in args.keys():
                    arg_type = args[key]
                    typed_args[key] = arg_type(match.group(key))
            except ValueError:
                return exc.HTTPNotFound()

            return controller(request, **typed_args)

        elif match:
            return controller(request)
    return exc.HTTPNotFound()

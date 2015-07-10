from json import dumps

from webapp2 import WSGIApplication, Response, Route
from jinja2 import Environment, PackageLoader


class Micron(WSGIApplication):
    def __init__(self, templatefile=None, *args, **kwargs):
        super(Micron, self).__init__(*args, **kwargs)
        if templatefile:
            self.router.tenv = Environment(loader=PackageLoader(templatefile), extensions=['jinja2.ext.autoescape'],
                                           autoescape=True)
        self.router.set_dispatcher(self._dispatcher)

    @staticmethod
    def _dispatcher(router, req, res):
        returned = router.default_dispatcher(req, res)
        if isinstance(returned, basestring):
            return Response(returned)
        elif isinstance(returned, Template):
            returned = router.tenv.get_template(returned.tfile).render(**returned.kwargs)
            return Response(returned)
        elif isinstance(returned, tuple):
            return Response(*returned)
        else:
            return dumps(returned)

    def route(self, *args, **kwargs):
        def wrap(handler):
            self.router.add(Route(handler=handler, *args, **kwargs))
            return handler

        return wrap


class Template:
    def __init__(self, tfile, **kwargs):
        self.tfile = tfile
        self.kwargs = kwargs


def template(tfile, **data):
    return Template(tfile, **data)
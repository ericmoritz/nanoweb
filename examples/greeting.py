from nanoweb import FrontController
import routes
from routes.middleware import RoutesMiddleware
from webob.dec import wsgify
from webob import Response

apps = {}


@wsgify
def hello(request):
    """A simple WSGI application that says, Hello, World!"""
    return Response("Hello, World!",
                    content_type="text/plain")
apps['hello'] = hello


@wsgify
def goodbye(request):
    """A simple WSGI application that says, Goodbye Cruel World!"""
    return Response("Goodbye Cruel World!",
                    content_type="text/plain")
apps['goodbye'] = goodbye

mapper = routes.Mapper()
mapper.connect("/hello/", application="hello")
mapper.connect("/goodbye/", application="goodbye")

application = FrontController(apps)
application = RoutesMiddleware(application, mapper)

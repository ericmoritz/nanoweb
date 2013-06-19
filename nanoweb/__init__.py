from webob.dec import wsgify
from webob import exc
import simplejson as json
from json_schema_validator.errors import ValidationError
from json_schema_validator.schema import Schema
from json_schema_validator.validator import Validator

__version__ = "1.0"

content_types = {
    "json": "application/json",
    "html": "text/html"
}

decoders = {
    "application/json": json.loads
}

encoders = {
    "application/json": json.dumps
}


def agent_accepts(request, offers):
    # If the format is given, always return
    content_type = None

    if "format" in request.urlvars:
        format = request.urlvars.get("format")
        content_type = content_types[format]

        if content_type not in offers:
            content_type = None
    else:
        content_type = request.accept.best_match(offers)

    if content_type is None:
        raise exc.HTTPNotAcceptable("Offered: %s" % ("; ".join(offers), ))
    else:
        return content_type


def allowed(request, methods):
    if request.method not in methods:
        raise exc.HTTPMethodNotAllowed(allow=methods)


def encode_body(content_type, data, encoders=encoders):
    try:
        encoder = encoders[content_type]
    except KeyError:
        raise ValueError("Unknown content-type: %s" % (content_type, ))

    return encoder(data)

def require_user(request):
    if request.remote_user is None:
        raise exc.HTTPUnauthorized()


def decode_body(request, json_schema=None, decoders=decoders):
    offers = decoders.keys()
    content_type = request.content_type

    if content_type not in offers:
        raise exc.HTTPUnsupportedMediaType(u"%s is not supported" % content_type)

    decoder = decoders[content_type]

    try:
        data = decoder(request.body)
    except Exception, error:
        raise exc.HTTPBadRequest(unicode(error))

    if json_schema:
        try:
            valid = Validator.validate(Schema(json_schema), data)
        except ValidationError, error:
            error_message = u"""%s

Schema:

%s""" % (unicode(error), json.dumps(json_schema).decode("ascii"))

            raise exc.HTTPBadRequest(error_message)

    return data


class FrontController(object):
    def __init__(self, applications):
        self.applications = applications

    @wsgify
    def __call__(self, request):
        match = request.urlvars

        if "_method" in request.GET:
            request.method = request.GET['_method']

        if match:
            inner_app = self.applications[match['application']]
            return request.get_response(inner_app)
        else:
            raise exc.HTTPNotFound()

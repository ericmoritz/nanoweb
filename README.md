# Nano Web

A small framework for WSGI applications.  nanoweb is simple glue
between Webob and Routes encourages the use of existing WSGI middleware
instead of forcing you to use it's own solutions to already solved problems.

## Example

Here is a simple greeting application using Nano

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

There you have it, a simple WSGI application using nanoweb

# Request Guards

nanoweb provides some guards for doing simple HTTP web services.  These guards
assert requirements for a request and if the request or application
can not fulfill the assertion, the request is aborted with the
appropriate HTTP status code.

## agent_accepts(request, offers)

Checks that the client has can accept the content types an application
provides. The request is aborted with `406 Not Acceptable` if the
application can not produce an acceptable response.

    import json 
    from webob import Response

    @wsgify
    def spew_json(request):
        agent_accepts(request, ["application/json"])
        return Response(json.dumps({"message": "Blegh"}))
    

## allowed(request, method)

Guards against requests using disallowed HTTP methods

    @wsgify
    def only_get(request):
        allowed(request, ["GET"])
        return Response("Got.")

## encode_body(content_type, data, encoders=encoders)

Returns serialized data given a content_type based on the dictionary,
`encoders`.  The `encoders` maps mime types to callables. It defaults
to the following::

    encoders = {
      "application/json": json.dumps
    }

Example:

    @wsgify
    def spew_json(request):
        content_type = agent_accepts(request, ["application/json"])
        return Response(encode_body(content_type, {"message": "Blegh"}),
                        content_type=content_type)

## require_user(request)

Asserts that the WSGI environ var "REMOTE_USER" is defined.  It is the
of a middleware to authenticate the request and populate the
REMOTE_USER field in the WSGI environ. Aborts with `401 Unauthorized`.


    @wsgify
    def private_app(request):
        require_user(request)
        return Response("Hi %s" % request.remote_user)

## decode_body(request, json_schema=None, decoders=decoders)

Deserializes the request body using the decoders dictionary.  Just
with encoders, it is a map of mime types to callables.  It defaults to
the following:

    decoders = {
      "application/json": json.loads
    }

If the request's content type is not in decoders, the request aborts
with a 415 Unsupported Media Type.

If json_schema is provided, the decoded body is validated against the
schema using the
[json-schema-validator](https://github.com/zyga/json-schema-validator)
module.  If the schema validation fails, the request aborts and
response with a 400 Bad Request.

    person_schema = {
      "type": "object",
      "properties": {"name": {"type": "string", "required": true},
                     "age":  {"type": "integer", "minimum": "0"},
                     "username": {"type": "string", "required": true}}}
    
    @wsgify
    def put_person(request):
        allowed(request, ["PUT"])
        data = decode_body(request, json_schema=person_schema)
        db.person.store(data['username'], data)
        return HTTPOk()


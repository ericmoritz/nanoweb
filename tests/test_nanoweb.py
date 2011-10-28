import unittest
from webob import Request
from webob import exc
import nanoweb
import simplejson as json


class AcceptsTest(unittest.TestCase):
    def test_accepted(self):
        request = Request.blank("/",
                                accept=["text/html"])

        result = nanoweb.agent_accepts(request, ["text/html"])

        self.assertEqual(result, "text/html")

    def test_not_accepted(self):
        request = Request.blank("/",
                                accept=["application/xml"])

        self.assertRaises(exc.HTTPNotAcceptable,
                          nanoweb.agent_accepts,
                          request, ["text/html"])

    def test_format_accepted(self):
        request = Request.blank("/", urlvars={"format": "html"},
                                accept=["application/json"])

        result = nanoweb.agent_accepts(request, ["text/html"])

        self.assertEqual(result, "text/html")
        
    def test_format_not_accepted(self):
        request = Request.blank("/", urlvars={"format": "json"})

        self.assertRaises(exc.HTTPNotAcceptable,
                          nanoweb.agent_accepts,
                          request, ["text/html"])

class EncodeBodyTest(unittest.TestCase):
    def test_encode_body(self):
        expected = {"foo": "bar"}
        json_result = nanoweb.encode_body("application/json",
                                       expected)
        result = json.loads(json_result)
        self.assertEqual(result, expected)

    def test_encode_body_unknown(self):
        # This occurs when the developer screws up and doesn't use
        # agent_accepts to guard against unoffered formats
        self.assertRaises(ValueError,
                          nanoweb.encode_body,
                          "application/xml", {})

    def test_encode_body_encoders(self):
        data = {"foo": "bar"}
        expected = unicode(data)

        result = nanoweb.encode_body("text/plain",
                                  data,
                                  encoders={ "text/plain": unicode })
        self.assertEqual(result, expected)
        
class DecodeBodyTest(unittest.TestCase):
    def test_not_offered(self):
        request = Request.blank("/",
                                method="PUT",
                                content_type="application/xml")

        self.assertRaises(exc.HTTPUnsupportedMediaType,
                          nanoweb.decode_body,
                          request)

    def test_good_json(self):
        expected = {"title": "test"}
        body = json.dumps(expected)

        request = Request.blank("/",
                                method="PUT",
                                content_type="application/json",
                                body=body)

        result = nanoweb.decode_body(request)
        
        self.assertEqual(result, expected)

    def test_bad_json(self):
        body = "{"
        request = Request.blank("/",
                                method="PUT",
                                content_type="application/json",
                                body=body)

        self.assertRaises(exc.HTTPBadRequest,
                          nanoweb.decode_body,
                          request)

    def test_valid_schema(self):
        json_schema = {"type": "object",
                       "properties": {
                "title": {"type": "string"},
                "pub_date": {"type": "string", 
                             "format": "date-time"}
                }}

        expected = {"title": "Test",
                    "pub_date": "2011-07-13T00:00:00Z"}
        body = json.dumps(expected)

        request = Request.blank("/",
                                method="PUT",
                                content_type="application/json",
                                body=body)

        result = nanoweb.decode_body(request,
                                  json_schema=json_schema)

        self.assertEqual(result, expected)

    def test_invalid_schema(self):
        json_schema = {"type": "object",
                       "properties": {
                "title": {"type": "string"},
                "pub_date": {"type": "string", 
                             "format": "date-time"}
                }}

        expected = {"title": "Test",
                    "pub_date": "not a date-time"}

        body = json.dumps(expected)

        request = Request.blank("/",
                                method="PUT",
                                content_type="application/json",
                                body=body)

        self.assertRaises(exc.HTTPBadRequest,
                          nanoweb.decode_body,
                          request, json_schema=json_schema)


class TestAllowed(unittest.TestCase):
    def test_is_allowed(self):
        request = Request.blank("/",
                                method="PUT")
        nanoweb.allowed(request, ["GET", "PUT"])
            
    def test_is_not_allowed(self):
        request = Request.blank("/",
                                method="DELETE")
        try:
            nanoweb.allowed(request, ["GET", "PUT"])
            self.assertTrue(False, "the allowed() function succeeded.")
        except exc.HTTPMethodNotAllowed, error:
            self.assertEqual(error.allow, ("GET", "PUT", ))

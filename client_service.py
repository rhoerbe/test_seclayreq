from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys
import urllib


def main():
    server_address = ('127.0.0.1', 8080)
    print(f'starting server at {server_address[0]}:{server_address[1]}')
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        with open('testdata/xmlsig_response.xml') as fd:
            self.expected_signed_data = fd.read()
        with open('testdata/unsigned_data.xml') as fd:
            self.xml_to_be_signed = fd.read()
        super().__init__(*args, **kwargs)
    
    def _set_response(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f"GET request,\nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        create_xml_signature_request = self._get_CreateXMLSignatureRequest(self.xml_to_be_signed)
        post_data = create_xml_signature_request
        seclay_post_request_form = self._get_seclay_post_request_form().format(post_data)
        self.wfile.write(seclay_post_request_form.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        ref = urllib.parse.unquote(post_data.decode('utf-8'))
        logging.info(f"POST request with signed data, form data:\n{ref}\n")
        if self.expected_signed_data != ref:
            loggin.error("Signed data not matching expected result")

        self._set_response()
        # self.send_response(200)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def _get_seclay_post_request_form(self):
        return '''\
<!DOCTYPE html>
<html>
  <head><meta charset="utf-8" /></head>
  <body onload="document.forms[0].submit()">
    <p>you must press the Continue button once to proceed.</p>
    <form action="http://localhost:8088/" method="post">
      <input type="hidden" name=" "/>
            <textarea rows="20" cols="100" name="XMLRequest">{}</textarea>
      <input type="submit" value="Continue"/>
    </form>
  </body>
</html>
            '''

    def _get_CreateXMLSignatureRequest(self, res_content):
        return '''\
<?xml version="1.0" encoding="UTF-8"?>
<sl:CreateXMLSignatureRequest
  xmlns:sl="http://www.buergerkarte.at/namespaces/securitylayer/1.2#">
  <sl:KeyboxIdentifier>SecureSignatureKeypair</sl:KeyboxIdentifier>
  <sl:DataObjectInfo Structure="detached">
    <sl:DataObject Reference=""></sl:DataObject>
    <sl:TransformsInfo>
    <dsig:Transforms xmlns:dsig="http://www.w3.org/2000/09/xmldsig#">
        <dsig:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
      </dsig:Transforms>
      <sl:FinalDataMetaInfo>
        <sl:MimeType>application/xml</sl:MimeType>
      </sl:FinalDataMetaInfo>
    </sl:TransformsInfo>
  </sl:DataObjectInfo>
  <sl:SignatureInfo>
    <sl:SignatureEnvironment>
      <sl:XMLContent>
        {}
      </sl:XMLContent>
    </sl:SignatureEnvironment>
    <sl:SignatureLocation xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" Index="0">
      {}
    </sl:SignatureLocation>
  </sl:SignatureInfo>
</sl:CreateXMLSignatureRequest>
        '''.format(res_content, '/md:EntityDescriptor')


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        raise "must use python 3.6 or higher"
    main()
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
        self.sig_response = ''
        super().__init__(*args, **kwargs)
    
    def _set_response(self):
        self.send_response(200)
        #self.send_header("Access-Control-Allow-Origin", "http://localhost")
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info(f"GET request,\nPath: {str(self.path)}\nHeaders:\n{str(self.headers)}")
        if self.path == '/favicon.ico':
            self.send_response(404)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            create_xml_signature_request = self._get_CreateXMLSignatureRequest(self.xml_to_be_signed)
            post_data = create_xml_signature_request
            seclay_post_request_form = self._get_seclay_post_request_form() % (post_data)
            self.wfile.write(seclay_post_request_form.encode('utf-8'))
            print("Signing request page sent")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.sig_response = urllib.parse.unquote(post_data.decode('utf-8'))
        logging.info(f"POST request with signed data, form data:\n{self.sig_response}\n")
        if self.expected_signed_data != self.sig_response:
            logging.error("Signed data not matching expected result")
        else:
            print("signed data received")

        self._set_response()
        result_page = self._get_result_page(self.sig_response)
        self.wfile.write(result_page.encode('utf-8'))

    def _get_seclay_post_request_form(self):
        return '''\
<!DOCTYPE html>
<html>
  <head><meta charset="utf-8" /></head>
  <body onload="document.forms[0].submit()">
    <p>Request page - this page should not be shown in the browser unless java script is disabled</p>
    <textarea rows="30" cols="100" readonly name="XMLRequest">%s</textarea>
    <script>

window.onload = process_automation;

function process_automation () {
    var http = new XMLHttpRequest();
    var url = 'http://localhost:8088';

    var params = 'XMLRequest=' + document.getElementsByName('XMLRequest')[0].value;

    http.ontimeout  = function (event) {
        submit_to_client('<error code=3 msg="connection timeout to signature service on 127.0.0.1:8088"/>');
    }

    http.open('POST', url, true);
    http.timeout = 5000

    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {  //signature response
        if(http.readyState == 4) {
            switch (http.status) {
                case 200:
                    if (http.responseText === undefined || http.responseText === '') {
                        submit_to_client('<error code=2 msg="There is no result to signature service on 127.0.0.1:8088"/>');
                    } else {
                        document.getElementsByName('XMLRequest')[0].value = http.responseText;
                        submit_to_client(http.responseText);
                    }
                    break;
                case 0: 
                    submit_to_client('<error code=1 msg="could not connect to signature service on 127.0.0.1:8088"/>');
                    break;
                default:
                    break;
            }
        }
    }
    http.send(params);
}

function submit_to_client(params) {
    var http = new XMLHttpRequest();
    var url = 'http://localhost:8080/sigresult';

    http.open('POST', url, true);
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {
        if (http.readyState == 4) {
            if (http.status != 200) {
                alert('Failed to answer signature creation request to ');
            }
        }
    }
    http.send(params);
}
    </script>
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

    def _get_result_page(self, sig_response):
        return '''\
        <!DOCTYPE html>
        <html>
          <head><meta charset="utf-8" /></head>
          <body>
            <p>Result page (you must reload the page to trigger the javascript function requesting the signature)</p>
            <p>Signature Service Response:</p>
            <textarea rows="30" cols="100" readonly>
              %s
            </textarea>
          </body>
        </html>
            ''' % sig_response


if __name__ == '__main__':
    if sys.version_info < (3, 6):
        raise "must use python 3.6 or higher"
    main()
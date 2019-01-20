= Request/Response Exchange via POST/POST exchanges

Purpose: request an XML-infoset to be signed by another service.
The connection to the other service is via front-channel, 
that is via the browser.

Flow: 

1. Client requests data entry form (GET /) 
2. Client Service respondes with an HTML form that contains a POST to the signature service.
   Data to be signed is pre-filled for the test case.
3. The browser will (automatically using javascipt) post the form 
4. The signature service responds with an HTML form that POSTs the signed data in a request to the client service. 
   (This is a mock-up service with a static result)
5. The browser will (automatically using javascipt) post the form
6. Success if the signed data has been received
 
 
Client-service listens on port 8080, Signature-service on 8088
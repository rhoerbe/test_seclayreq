# Request/Response Exchange via POST/POST exchanges

## Purpose

Request an XML-infoset to be signed by another service.
The connection to the other service is via front-channel, 
that is via the browser.

## Flow: 

Client-service listens on port 8080, Signature-service on 8088, both localhost

1. Client requests data entry form: (GET http://localhost:8080/  ) 
2. Client Service respondes with an HTML form that contains a POST to the signature service.
   Data to be signed is pre-filled for the test case.
3. The browser will (automatically using javascipt) post the form (POST http://localhost:8088/) 
4. The signature service responds with the signed data 
   (signature_service.py is a mock-up service with a static result)
5. The browser will (automatically using javascipt) post the form back to the client_service (POST http://localhost:8080/ )
6. Success if the signed data has been received, display the result in the browser
 
 

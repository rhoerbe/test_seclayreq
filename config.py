client_service_address = ('127.0.0.1', 18080)
signature_service_url = 'http://localhost:8088/http-security-layer-request'

# Debug helper
# mitmweb --listen-port 8080 --mode reverse:http://127.0.0.1:18080 --listen-host 127.0.0.1 --web-port 8081
# mitmweb --listen-port 8088 --mode reverse:http://127.0.0.1:3495 --listen-host 127.0.0.1 --web-port 8082
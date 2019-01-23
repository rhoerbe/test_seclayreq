window.onload = process_automation;

function process_automation () {
    var http = new XMLHttpRequest();
    var url = 'http://localhost:8088/http-security-layer-request';
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

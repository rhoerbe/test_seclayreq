window.onload = process_automation;

function process_automation () {
    var http = new XMLHttpRequest();
    var url = 'http://localhost:8088';

    var params = 'XMLRequest=' + document.getElementsByName('XMLRequest')[0].value;
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            //success response
            document.getElementsByName('XMLRequest')[0].value = http.responseText;
            submit_to_client(http.responseText);
        }
    }
    http.send(params);
}

function submit_to_client(params){
    var http = new XMLHttpRequest();
    var url = 'http://localhost:8080';

    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            //success response
            alert('ok');
        }
    }
    http.send(params);
}
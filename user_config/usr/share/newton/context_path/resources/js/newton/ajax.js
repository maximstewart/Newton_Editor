const logUIExceptionAjax = (data, action = "client-exception-logger") => {
    const postArgs = 'exception_data=' + data;

    messenger.backend.postMessage(postArgs);
}


const doAjax = (actionPath, data, action) => {
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            if (this.responseText != null) {  // this.responseXML if getting XML data
                postAjaxController(JSON.parse(this.responseText), action);
            } else {
                let type = "danger"
                let msg  = "No content returned. Check the target path.";
                data     = '{"message": { "type": "' + type +  '", "text": "' + text + '" } }'
                postAjaxController(JSON.parse(data));
            }
        }
    };

    xhttp.open("POST", actionPath, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // Force return to be JSON NOTE: Use application/xml to force XML
    xhttp.overrideMimeType('application/json');
    xhttp.send(data);
}
 
const formatURL = (basePath) => {
    url = window.location.href;
    if ( url.endsWith('/') )
        return url + basePath;
    else
        return url + '/' + basePath;
}

const fetchData = async (url) => {
    let response = null;
    response = await fetch(url);
    return await response.json();
}
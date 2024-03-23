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




/* ----------------------------------- Ace LSP -------------------------------*/
async function fetchScript(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Error fetching script: ${response.statusText}`);
    }
    const scriptContent = await response.text();
    return scriptContent;
}

function createScriptBlob(scriptContent) {
    const scriptBlob = new Blob([scriptContent], { type: 'application/javascript' });
    return scriptBlob;
}

function createBlobURL(scriptBlob) {
    const blobURL = URL.createObjectURL(scriptBlob);
    return blobURL;
}

async function importScriptFromNetwork(url) {
    const text= await fetchScript(url);

    // Create a Blob with the text content and MIME type "text/javascript".
    const blob = createScriptBlob(text);

    // Create an object URL from the Blob.
    return createBlobURL(blob);
}

async function importJavaScriptFile(url) {
    const text= await fetchScript(url);

    // Create a Blob with the text content and MIME type "text/javascript".
    const blob = createScriptBlob(text);

    // Create an object URL from the Blob.
    const objectURL = createBlobURL(blob);

    // Create a new script element and set its src attribute to the object URL.
    const scriptElement = document.createElement("script");
    scriptElement.src = objectURL;

    // Add a listener to revoke the object URL when the script has loaded.
    scriptElement.addEventListener("load", () => {
        URL.revokeObjectURL(objectURL);
    });

    // Append the script element to the document to execute the JavaScript code.
    document.body.appendChild(scriptElement);
}

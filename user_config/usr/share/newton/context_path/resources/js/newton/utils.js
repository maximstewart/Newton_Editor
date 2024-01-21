// Message handler
const displayMessage = (message, type, timeout, msgWindow = "page-alert-zone") => {
    let alertField  = document.getElementById(msgWindow);
    let divElm      = document.createElement("DIV");
    let btnElm      = document.createElement("BUTTON");
    let spnElm      = document.createElement("SPAN");
    let textElm     = document.createTextNode(message);

    divElm.setAttribute("class", "alert alert-dismissible fade show alert-" + type);
    divElm.setAttribute("role", "alert");
    divElm.appendChild(textElm);
    btnElm.type     = "button";
    textElm         = document.createTextNode("X");
    btnElm.setAttribute("class", "btn-dark btn-close");
    btnElm.setAttribute("data-bs-dismiss", "alert");
    btnElm.setAttribute("aria-label", "close");
    spnElm.setAttribute("aria-hidden", "true");
    spnElm.appendChild(textElm);
    btnElm.appendChild(spnElm);
    divElm.appendChild(btnElm);
    alertField.appendChild(divElm);

    if (timeout > 0) {
        setTimeout(function () {
            clearChildNodes(alertField);
        }, timeout * 1000);
    }
}

const sendMessage = (topic, target, content) => {
    const messageBody = {
        "topic": topic,
        'target': target,
        "content": btoa(content)
    };

    messenger.backend.postMessage( JSON.stringify(messageBody) );
}

const getSHA256Hash = async (input) => {
    let textAsBuffer = new TextEncoder().encode(input);
    let hashBuffer   = await window.crypto.subtle.digest("SHA-256", textAsBuffer);
    let hashArray    = Array.from( new Uint8Array(hashBuffer) );
    let fhash         = hashArray.map(
        (item) => item.toString(16).padStart(2, "0")
    ).join("");

    return fhash;
};

const clearChildNodes = (parent) => {
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

const getSiblingElm = (elm) => {
    return ( isNotNullOrUndefined(elm.nextElementSibling) )
                        ?
                        elm.nextElementSibling
                        :
                        elm.previousElementSibling;
}

const isNotNullOrUndefined = (val) => {
    return (val !== undefined && val !== null)
}


// Cache Buster
const clearCache = () => {
    const rep = /.*\?.*/;
    let links     = document.getElementsByTagName('link'),
        scripts   = document.getElementsByTagName('script'),
        video     = document.getElementsByTagName('video'),
        process_scripts = false;

    for (let i = 0; i < links.length; i++) {
        let link = links[i],
        href = link.href;
        if(rep.test(href)) {
            link.href = href + '&' + Date.now();
        } else {
            link.href = href + '?' + Date.now();
        }

    }
    if(process_scripts) {
        for (let i = 0; i < scripts.length; i++) {
            let script = scripts[i],
            src = script.src;
            if(rep.test(src)) {
                script.src = src+'&'+Date.now();
            } else {
                script.src = src+'?'+Date.now();
            }
        }
    }
}
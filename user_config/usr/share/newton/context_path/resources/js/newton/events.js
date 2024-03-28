window.onload = (eve) => {
    console.log("Window Loaded...");

    console.log("Defining custom elements...");
    defineCustomElements();

    console.log("Loading LSP client files...");
    loadLSPClientJSFiles();

    console.log("Loading editor...");
    loadEditor();
    loadPreviewEditor();
    loadInitialSession();
    loadStartingFiles();
}


const defineCustomElements = () => {
    customElements.define("input-list", InputList, { extends: 'ul' });
    customElements.define("input-list-item", InputListItem, { extends: 'li' });
}

const loadLSPClientJSFiles = () => {
    sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = LSP_SERVER_CONFG, content = "");
    sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = `${BASE_LINK}/ace-linters.js`, content = "");
    sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = `${BASE_LINK}/base-service.js`, content = "");
    sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = `${BASE_LINK}/service-manager.js`, content = "");
    sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = `${BASE_LINK}/language-client.js`, content = "");

    // Note: If using builtin services tghan connecting to a socket.
    // sendMessage(topic = "load_javascript", ftype = "", fhash = "", fpath = `${BASE_LINK}/python-service.js`, content = "");
}

window.onerror = function(msg, url, line, col, error) {
    // Note that col & error are new to the HTML 5 spec and may not be supported in every browser.
    const suppressErrorAlert = false;
    let extra = !col ? '' : '\ncolumn: ' + col;
    extra += !error ? '' : '\nerror: ' + error;
    const data = `Error:  ${msg} \nurl: ${url} \nline: ${line}  ${extra}`;

    sendMessage("error", "", data)

    // If you return true, then error alerts (like in older versions of Internet Explorer) will be suppressed.
    return suppressErrorAlert;
};


document.addEventListener("keyup", (eve) => {
    switch (eve.key) {
        case "ArrowUp":
            setLabels();
            break;
        case "ArrowDown":
            setLabels();
            break;
        case "ArrowLeft":
            setLabels();
            break;
        case "ArrowRight":
            setLabels();
            break;
        case "Enter":
            if ( isNotNullOrUndefined(previewSel) ) {
                let event = new MouseEvent('dblclick', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true
                  });

                previewSel.dispatchEvent(event);
            }
            break
        case "Control":
            isControlDown = false;
            break;
        case "b":
            if (isControlDown) {
                if ( isNotNullOrUndefined(previewSel) ) {
                    clearChildNodes(previewSel.parentElement);
                    $('#buffers-modal').modal("toggle");
                    previewSel  = null;
                    editor.focus();
                } else {
                    listOpenBuffers();
                }
            }
            break;
        default:
            setLabels();
            break
    }
});


document.addEventListener("keydown", (eve) => {
    switch (eve.key) {
        case "ArrowUp":
            if ( isNotNullOrUndefined(previewSel) ) {
                eve.preventDefault();
                selectPriorPreview();
            }
            break;
        case "ArrowDown":
            if ( isNotNullOrUndefined(previewSel) ) {
                eve.preventDefault();
                selectNextPreview();
            }
            break;
        case "ArrowLeft":
            break;
        case "ArrowRight":
            break;
        case "Control":
            isControlDown = true;
            break;
        default:
            break
    }
});
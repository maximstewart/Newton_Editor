
const loadPreviewEditor = () => {
    ace.require("ace/ext/language_tools");

    previewEditor = ace.edit("preview-editor");
    // Note:  https://github.com/ajaxorg/ace/wiki/Configuring-Ace
    previewEditor.setOptions(editorOpts);

    // Note:  https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts
    previewEditor.commands.addCommands(editorCommands);

    previewEditor.setTheme("ace/theme/one_dark");
}

const loadEditor = () => {
    ace.require("ace/ext/language_tools");

    editor = ace.edit("editor");
    // Note:  https://github.com/ajaxorg/ace/wiki/Configuring-Ace
    editor.setOptions(editorOpts);

    // Note:  https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts
    editor.commands.addCommands(editorCommands);

    editor.setTheme("ace/theme/one_dark");
    
    editor.addEventListener("click", (eve) => {
        setLabels();
    });
}

const loadInitialSession = () => {
    newSession(null, editor.getSession());
}

const newSession = (eve = null, session = null) => {
    let ftype          = "buffer";
    let fhash          = Date.now().toString();
    let fpath          = ""
    session            = ( isNotNullOrUndefined(session) ) ? session : ace.createEditSession("");

    aceSessions[fhash] = {"ftype": ftype, "fname": "", "fpath": fpath, "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_buffer", ftype, fhash, fpath, "");
}

const switchSession = (fhash) => {
    ftype   = aceSessions[fhash]["ftype"];
    session = aceSessions[fhash]["session"];

    setSession(ftype, fhash, session);
}

const setSession = (ftype, fhash, session) => {
    currentSession = fhash;
    editor.setSession(session);

    if (ftype !== "buffer") {
        editor.session.setMode("ace/mode/" + ftype);
    }

    setLabels();
}

const updateSession = (fhash, ftype, fname, fpath) => {
    aceSessions[fhash]["ftype"] = ftype;
    aceSessions[fhash]["fname"] = fname;
    aceSessions[fhash]["fpath"] = fpath;
}

const closeSession = (fhash) => {
    let ftype = aceSessions["ftype"];
    let fpath = aceSessions["fpath"];

    delete aceSessions[fhash];
    sendMessage("close", ftype, fhash, fpath, "");
}

const removeSession = (fhash) => {
    delete aceSessions[fhash];
}

const loadFile = (ftype, fname, fpath, content, line = 0) => {
    let fhash          = Date.now().toString();
    session            = ace.createEditSession( atob(content) );
    aceSessions[fhash] = {"ftype": ftype, "fname": fname, "fpath": fpath, "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_file", ftype, fhash, fpath, fname);
}

const saveSession = (fhash) => {
    let ftype   = aceSessions[fhash]["ftype"];
    let fpath   = aceSessions[fhash]["fpath"];
    let session = aceSessions[fhash]["session"];
    let content = session.getValue();

    sendMessage("save", ftype, fhash, fpath, content);
}




const listOpenBuffers = () => {
    $('#buffers-modal').modal("toggle");

    let ulElm = document.getElementById('buffers-selection');
    let keys  = Object.keys(aceSessions);

    for (let i = 0; i < keys.length; i++) {
        let session = aceSessions[keys[i]];
        let liElm   = document.createElement("li");
        let fname   = aceSessions[keys[i]]["fname"];
        let fhash   = keys[i];

        liElm.innerText = ( fname === "" ) ? "buffer" : fname;
        liElm.classList.add("list-group-item");
        liElm.setAttribute("fhash", fhash);

        if (fhash === currentSession) {
            previewSel  = liElm;
            liElm.classList.add("bg-success");
            liElm.classList.add("bg-info");
        }


        liElm.addEventListener("click", (eve) => {
            if ( !isNotNullOrUndefined(previewSel) ) return;

            previewSel.classList.remove("bg-info");

            let fhash   = eve.target.getAttribute("fhash");
            let ftype   = aceSessions[fhash]["ftype"];
            let session = aceSessions[fhash]["session"];
            previewSel  = eve.target;

            previewEditor.setSession(session);

            if (ftype !== "buffer") {
                previewEditor.session.setMode("ace/mode/" + ftype);
            }

            previewSel.classList.add("bg-info");
        })

        liElm.addEventListener("dblclick", (eve) => {
            let fhash   = eve.target.getAttribute("fhash");
            let ftype   = aceSessions[fhash]["ftype"];
            let session = aceSessions[fhash]["session"];

            clearChildNodes(previewSel.parentElement);

            previewSel  = null;
            setSession(ftype, fhash, session);
            $('#buffers-modal').modal("toggle");
            editor.focus();
        })

        ulElm.appendChild(liElm);
    }
}


const selectPriorPreview = () => {
    let selectedElm = previewSel.previousElementSibling;
    if ( !isNotNullOrUndefined(selectedElm) ) {
        let childrenElms = previewSel.parentElement.children;
        selectedElm = childrenElms[childrenElms.length - 1];
    }

    selectedElm.click();
}

const selectNextPreview = () => {
    let selectedElm = previewSel.nextElementSibling;
    if ( !isNotNullOrUndefined(selectedElm) ) {
        let childrenElms = previewSel.parentElement.children;
        selectedElm = childrenElms[0];
    }

    selectedElm.click();
}


const setLabels = () => {
        let ftype  = aceSessions[currentSession]["ftype"];
        let fpath  = aceSessions[currentSession]["fpath"];
        let cursor = editor.selection.getCursor();
        let pos    = `${cursor.row + 1}:${cursor.column}`;

        sendMessage("set_info_labels", ftype, "", fpath, pos);
}



const zoomIn = () => {
    fontSize += 1;
    document.getElementById('editor').style.fontSize = `${fontSize}px`;
}

const zoomOut = () => {
    fontSize -= 1;
    document.getElementById('editor').style.fontSize = `${fontSize}px`;
}

const toggleLineHighlight = () => {
    highlightLine = !highlightLine;
    editor.setHighlightActiveLine(highlightLine);
}


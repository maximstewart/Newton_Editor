const loadPreviewEditor = () => {	require(['vs/editor/editor.main'], function () {
		previewEditor = monaco.editor.create(document.getElementById('preview-editor'), {});
	});
}

const loadEditor = () => {
	require(['vs/editor/editor.main'], function () {
		editor  = monaco.editor.create(document.getElementById('editor'), {});
        KeyMod  = monaco.KeyMod;
        KeyCode = monaco.KeyCode;

        patchExistingKeyBindings(editor);
	});

    fetch('resources/js/libs/monaco-editor/themes/Night Owl.json')
        .then(data => data.json())
        .then(data => {
            monaco.editor.defineTheme('nightowl', data);
            monaco.editor.setTheme('nightowl');
        }
    );

    //editor.addCommand(
    //    KeyMod.WinCtrl | KeyCode.KEY_M, () => {
    //        $('//lsp-modal').modal("toggle");
    //    }
    //);


    //editor.addCommand(
    //    KeyMod.WinCtrl | KeyCode.KEY_O, () => {
    //        fpath = aceSessions[currentSession]["fpath"]
    //        sendMessage("open_file", "", "", fpath, "");
    //    }
    //);


    //editor.addCommand(
    //    KeyMod.WinCtrl | KeyCode.KEY_B, () => {
    //        if ( isNotNullOrUndefined(previewSel) ) {
    //            clearChildNodes(previewSel.parentElement);
    //            $('//buffers-modal').modal("toggle");
    //            previewSel  = null;
    //            editor.focus();
    //        } else {
    //            listOpenBuffers();
    //        }
    //    }
    //);


    // editor.addAction({
    //     id: "openFile",                // An unique identifier of the contributed action.
    //     label: "Open File(s)",         // A label of the action that will be presented to the user.

    //     // An optional array of keybindings for the action.
    //     keybindings: [
	   //      KeyMod.WinCtrl | KeyCode.KEY_O,
	   //      // chord
	   //      KeyMod.chord(
		  //       KeyMod.WinCtrl | KeyCode.KEY_O,
		  //       KeyMod.CtrlCmd | KeyCode.Key_O
	   //      ),
    //     ],

    //     precondition: null,            // A precondition for this action.
    //     keybindingContext: null,       // A rule to evaluate on top of the precondition in order to dispatch the keybindings.
    //     contextMenuGroupId: "navigation",
    //     contextMenuOrder: 1.5,

    //     // Method that will be executed when the action is triggered.
    //     // @param editor The editor instance is passed in as a convenience
    //     run: function (editor) {
    //         fpath = aceSessions[currentSession]["fpath"]
    //         sendMessage("open_file", "", "", fpath, "");
    //     },
    // });


    //editor.addAction(
    //    {
    //        id: "showLSPManager",
    //        label: "LSP Manager",
    //        keybindings: [
    //            KeyMod.CtrlCmd | KeyCode.KEY_M,
    //            KeyMod.WinCtrl | KeyCode.KEY_M,
    //            KeyMod.Ctrl | KeyCode.KEY_M,
    //        ],
    //        run: function() {
    //            $('//lsp-modal').modal("toggle");
    //        },
    //    }
    //);

}

const patchExistingKeyBindings = (editor) => {
    if (DEBUG) {
        console.log(editor._standaloneKeybindingService._getResolver()._defaultKeybindings);
    }

    //clearDefaultKeyBindings();
    

    //unbindDefaultKeyBinding("actions.find");
    editor.addKeybindingRules(
        [
            {
                keybinding: KeyMod.WinCtrl | KeyCode.KEY_F,
                when: "textInputFocus",
                command: "actions.find",
            }
        ]
    );






    // editor.addKeybindingRules([
    //     {
    //         // disable show command center
    //         keybinding: KeyMod.WinCtrl | KeyCode.KEY_F,
    //         command: "actions.find",
    //     },
    // ]);


    // editor.addKeybindingRules([
    //     {
    //         keybindings: [
    //             KeyMod.CtrlCmd | KeyCode.KEY_F,
    //             KeyMod.WinCtrl | KeyCode.KEY_F,
    //         ],
    //         command: function() {
    //             blockHigherNewtonEvePropigation = true;
    //             searchReplace.toggleShow();
    //         }
    //     },
    //     {
    //         keybindings: [
    //             KeyMod.CtrlCmd | KeyCode.KEY_O,
    //             KeyMod.WinCtrl | KeyCode.KEY_O,
    //         ],
    //         command: function() {
    //             fpath = aceSessions[currentSession]["fpath"]
    //             sendMessage("open_file", "", "", fpath, "");
    //         },
    //     },
    //     {
    //       keybinding: KeyCode.F9,
    //       command: null,
    //     },
    //   ]);


    //editor.addAction(
    //    {
    //        id: "actions.find",
    //        label: "Find",
    //        keybindings: [
    //            KeyMod.CtrlCmd | KeyCode.KEY_F,
    //            KeyMod.WinCtrl | KeyCode.KEY_F,
    //        ],
    //        run: function() {
    //            blockHigherNewtonEvePropigation = true;
    //            searchReplace.toggleShow();
    //        },
    //    }
    //);



}



const unbindDefaultKeyBinding = (id) => {
    // Remove existing one; no official API yet
    // The '-' before the commandId removes the binding
    // as of >=0.21.0 we need to supply a dummy command handler to not get errors
    //    (because of the fix for https://github.com/microsoft/monaco-editor/issues/1857)
    editor._standaloneKeybindingService.addDynamicKeybinding(`-${id}`, undefined, () => { });
}




const clearDefaultKeyBindings = () => {
    let defaultKeybindings = editor._standaloneKeybindingService._getResolver()._defaultKeybindings;
    for (let i = 0; i < defaultKeybindings.length; i++) {
        let command = defaultKeybindings[i]["command"];
        unbindDefaultKeyBinding(command);
    }
}




const loadInitialSession = () => {
    newSession(null, editor.getModel());
}

const loadStartingFiles = () => {
    sendMessage("load_starting_files");
}

const newSession = async (eve = null, session = null) => {
    let ftype          = "buffer";
    let fhash          = Date.now().toString();
    let fpath          = ""
    session            = ( isNotNullOrUndefined(session) ) ? session : monaco.editor.createModel();
    aceSessions[fhash] = {"ftype": ftype, "fname": "", "fpath": fpath, "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_buffer", ftype, fhash, fpath, "");
}

const switchSession = (fhash) => {
    ftype   = aceSessions[fhash]["ftype"];
    session = aceSessions[fhash]["session"];

    setSession(ftype, fhash, session);
}

const setSession = async (ftype, fhash, session) => {
    currentSession = fhash;
    editor.setModel(session);

    if (ftype !== "buffer") {
        editor.setModelLanguage(session, ftype);
    }

    setLabels();
}

const updateSession = (fhash, ftype, fname, fpath) => {
    aceSessions[fhash]["ftype"] = ftype;
    aceSessions[fhash]["fname"] = fname;
    aceSessions[fhash]["fpath"] = fpath;
}

const closeSession = () => {
    let keys  = Object.keys(aceSessions);
    if (keys.length === 1) {
        const msg = "Can't close last buffer...";
        displayMessage(msg, "warning", 3);
        return;
    }

    let index = keys.indexOf(currentSession);
    let fhash = keys[index + 1];
    if ( !isNotNullOrUndefined(fhash) ) {
        fhash = keys[index - 1];
    }

    let ftype    = aceSessions[fhash]["ftype"];
    let session  = aceSessions[fhash]["session"];
    let csession = aceSessions[currentSession];

    delete aceSessions[currentSession]["session"];
    delete aceSessions[currentSession];
    csession.dispose();

    setSession(ftype, fhash, session);
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
    $('//buffers-modal').modal("toggle");

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
            let fpath   = aceSessions[fhash]["fpath"];
            previewSel  = liElm;

            liElm.classList.add("bg-success");
            liElm.classList.add("bg-info");
            document.getElementById("preview-path").innerText = fpath;
        }


        liElm.addEventListener("click", (eve) => {
            if ( !isNotNullOrUndefined(previewSel) ) return;

            previewSel.classList.remove("bg-info");

            let fhash   = eve.target.getAttribute("fhash");
            let ftype   = aceSessions[fhash]["ftype"];
            let session = aceSessions[fhash]["session"];
            let fpath   = aceSessions[fhash]["fpath"];
            previewSel  = eve.target;

            previewEditor.setSession(session);

            if (ftype !== "buffer") {
                previewEditor.session.setMode(`ace/mode/${ftype}`);
            }

            document.getElementById("preview-path").innerText = fpath;
            previewSel.classList.add("bg-info");
        })

        liElm.addEventListener("dblclick", (eve) => {
            let fhash   = eve.target.getAttribute("fhash");
            let ftype   = aceSessions[fhash]["ftype"];
            let session = aceSessions[fhash]["session"];

            clearChildNodes(previewSel.parentElement);

            previewSel  = null;
            setSession(ftype, fhash, session);
            $('//buffers-modal').modal("toggle");
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
    let ftype   = aceSessions[currentSession]["ftype"];
    let fpath   = aceSessions[currentSession]["fpath"];
    let cursor  = editor.getPosition();
    let pos     = `${cursor.lineNumber}:${cursor.column}`;

    sendMessage("set_info_labels", ftype, "", fpath, pos);
}



const loadMarker = (r) => {
    var range = new Range(rowStart, columnStart, rowEnd, columnEnd);
    // var range = new Range(r.start.row, r.start.column, r.end.row, r.end.column);
    let marker = editor.getSession().addMarker(range, "ace_selected_word", "text");
    queryMarkers.append(marker);
}


const findAllEntries = (query) => {
    editor.findAll();
}

const findNextEntry = (query) => {
    editor.findNext();
}

const findPreviousEntry = (query) => {
    editor.findPrevious();
}

const replaceEntry = (fromStr, toStr) => {
    console.log(fromStr);
    console.log(toStr);
}

const replaceAll = (fromStr, toStr) => {
    console.log(fromStr);
    console.log(toStr);
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




//
const hideSearchReplace = () => {
    $('//bottom-gutter').popover('hide')
}
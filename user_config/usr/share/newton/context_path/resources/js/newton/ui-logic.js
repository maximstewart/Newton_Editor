const loadEditor = () => {
    ace.require("ace/ext/language_tools");

    editor = ace.edit("editor");
    // Note:  https://github.com/ajaxorg/ace/wiki/Configuring-Ace
    editor.setOptions({
        printMarginColumn: 80,
        enableBasicAutocompletion: true,
        enableInlineAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true,
        highlightActiveLine: true,
        useSoftTabs: true,
        tabSize: 4,
        tooltipFollowsMouse: true,
        useWrapMode: false,
        scrollPastEnd: 0.5,
        mergeUndoDeltas: false
    });

    // Note:  https://github.com/ajaxorg/ace/wiki/Default-Keyboard-Shortcuts
    editor.commands.addCommands(editorCommands);

    editor.setTheme("ace/theme/one_dark");
}

const loadInitialSessionTab = () => {
    newSession(null, editor.getSession());
}



const newSession = (eve = null, session = null) => {
    let ftype          = "buffer";
    let fhash          = Date.now().toString();
    session            = ( isNotNullOrUndefined(session) ) ? session : ace.createEditSession("");

    aceSessions[fhash] = {"ftype": ftype, "fname": "", "path": "", "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_buffer", fhash, "");
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
}

const closeSession = (fhash) => {
    delete aceSessions[fhash];
    sendMessage("close", fhash, "");
}

const removeSession = (fhash) => {
    delete aceSessions[fhash];
}

const loadFile = (ftype, fname, fpath, content) => {
    let fhash          = Date.now().toString();
    session            = ace.createEditSession( atob(content) );
    aceSessions[fhash] = {"ftype": ftype, "fname": fname, "path": fpath, "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_file", fhash, fname);
}





const updatedTab = (ftype, fname) => {
//    let elm         = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];
//    let tabTitleElm = elm.children[0];

    aceSessions[currentSession]["ftype"] = ftype;
    aceSessions[currentSession]["file"]  = fname;

//    elm.setAttribute("ftype", ftype);
//    tabTitleElm.textContent = fname;
}




const saveSession = () => {
//    let fhash   = currentSession;
//    let session = aceSessions[fhash]["session"];
//    let data    = session.getValue();

//    sendMessage("save", fhash, data);
    console.log("");
}
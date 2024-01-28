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

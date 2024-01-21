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

const loadInitialSessionTab = async () => {
    newSession(null, editor.getSession());
}

const newSession = async (elm = null, session = null) => {
    let ftype          = "buffer";
    let fhash          = await getSHA256Hash( new Date().toString() );
    session            = ( isNotNullOrUndefined(session) ) ? session : ace.createEditSession("");

    aceSessions[fhash] = {"ftype": ftype, "file": "", "session": session};

    setSession(ftype, fhash, session);
    sendMessage("load_buffer", fhash, "");
}

const switchSession = (fhash) => {
    ftype   = aceSessions[fhash]["ftype"];
    session = aceSessions[fhash]["session"];

    setSession(ftype, fhash, session);
}


const closeSession = (fhash) => {
    delete aceSessions[fhash];
    
    keys = Object.keys(aceSessions);
    console.log(keys.length);
}


const setSession = (ftype, fhash, session) => {
    currentSession = fhash;
    editor.setSession(session);

    if (ftype !== "buffer") {
        editor.session.setMode("ace/mode/" + ftype);
    }
}


























const loadFile = (ftype, fhash, file, content) => {
    session = ace.createEditSession( atob(content) );
    aceSessions[fhash] = {"ftype": ftype, "file": file, "session": session};

//    let tab = `
//        <li class='tab active-tab' role="presentation" fhash='${fhash}' ftype='${ftype}' draggable="true"
//            ondragend="dragEnd()" ondragover="dragOver(event)" ondragstart="dragStart(event)"
//        >
//            <span class='file-name' onclick='switchSession(this)'>${file}</span>
//            <span class='close-button' onclick='closeSession(this)'>
//                <i class="bi bi-x-square" aria-hidden="true"></i>
//            </span>
//        </li>
//    `;

    // TODO: Need to account for given editor we have focused when implimented...
//    document.getElementsByClassName("nav-tabs")[0]
//            .insertAdjacentHTML('beforeend', tab);

    setSession(ftype, fhash, session);
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
    let fhash   = currentSession;
    let session = aceSessions[fhash]["session"];
    let data    = session.getValue();

    sendMessage("save", fhash, data);
}
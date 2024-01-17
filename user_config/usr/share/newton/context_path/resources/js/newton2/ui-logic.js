const loadFile = (ftype, fhash, file, content) => {
    session = ace.createEditSession( atob(content) );
    aceSessions[fhash] = {"ftype": ftype, "file": file, "session": session};

    let tab = `
        <li class='tab active-tab' role="presentation" fhash='${fhash}' ftype='${ftype}' draggable="true"
            ondragend="dragEnd()" ondragover="dragOver(event)" ondragstart="dragStart(event)"
        >
            <span class='file-name' onclick='switchSession(this)'>${file}</span>
            <span class='close-button' onclick='closeSession(this)'>
                <i class="bi bi-x-square" aria-hidden="true"></i>
            </span>
        </li>
    `;

    // TODO: Need to account for given editor we have focused when implimented...
    document.getElementsByClassName("nav-tabs")[0]
            .insertAdjacentHTML('beforeend', tab);

    setSession(ftype, fhash, session);
}

const updatedTab = (ftype, fname) => {
    let elm         = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];
    let tabTitleElm = elm.children[0];

    aceSessions[currentSession]["ftype"] = ftype;
    aceSessions[currentSession]["file"]  = fname;

    elm.setAttribute("ftype", ftype);
    tabTitleElm.textContent = fname;
}



const loadInitialSessions = () => {
    let elms = document.getElementsByClassName("add-session-bottom");
    for (let i = 0; i < elms.length; i++) {
        elms[i].click();
    }
}

const newSession = async (elm) => {
    let ftype   = "buffer";
    let fhash   = await getSHA256Hash( new Date().toString() );
    let session = ace.createEditSession("");

    let tab = `
        <li class='tab active-tab' role="presentation" fhash='${fhash}' ftype='${ftype}' draggable="true"
            ondragend="dragEnd()" ondragover="dragOver(event)" ondragstart="dragStart(event)"
        >
            <span class='file-name' onclick='switchSession(this)'>buffer</span>
            <span class='close-button' onclick='closeSession(this)'>
                <i class="bi bi-x-square" aria-hidden="true"></i>
            </span>
        </li>
    `;

    aceSessions[fhash] = {"ftype": "buffer", "file": "", "session": session};
    let container  = elm.parentElement.parentElement.parentElement;
    let tabs       = container.children[0].children[0];

    tabs.insertAdjacentHTML('beforeend', tab);
    setSession(ftype, fhash, session);
}

const saveSession = () => {
    let fhash   = currentSession;
    let session = aceSessions[fhash]["session"];
    let data    = session.getValue();

    sendMessage("save", fhash, data);
}

const setSession = (ftype, fhash, session) => {
    if (currentSession) {
        let currentElm = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];
        currentElm.classList.remove("active-tab");
    }

    currentSession = fhash;
    let currentElm = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];

    currentElm.classList.add("active-tab");
    editor.setSession(session);

    if (ftype !== "buffer") {
        editor.session.setMode("ace/mode/" + ftype);
    }
}

const switchSession = (elm) => {
    let parentElm = elm.parentElement;
    let ftype   = parentElm.getAttribute("ftype");
    let fhash   = parentElm.getAttribute("fhash");
    let session = aceSessions[fhash]["session"];

    setSession(ftype, fhash, session);
}

const closeSession = (elm) => {
    let keys = Object.keys(aceSessions);
    if (keys.length < 2) return

    let parentElm  = elm.parentElement;
    let ftype      = parentElm.getAttribute("ftype");
    let fhash      = parentElm.getAttribute("fhash");

    if (ftype !== "buffer") {
        sendMessage("close", fhash, "");
    }

    if (fhash === currentSession) {
        let siblingElm = getSiblingElm(parentElm);

        if ( isNotNullOrUndefined(siblingElm) ) {
            let sftype = siblingElm.getAttribute("ftype");
            let sfhash = siblingElm.getAttribute("fhash");

            setSession(sftype, sfhash, aceSessions[sfhash]["session"]);
        }
    }

    parentElm.remove();
    delete aceSessions[fhash];

}
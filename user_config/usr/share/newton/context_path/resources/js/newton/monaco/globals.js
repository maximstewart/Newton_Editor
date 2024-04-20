const DEBUG = true;

const QueryState = {
    Searching: 0,
    SearchSuccess: 1,
    SearchFail: 2
};


const EDITOR_OPTS   = {
    autoIndent: 'full',
    contextmenu: true,
    fontFamily: 'monospace',
    fontSize: 13,
    lineHeight: 24,
    hideCursorInOverviewRuler: true,
    matchBrackets: 'always',
    minimap: {
      enabled: true,
    },
    scrollbar: {
      horizontalSliderSize: 4,
      verticalSliderSize: 18,
    },
    selectOnLineNumbers: true,
    roundedSelection: false,
    readOnly: false,
    cursorStyle: 'line',
    automaticLayout: true,
};



const BASE_LINK        = `${window.location.href}resources/js/libs/ace_editor/lsp`;
const LSP_SERVER_CONFG = `${window.location.href}../lsp-servers-config.json`;
const BASE_LSP_LINK    = "http://0.0.0.0:3030";

let KeyMod             = null;
let KeyCode            = null;

const SCRIPT_BLOB_URLs = {};
let lspProvider        = null;
let lspServersConfig   = null;
let lspSettingsUI      = document.getElementById('lsp-settings');


let searchReplace    = null;
let editor           = null;
let previewEditor    = null;
let aceSessions      = {};
let currentSession   = null;
let previewSel       = null;
let fontSize         = 12;
let highlightLine    = true;
let isControlDown    = false;
let queryMarkers     = [];


let blockHigherNewtonEvePropigation = false;



const messenger   = (window.webkit) ? window.webkit.messageHandlers : {"backend": {"postMessage": (message) => {
    let json      = JSON.parse(message);
    let topic     = json["topic"];

    if (topic === "load_javascript") {
        let elm  = document.createElement("SCRIPT");
        elm.src  = json["fpath"];

        document.body.append(elm);
        return;
    }

    if (topic === "load_json"
        // &&
        // json["fpath"].includes("lsp-servers-config.json")
    ) {
        fetch( json["fpath"] )
        .then((response) => response.json())
        .then((response) => {
            lspServersConfig = response;
            loadSettingsFileToUI();
        });
        return;
    }

    if (topic === "load_starting_files") {
        return;
    }

    if (topic === "set_info_labels") {
        return;
    }

    if (topic === "load_buffer") {
        return;
    }

    if (topic === "open_file") {
        return;
    }

    console.log("Message Backend: " + message);
}
}};
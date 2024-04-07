const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};


const EDITOR_OPTS   = {
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
    }


const BASE_LINK        = `${window.location.href}resources/js/libs/ace_editor/lsp`;
const LSP_SERVER_CONFG = `${window.location.href}../lsp-servers-config.json`;
const BASE_LSP_LINK    = "http://0.0.0.0:4880";

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
const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};

const editorOpts   = {
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


let PythonMode     = null;
//let PythonMode = ace.require("ace/mode/python").Mode;


let editor         = null;
let previewEditor  = null;
let aceSessions    = {};
let currentSession = null;
let previewSel     = null;
let fontSize       = 12;
let highlightLine  = true;
let isControlDown  = false;
let queryMarkers   = [];
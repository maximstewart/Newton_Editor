const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};

let aceSessions    = {};
let currentSession = null;



window.onload = (eve) => {
    console.log("Loaded...");
    loadInitialSessions();
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





ace.require("ace/ext/language_tools");
let StatusBar = ace.require('ace/ext/statusbar').StatusBar;


let editor = ace.edit("editor");
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
const statusBar = new StatusBar(editor, document.getElementById('status-bar'));
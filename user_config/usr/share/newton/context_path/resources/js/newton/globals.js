const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};

let editor         = null;
let previewEditor  = null;
let aceSessions    = {};
let currentSession = null;
let previewSel     = null;
let isControlDown  = false;
const messenger  = (window.webkit) ? window.webkit.messageHandlers : (message) => {
    console.log("Message: " + message);
};

let editor         = null;
let aceSessions    = {};
let currentSession = null;

const editorCommands = [
    {
        name: "showSettingsMenu",
        bindKey: {win: "Ctrl-Shift-m", mac: "Ctrl-Shift-m"},
        exec: function(editor) {
            ace.config.loadModule("ace/ext/settings_menu", function(module) {
                module.init(editor);
                editor.showSettingsMenu();
            })
        }
    }, {
        name: "showKeyboardShortcuts",
        bindKey: {win: "ctrl-shift-h", mac: "command-shift-h"},
        exec: function(editor) {
            ace.config.loadModule("ace/ext/keybinding_menu", function(module) {
                module.init(editor);
                editor.showKeyboardShortcuts();
            })
        }
    }, {
        name: "saveSession",
        bindKey: {win: "ctrl-s", mac: "ctrl-s"},
        exec: function(editor) {
            saveSession();
        },
        readOnly: true
    }, {
        name: "newSession",
        bindKey: {win: "ctrl-t", mac: "ctrl-t"},
        exec: function(editor) {
            let elm = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];
            newSession(elm);
        },
        readOnly: true
    }, {
        name: "closeSession",
        bindKey: {win: "ctrl-w", mac: "ctrl-w"},
        exec: function(editor) {
            let elm = document.querySelectorAll(`[fhash="${currentSession}"]`)[0];
            closeSession(elm.children[1]);
        },
        readOnly: true
    }, {
        name: "movelinesUp",
        bindKey: {win: "ctrl-up", mac: "ctrl-up"},
        exec: function(editor) {
            editor.execCommand("movelinesup");
        },
        readOnly: true
    }, {
        name: "movelinesDown",
        bindKey: {win: "ctrl-down", mac: "ctrl-down"},
        exec: function(editor) {
            editor.execCommand("movelinesdown");
        },
        readOnly: true
    }, {
        name: "scrollUp",
        bindKey: {win: "alt-up", mac: "alt-up"},
        exec: function(editor) {
            editor.execCommand("scrollup");
        },
        readOnly: true
    }, {
        name: "scrollDown",
        bindKey: {win: "alt-down", mac: "alt-down"},
        exec: function(editor) {
            editor.execCommand("scrolldown");
        },
        readOnly: true
    }


];

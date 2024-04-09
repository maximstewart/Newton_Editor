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
        name: "openCommandPalette2",
        bindKey: {linux: "Command-Shift-/|F1", win: "Ctrl-Shift-/|F1"},
        exec: function(editor) {
            editor.execCommand("openCommandPalette");
        }
    }, {
        name: "showLSPManager",
        bindKey: {win: "ctrl-m", mac: "command-m"},
        exec: function(editor) {
            $('#lsp-modal').modal("toggle");
        }
    }, {
        name: "search",
        bindKey: {win: "ctrl-f", mac: "ctrl-f"},
        exec: function(editor) {
            blockHigherNewtonEvePropigation = true;
            searchReplace.toggleShow();
        },
        readOnly: true
    }, {
        name: "openFile",
        bindKey: {win: "ctrl-o", mac: "ctrl-o"},
        exec: function(editor) {
            fpath = aceSessions[currentSession]["fpath"]
            sendMessage("open_file", "", "", fpath, "");
        },
        readOnly: true
    }, {
        name: "saveSession",
        bindKey: {win: "ctrl-s", mac: "ctrl-s"},
        exec: function(editor) {
            saveSession(currentSession);
        },
        readOnly: true
    }, {
        name: "newSession",
        bindKey: {win: "ctrl-t", mac: "ctrl-t"},
        exec: function(editor) {
            newSession();
        },
        readOnly: true
    }, {
        name: "closeSession",
        bindKey: {win: "ctrl-w", mac: "ctrl-w"},
        exec: function(editor) {
            closeSession(currentSession);
        },
        readOnly: true
    }, {
        name: "toggleLineHighlight",
        bindKey: {win: "ctrl-h", mac: "ctrl-h"},
        exec: function(editor) {
            toggleLineHighlight();
        },
        readOnly: true
    }, {
        name: "gotoDefinition",
        bindKey: {win: "ctrl-g", mac: "ctrl-g"},
        exec: function(editor) {
            console.log("Goto stub...");
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
        name: "tgglTopMainMenubar",
        bindKey: {win: "ctrl-0", mac: "ctrl-0"},
        exec: function(editor) {
            sendMessage("tggl_top_main_menubar", "", "", "", "");
        },
        readOnly: true
    }, {
        name: "zoomIn",
        bindKey: {win: "ctrl-=", mac: "ctrl-="},
        exec: function(editor) {
            zoomIn();
        },
        readOnly: true
    }, {
        name: "zoomOut",
        bindKey: {win: "ctrl--", mac: "ctrl--"},
        exec: function(editor) {
            zoomOut();
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
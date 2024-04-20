/* Works but isn't websocket */
// manager.registerService("python", {
//     module: () => {
//         importScripts( "${ SCRIPT_BLOB_URLs["python-service.js"] }" );
//         return {PythonService};
//     },
//     className: "PythonService",
//     modes: "python|python3",
// });



                            // modes: "python|python3",
const loadPythonLSPFromBlobURLs = () => {
    importJavaScriptFileFromBlobURL( SCRIPT_BLOB_URLs["ace-linters.js"] ).then(
        async () => {
            let workerString = `
                !function () {
                    importScripts( "${ SCRIPT_BLOB_URLs["service-manager.js"] }" );
                    let manager = new ServiceManager(self);

                    /* Works and is websocket */
                    manager.registerServer(
                        "python", {
                            module: () => {
                                importScripts( "${ SCRIPT_BLOB_URLs["language-client.js"] }" );
                                return {LanguageClient};
                            },
                            modes: "python",
                            type: "socket", // "socket|worker"
                            socket: new WebSocket( "${ lspServersConfig['python3']['socket'] }" ),
                            initializationOptions: ${ JSON.stringify( lspServersConfig['python3']['initialization-options'] ) }
                        }
                    );
                }()
            `;

            let worker   = new Worker(
                createBlobURL(
                    createScriptBlob(workerString)
                )
            );

            lspProvider = LanguageProvider.create(worker);
            lspProvider.registerEditor(editor);
        }
    ).catch((e) => {
        console.log(e);
    });
}


const loadPythonLSPFromNetwork = () => {
    importJavaScriptFile(BASE_LSP_LINK + "/ace-linters.js").then(
        async () => {
            let workerString = `
                !function () {
                    importScripts("${await importScriptFromNetwork(BASE_LSP_LINK + "/service-manager.js")}");
                    let manager = new ServiceManager(self);

                    /* Works and is websocket */
                    manager.registerServer("python", {
                        module: () => {
                            importScripts("${await importScriptFromNetwork(BASE_LSP_LINK + "/language-client.js")}");
                            return {LanguageClient};
                        },
                        modes: "python|python3",
                        type: "socket", // "socket|worker"
                        socket: new WebSocket( "${ lspServersConfig['python']['socket'] }" ),
                        initializationOptions: ${ JSON.stringify( lspServersConfig['python']['initialization-options'] ) }
                    });
                }()
            `;

            let worker   = new Worker(
                createBlobURL(
                    createScriptBlob(workerString)
                )
            );

            lspProvider = LanguageProvider.create(worker);
            lspProvider.registerEditor(editor);
        }
    ).catch((e) => {
        console.log(e);
    });

}


const loadSettingsFileToUI = async () => {
    let config    = lspServersConfig;
    let languages = Object.keys(config);

    clearChildNodes(lspSettingsUI);
    for (let i = 0; i < languages.length; i++) {
        let elm  = document.createElement("lsp-config");
        let lang = languages[i];

        elm.setTitle(lang);
        lspSettingsUI.appendChild( elm );

        generateElement(config[lang], "", elm);
    }

}


const saveSettingsFileFromUI = () => {
    console.log("Stub...");
}


const generateElement = (config = {}, parent = "", elm = null) => {
    const proto = Object.getPrototypeOf(config);

    switch (proto) {
        case String.prototype:
            handleString(config, parent, elm);

            break;
        case Array.prototype:
            handleList(config, parent, elm);

            break;
        case Boolean.prototype:
            handleBoolean(config, parent, elm);

            break;
        case Number.prototype:
            console.log("Number generatable HTML type stub...");
            break;
        case Map.prototype:
            console.log("Map generatable HTML type stub...");

            break;
        default:
            if ( isDict(config) ) {
                handleDictionary(config, parent, elm);

                break;
            }

            console.log("No generatable HTML type...");
            console.log(`config: ${config}\nparent: ${parent}\nelm: ${elm}`);
    }

}


const handleDictionary = (config, parent, elm) => {
    let listElm = document.createElement("input-dict");
    let keys    = Object.keys(config);
    listElm.setTitle( parent );

    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];

        generateElement(config[key], key, listElm);
    }

    elm.append(listElm);
    return elm;
}

const handleList = (config, parent, elm) => {
    let listElm = document.createElement("input-list");
    listElm.setTitle( parent );

    for (var i = 0; i < config.length; i++) {
        let inputElm = document.createElement("input-list-item");

        inputElm.setText( config[i] );
        listElm.append(inputElm);
    }

    elm.append(listElm);
    return elm;
}

const handleString = (config, parent, elm) => {
    let inputElm = document.createElement("input-list-item");

    inputElm.setTitle(parent);
    inputElm.setText(config);
    elm.append(inputElm);
}

const handleBoolean = (config, parent, elm) => {
    let inputElm = document.createElement("input-checkbox");

    inputElm.setTitle(parent);
    (config === true) ? inputElm.on() : inputElm.off();

    elm.append(inputElm);
}
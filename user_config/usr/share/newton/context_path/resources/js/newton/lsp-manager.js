/* Works but isn't websocket */
// manager.registerService("python", {
//     module: () => {
//         importScripts( "${ SCRIPT_BLOB_URLs["python-service.js"] }" );
//         return {PythonService};
//     },
//     className: "PythonService",
//     modes: "python|python3",
// });



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
                            modes: "python|python3",
                            type: "socket", // "socket|worker"
                            socket: new WebSocket( "${ lspServersConfig['python']['socket'] }" ),
                            initializationOptions: ${ JSON.stringify( lspServersConfig['python']['initialization_options'] ) }
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
                        initializationOptions: ${ JSON.stringify( lspServersConfig['python']['initialization_options'] ) }
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
    generateElement(lspServersConfig);

    // let config = lspServersConfig;
    // let keys = Object.keys(lspServersConfig);

    // for (let i = 0; i < languages.length; i++) {
    //     let elm  = document.createElement("lsp-config");
    //     let lang = languages[i];

    //     elm.setTitle(lang);
    //     lspSettingsUI.appendChild( elm );

    //     generateElement(lang, elm, lspServersConfig[lang]);
    // }

}


const saveSettingsFileFromUI = () => {

}


const generateElement = (config = {}, parent = "", elm = null) => {
    const proto = Object.getPrototypeOf(config)
    console.log(config, parent, elm);

    switch (proto) {
        case String.prototype:
            handleString(config, elm);

            // lspSettingsUI.appendChild( target );

            break;
        case Array.prototype:
            handleList(config, elm);

            // lspSettingsUI.appendChild( target );

            break;
        case Boolean.prototype:

            break;
        case Map.prototype:

            break;
        default:
            if ( isDict(config) ) {
                if (parent === "" && elm === null) {
                    handleRoot(config);
                    // let elm  = document.createElement("lsp-config");
                    // let lang = languages[i];

                    break;
                }

                handleDictionary(config, elm);

                // target = handleDictionary(config, elm);
                // lspSettingsUI.appendChild( target );
                // let elm  = document.createElement("lsp-config");
                // let lang = languages[i];

                break;
            }

            console.log("No generatable HTML type...")
    }

}




const handleRoot = (config) => {
    let keys = Object.keys(config);

    for (let i = 0; i < keys.length; i++) {
        let elm = document.createElement("lsp-config");
        let key = keys[i];

        elm.setTitle(key);
        lspSettingsUI.appendChild( elm );

        generateElement(config[key], key, elm);
    }

}


const handleDictionary = (config, elm) => {
    let keys = Object.keys(config);

    for (let i = 0; i < keys.length; i++) {
        let key = keys[i];

        generateElement(config[key], key, elm);
    }
}

const handleList = (config, elm) => {
    let listElm = document.createElement("input-list");

    for (var i = 0; i < config.length; i++) {
        let inputElm = document.createElement("input-list-item");
        inputElm.setText( config[i] );
        listElm.append(inputElm);
    }

    elm.append(listElm);

    return elm;
}

const handleString = (config, elm) => {
    console.log(config, elm);
    let inputElm = document.createElement("input-list-item");

    inputElm.setTitle(parent);
    inputElm.setText(config);
    elm.append(inputElm);
}
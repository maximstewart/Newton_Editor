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
    let languages = Object.keys(lspServersConfig);

    for (let i = 0; i < languages.length; i++) {
        let lang = languages[i];
        let elm  = document.createElement("input-list");

        elm.setTitle(lang);
        lspSettingsUI.appendChild( elm );

        generateElement(lang, elm, lspServersConfig[lang]);
    }

}


const saveSettingsFileFromUI = () => {

}


const generateElement = (parent, elm, config) => {
    const proto = Object.getPrototypeOf(config)

    switch (proto) {
        case String.prototype:
            let inputElm = document.createElement("input-list-item");
            inputElm.setTitle(parent);
            inputElm.setText(config);
            elm.append(inputElm);

            break;
        case Array.prototype:
            let inputListElm = document.createElement("input-list");
            for (var i = 0; i < config.length; i++) {
                let inputElm = document.createElement("input-list-item");
                inputElm.setText( config[i] );
                inputListElm.append(inputElm);
            }
            elm.append(inputListElm);

            break;
        case Boolean.prototype:

            break;
        case Map.prototype:

            break;
        default:
            if ( isDict(config) ) {
                let keys = Object.keys(config);

                for (let i = 0; i < keys.length; i++) {
                    let key = keys[i];
                    generateElement(key, elm, config[key] );
                }

                break;
            }

            console.log("No generatable HTML type...")
    }

}

const isDict = (dict) => {
    return typeof dict === "object" && !Array.isArray(dict);
};
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

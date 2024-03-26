/* Works but isn't websocket */
// manager.registerService("python", {
//     module: () => {
//         importScripts( "${ scriptBlobURLs["python-service.js"] }" );
//         return {PythonService};
//     },
//     className: "PythonService",
//     modes: "python|python3",
// });

// importScripts("${await importScriptFromNetwork(baseLink + "/service-manager.js")}");
// importScripts("${await importScriptFromNetwork(baseLink + "/python-service.js")}");
// importScripts("${await importScriptFromNetwork(baseLink + "/language-client.js")}");



// initializationOptions: {
//     "pylsp.plugins.rope_autoimport.enabled": true,
//     "pylsp.plugins.rope_completion.enabled": true,
//     "pylsp.plugins.rope_completion.eager": true,
//     "pylsp.plugins.jedi_completion.fuzzy": true,
//     "pylsp.plugins.jedi.extra_paths": [
//         "/home/abaddon/Portable_Apps/py-venvs/flask-apps-venv/venv/lib/python3.10/site-packages",
//         "/home/abaddon/Portable_Apps/py-venvs/gtk-apps-venv/venv/lib/python3.10/site-packages/gi"
//     ]
// }

// "/home/abaddon/Portable_Apps/py-venvs/flask-apps-venv/venv/lib/python3.10/site-packages"


const loadPythonLSPFromBlobURLs = () => {
    importJavaScriptFileFromBlobURL( scriptBlobURLs["ace-linters.js"] ).then(
        async () => {
            let workerString = `
                !function () {
                    importScripts( "${ scriptBlobURLs["service-manager.js"] }" );
                    let manager = new ServiceManager(self);

                    /* Works and is websocket */
                    manager.registerServer("python", {
                        module: () => {
                            importScripts( "${ scriptBlobURLs["language-client.js"] }" );
                            return {LanguageClient};
                        },
                        modes: "python|python3",
                        type: "socket", // "socket|worker"
                        socket: new WebSocket("ws://127.0.0.1:3030/python"),
                        initializationOptions: {
                            "pylsp.plugins.rope_autoimport.enabled": true,
                            "pylsp.plugins.rope_completion.enabled": true,
                            "pylsp.plugins.rope_completion.eager": true,
                            "pylsp.plugins.jedi_completion.fuzzy": true,
                            "pylsp.plugins.jedi.extra_paths": [
                                "/home/abaddon/Portable_Apps/py-venvs/lsp_bridge-venv/venv/lib/python3.10/site-packages/gi-stubs"
                            ]
                        }
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


const loadPythonLSPFromNetwork = () => {
    importJavaScriptFile(baseLSPLink + "/ace-linters.js").then(
        async () => {
            let workerString = `
                !function () {
                    importScripts("${await importScriptFromNetwork(baseLSPLink + "/service-manager.js")}");
                    let manager = new ServiceManager(self);

                    /* Works and is websocket */
                    manager.registerServer("python", {
                        module: () => {
                            importScripts("${await importScriptFromNetwork(baseLSPLink + "/language-client.js")}");
                            return {LanguageClient};
                        },
                        modes: "python|python3",
                        type: "socket", // "socket|worker"
                        socket: new WebSocket("ws://127.0.0.1:3030/python"),
                        initializationOptions: {
                            "pylsp.plugins.jedi.extra_paths": [
                                "/home/abaddon/Portable_Apps/py-venvs/flask-apps-venv/venv/lib/python3.10/site-packages",
                                "/home/abaddon/Portable_Apps/py-venvs/gtk-apps-venv/venv/lib/python3.10/site-packages/gi"
                            ]
                        }
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

window.onload = (eve) => {
    loadEditor();
    loadInitialSessionTab();

    console.log("Window Loaded...");
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
const postAjaxController = (data, action) => {
    if (data.message) {
        message = data.message

        if (action == "someAction" && message.type.includes("success")) {
            console.log("Success!");
        }

        displayMessage(message.text, message.type, 0);
    }
}

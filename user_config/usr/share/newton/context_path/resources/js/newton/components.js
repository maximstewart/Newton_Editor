class InputListContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "input-list-template") {
        let template = document.getElementById(tag);
        let templateContent = template.content;

        const shadowRoot = this.attachShadow({ mode: "open" });
        shadowRoot.appendChild( templateContent.cloneNode(true) );
    }
    
    setTitle(title = "[NO TITLE]") {
        this.shadowRoot.getElementById("title").innerText = title;
    }
    
    append(elm = null) {
        if (!elm) return;
        this.shadowRoot.getElementById("input-list").appendChild(elm);
    }

    remove(elm = null) {
        if (!elm) return;
        this.shadowRoot.getElementById("input-list").remove(elm);
    }

    serialize() {
        let tags = this.shadowRoot.children;
        for (var i = 0; i < tags.length; i++) {
            data = tags[i].serialize();
        }
    }
}

class InputListItemContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "input-list-item-template") {
        let template = document.getElementById(tag);
        let templateContent = template.content;

        const shadowRoot = this.attachShadow({ mode: "open" });
        shadowRoot.appendChild( templateContent.cloneNode(true) );
    }

    setTitle(textStr = "") {
        if (Object.getPrototypeOf(textStr) !== String.prototype) return;

        this.shadowRoot.getElementById("title").innerText = textStr;
    }

    getText() {
        return this.shadowRoot.getElementById("input-entry").value;
    }

    setText(textStr = "") {
        if (Object.getPrototypeOf(textStr) !== String.prototype) return;

        this.shadowRoot.getElementById("input-entry").value = textStr;
    }

    clear() {
        this.shadowRoot.getElementById("input-entry").value = "";
    }

    serialize() {
        return this.shadowRoot.getElementById("input-entry").value;
    }
}


class InputList extends InputListContainer {
    constructor() {
        super();
        this.loadShaddowRoot();
    }
}

class InputListItem extends InputListItemContainer {
    constructor() {
        super();
        this.loadShaddowRoot();
    }
}

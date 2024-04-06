class LspConfigContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "lsp-config-template") {
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
        this.shadowRoot.getElementById("lsp-config").appendChild(elm);
    }

    remove(elm = null) {
        if (!elm) return;
        this.shadowRoot.getElementById("lsp-config").remove(elm);
    }

    serialize() {
        let tags = this.shadowRoot.children;
        for (var i = 0; i < tags.length; i++) {
            data = tags[i].serialize();
        }
    }
}

class InputDictContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "input-dict-template") {
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
        this.shadowRoot.getElementById("input-dict").appendChild(elm);
    }

    remove(elm = null) {
        if (!elm) return;
        this.shadowRoot.getElementById("input-dict").remove(elm);
    }

    serialize() {
        let tags = this.shadowRoot.children;
        for (var i = 0; i < tags.length; i++) {
            data = tags[i].serialize();
        }
    }
}

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

class InputCheckboxContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "input-checkbox-template") {
        let template = document.getElementById(tag);
        let templateContent = template.content;

        const shadowRoot = this.attachShadow({ mode: "open" });
        shadowRoot.appendChild( templateContent.cloneNode(true) );
    }

    setTitle(textStr = "") {
        if (Object.getPrototypeOf(textStr) !== String.prototype) return;
        this.shadowRoot.getElementById("title").innerText = textStr;
    }

    toggle() {
        let elm = this.shadowRoot.getElementById("input-checkbox");
        elm.checked = !elm.checked;
    }

    on() {
        let elm = this.shadowRoot.getElementById("input-checkbox").checked = true;
    }

    off() {
        let elm = this.shadowRoot.getElementById("input-checkbox").checked = false;
    }

    serialize() {
        return this.shadowRoot.getElementById("input-checkbox").value;
    }
}

class SearchReplaceContainer extends HTMLElement {
    constructor() {
        super();
    }

    loadShaddowRoot(tag = "search-replace-template") {
        let template = document.getElementById(tag);
        let templateContent = template.content;

        const shadowRoot = this.attachShadow({ mode: "open" });
        shadowRoot.appendChild( templateContent.cloneNode(true) );
    }

    loadSignals() {
        let elm = this.shadowRoot.getElementById("find-entry");

        elm.addEventListener("keyup", (eve) => {
            findEntry(eve.value);
        });
    }

}




class LspConfig extends LspConfigContainer {
    constructor() {
        super();
        this.loadShaddowRoot();
    }
}

class InputDict extends InputDictContainer {
    constructor() {
        super();
        this.loadShaddowRoot();
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

class InputCheckbox extends InputCheckboxContainer {
    constructor() {
        super();
        this.loadShaddowRoot();
    }
}

class SearchReplace extends SearchReplaceContainer {
    constructor() {
        super();

        this.loadShaddowRoot();
        this.loadSignals();
    }
}
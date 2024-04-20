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
        this.showing = false;
    }

    loadSignals() {
        this.bindToggleSignal( this.shadowRoot.getElementById("whole-word-btn") );
        this.bindToggleSignal( this.shadowRoot.getElementById("only-in-selection-btn") );
        this.bindToggleSignal( this.shadowRoot.getElementById("match-case-btn") );
        this.bindToggleSignal( this.shadowRoot.getElementById("use-regex-btn") );

        let elm = this.shadowRoot.getElementById("find-entry");

        elm.addEventListener("keydown", (eve) => {
            if (eve.key === "Enter") {
                let elm = this.shadowRoot.getElementById("find-btn");
                elm.click();
                return;
            }
        });

        elm.addEventListener("keyup", (eve) => {
            if (eve.key !== "Enter") {
                let elm = this.shadowRoot.getElementById("find-all-btn");
                elm.click();
            }
        });

        elm = this.shadowRoot.getElementById("find-btn");
        elm.addEventListener("click", (eve) => {
            this.findEntry( this.getQuery() );
        });

        elm = this.shadowRoot.getElementById("find-all-btn");
        elm.addEventListener("click", (eve) => {
            this.findAllEntries( this.getQuery() );
        });

        elm = this.shadowRoot.getElementById("replace-btn");
        elm.addEventListener("click", (eve) => {
            this.findEntry( this.getQuery() );
            this.replaceEntry( this.getreplacer() );
        });

        elm = this.shadowRoot.getElementById("replace-all-btn");
        elm.addEventListener("click", (eve) => {
            this.findEntry( this.getQuery() );
            this.replaceAll( this.getreplacer() );
        });
    }

    bindToggleSignal(elm) {
        elm.addEventListener("click", (eve) => {
            let elm      = eve.target.nodeName === "IMG" ? eve.target.parentElement : eve.target;
            let isActive = elm.classList.contains("btn-info");

            if (isActive) {
                elm.classList.remove("btn-info");
                elm.classList.add("btn-dark");
            } else {
                elm.classList.add("btn-info");
                elm.classList.remove("btn-dark");
            }

            this.setFindOptionsLbl();
        });
    }

    toggleShow() {
        if (this.showing) {
            this.showing = false;
            $('#bottom-gutter').popover('hide');
        } else {
            this.showing = true;
            $('#bottom-gutter').popover('show');
        }

        setTimeout(() => {
            if (this.showing) {
                let elm = this.shadowRoot.getElementById("find-entry");
                elm.focus();
            } else {
                editor.focus();
            }
        }, 0.5);
    }

    findPreviousEntry(query) {
        editor.findPrevious();
    }

    replaceEntry(toStr) {
        editor.replace(toStr);
    }

    replaceAll(toStr) {
        editor.replaceAll(toStr);
    }

    findNextEntry(query) {
        editor.findNext();
    }

    findAllEntries(query = null, isBackwwards = false, isWrap = true, range = null) {
        this.updateStyle(QueryState.SearchSuccess);
        if (query === "") {
            this.shadowRoot.getElementById("find-status-lbl").innerText = "Find in current buffer";
            this.updateStyle(QueryState.Searching);
            this.clearSearchMarkers();

            return;
        }

        let totalCount = editor.findAll(query, {
            backwards: isBackwwards,
            wrap: isWrap,
            caseSensitive: this.isMatchCase(),
            wholeWord: this.isUseWholeWord(),
            regExp: this.isUseRegex(),
            range: range === "True" ? true : false
        });

        if (totalCount === 0) {
            console.log('Empty search result...');
            this.clearSearchMarkers();
        }

        this.updateStatusLbl(totalCount, query);

        return totalCount;
    }

    clearSearchMarkers() {
        let markers = session.getMarkers(false);
        for (var id in markers) {
            if (
                markers[id].clazz.indexOf("ace_selection") === 0 ||
                markers[id].clazz.indexOf("ace_selected-word") === 0
            ) {
                session.removeMarker(id);
            }
        }
    }

    findEntry(query = null, isBackwwards = false, isWrap = true, range = null) {
        let result = editor.find(query, {
            backwards: isBackwwards,
            wrap: isWrap,
            caseSensitive: this.isMatchCase(),
            wholeWord: this.isUseWholeWord(),
            regExp: this.isUseRegex(),
            range: range === "True" ? true : false
        });

        return result;
    }

    updateStatusLbl(totalCount = 0, query = "") {
        if ( !query ) return;

        let count  = (totalCount > 0) ? totalCount : "No";
        let plural = (totalCount > 1) ? "s" : "";

        if (totalCount === 0)
            this.updateStyle(QueryState.SearchFail);

        const statusLbl = `${count} result${plural} found for '${query}'`;
        this.shadowRoot.getElementById("find-status-lbl").innerText = statusLbl;
    }

    setFindOptionsLbl() {
        let findOptions = "Finding with Options: ";

        if ( this.isUseRegex() )
            findOptions += "Regex";

        findOptions += ( this.isUseRegex() ) ? ", " : "";
        findOptions += ( this.isMatchCase() ) ? "Case Sensitive" : "Case Inensitive";

        if ( this.isSelectionSearchOnly() )
            findOptions += ", Within Current Selection";

        if ( this.isUseWholeWord() )
            findOptions += ", Whole Word";

        this.shadowRoot.getElementById("find-options-lbl").innerText = findOptions;
    }

    updateStyle(state) {
        let elm = this.shadowRoot.getElementById("find-entry");

        elm.classList.remove("searching");
        elm.classList.remove("search-success");
        elm.classList.remove("search-fail");

        if (state === 0)
            elm.classList.add("searching");
        else if (state === 1)
            elm.classList.add("search-success");
        else if (state === 2)
            elm.classList.add("search-fail");
    }


    getQuery() {
        return this.shadowRoot.getElementById("find-entry").value;
    }

    getreplacer() {
        return this.shadowRoot.getElementById("replace-entry").value;
    }

    isUseWholeWord() {
        let elm = this.shadowRoot.getElementById("whole-word-btn");
        return elm.classList.contains("btn-info");
    }

    isSelectionSearchOnly() {
        let elm = this.shadowRoot.getElementById("only-in-selection-btn");
        return elm.classList.contains("btn-info");
    }

    isMatchCase() {
        let elm = this.shadowRoot.getElementById("match-case-btn");
        return elm.classList.contains("btn-info");
    }

    isUseRegex() {
        let elm = this.shadowRoot.getElementById("use-regex-btn");
        return elm.classList.contains("btn-info");
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
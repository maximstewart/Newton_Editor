// Taken from: https://stackoverflow.com/questions/10588607/tutorial-for-html5-dragdrop-sortable-list

let dndSelected = null

function dragOver(e) {
    if (isBefore(dndSelected, e.target)) {
        e.target.parentNode.insertBefore(dndSelected, e.target);
    } else {
        try {
            e.target.parentNode.insertBefore(dndSelected, e.target.nextSibling);
        } catch(e) {
            return;
        }
    }
}

function dragEnd() {
    dndSelected = null;
}

function dragStart(e) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', null);
    dndSelected = e.target;
}

function isBefore(el1, el2) {
    let cur;
    if (el2.parentNode === el1.parentNode) {
        for (cur = el1.previousSibling; cur; cur = cur.previousSibling) {
            if (cur === el2) return true;
        }
    }

    return false;
}
//star function
function starset(id) {
    fetch("/api/sets/star/"+id)
};
function unstarset(id) {
    fetch("/api/sets/unstar/"+id)
}
function starlesson(id) {
    fetch("/api/lessons/star/"+id)
}
function unstarlesson(id) {
    fetch("/api/lessons/unstar/"+id)
}
//star function
function star(id) {
    fetch("/api/sets/star/"+id)
};
function starlesson(id) {
    fetch("/api/lessons/star/"+id)
}
function unstarlesson(id) {
    fetch("/api/lessons/unstar/"+id)
}
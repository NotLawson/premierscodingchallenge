let answered = false;
let newprogress;
function keydown(e) {
    let key = e.key;    
    console.log(key);
    if (key==="Enter"){
        if (answered==true) {
            document.cookie = "question="+newprogress.toString()+";"
            location.reload();
        };
    } else if (key===" "){
        document.getElementById("progress").setAttribute("value", progress.toString());
        newprogress = progress + 1;
        document.getElementById("definition").removeAttribute("hidden");
        answered = true;
    }
};

document.onkeydown = keydown
document.getElementById("term").innerHTML = question.term

document.getElementById("definition").innerHTML = question.definition



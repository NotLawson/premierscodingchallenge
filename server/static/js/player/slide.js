let answered = false;
let newprogress;
function keydown(e) {
    let key = e.key;    
    console.log(key);

    if (key==="Enter"){
        document.getElementById("progress").setAttribute("value", progress.toString());
        newprogress = progress + 1;
        answered = true;
        if (answered==true) {
            document.cookie = "question="+newprogress.toString()+";"
            location.reload();
        };
    }
};

let answers = question.answers
document.onkeydown = keydown
document.getElementById("question").innerHTML = question.question

document.getElementById("slidecontent").innerHTML = answers[0]



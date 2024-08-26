let answered = false;
let newprogress;function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

function keydown(e) {
    let key = e.key;    
    console.log(key);
    if (key === "a" || key === "1") {
        if (answered===false){
            answer("A");
            answered=true;
            document.getElementById("progress").setAttribute("value", progress.toString())
            newprogress = progress + 1;
        }
    }else if (key==="b" || key === "2"){
        if (answered===false){
            answer("B");
            answered=true;
            document.getElementById("progress").setAttribute("value", progress.toString())
            newprogress = progress + 1;
        }
    }else if (key==="c" || key === "3"){
        if (answered===false){
            answer("C");
            answered=true;
            document.getElementById("progress").setAttribute("value", progress.toString())
            newprogress = progress + 1;
        }
    }else if (key==="Enter"){
        if (answered===true){
            document.cookie = "question="+newprogress.toString()+";"
            location.reload();
        }
    }
};
document.onkeydown = keydown

function answer(guess) {
    colour(correctanswer)
    if (guess!==correctanswer) {
        document.getElementById(guess).classList.add("incorrect")
    }else{
        addConfetti();
        let score = Number(getCookie("score"))+1;
        document.cookie = "score="+score.toString()+";"
    }
}

function colour(correct) {
    if (correct==="A") {
        document.getElementById("A").classList.add("correct")
        document.getElementById("B").classList.add("incorrect-soft")
        document.getElementById("C").classList.add("incorrect-soft")
    } else if (correct==="B") {
        document.getElementById("B").classList.add("correct")
        document.getElementById("A").classList.add("incorrect-soft")
        document.getElementById("C").classList.add("incorrect-soft")
    } else if (correct==="C") {
        document.getElementById("C").classList.add("correct")
        document.getElementById("B").classList.add("incorrect-soft")
        document.getElementById("A").classList.add("incorrect-soft")
    }
}

function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
}

function a() {if (answered===false){answer("A");answered=true;document.getElementById("progress").setAttribute("value", progress.toString());newprogress = progress + 1;}};
function b() {if (answered===false){answer("B");answered=true;document.getElementById("progress").setAttribute("value", progress.toString());newprogress = progress + 1;}};
function c() {if (answered===false){answer("C");answered=true;document.getElementById("progress").setAttribute("value", progress.toString());newprogress = progress + 1;}};

const A = document.getElementById("A");
const B = document.getElementById("B");
const C = document.getElementById("C");
A.addEventListener("click", a);
B.addEventListener("click", b);
C.addEventListener("click", c);


// Set questions
let buttons = ["A", "B", "C"];
buttons = buttons.sort(function () {
    return Math.random() - 0.5;
});
let answers = question.answers

document.getElementById("question").innerHTML = question.question

// Set Question 1
let correctanswer = buttons[0]
document.getElementById(buttons[0]).innerHTML = buttons[0]+": "+answers[0]

// Set Question 2
document.getElementById(buttons[1]).innerHTML = buttons[1]+": "+answers[1]

// Set Question 3
document.getElementById(buttons[2]).innerHTML = buttons[2]+": "+answers[2]

// Set Question 4


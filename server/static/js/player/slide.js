let answered = false;
let newprogress;
function getCookie(cname) {
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

    if (key==="Enter"){
        document.getElementById("progress").setAttribute("value", progress.toString());
        newprogress = progress + 1;
        answered = true;
        let score = Number(getCookie("score"))+1;
        document.cookie = "score="+score.toString()+";"
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



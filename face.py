from flask import Flask
from flask import jsonify
from flask import send_file

app = Flask(__name__)

HTML = """

<!DOCTYPE html>

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body{
    margin:0;
    background:black;
    overflow:hidden;
}

.face{
    width:100vw;
    height:65vh;
    display:flex;
    justify-content:center;
    align-items:center;
    gap:120px;
    transition:transform 0.15s linear;
}
.eye{
    width:120px;
    height:120px;
    background:#00ffff;
    border-radius:50%;
    animation:blink 5s infinite;
}

@keyframes blink{

    0%,95%,100%{
        transform:scaleY(1);
    }

    97%{
        transform:scaleY(0.05);
    }
}
#teaching-panel{

    position:absolute;

    bottom:0;

    width:100%;

    height:35%;

    background:#000;

    color:white;

    padding:20px;

    box-sizing:border-box;

    font-size:24px;

    overflow:auto;
}
#panel-title{
    font-size:28px;
    font-weight:bold;
    text-align:center;
    margin-bottom:15px;
    color:#00ffff;
}

#lesson{

    width:90%;

    margin:auto;

    padding:20px;

    border-radius:20px;

    background:#1a1a1a;

    color:white;

    text-align:center;

    line-height:1.6;

    font-size:22px;

    white-space:pre-wrap;
}
#visual{

    display:none;

    width:90%;

    margin:auto;

    text-align:center;

    color:#00ffff;

    font-size:22px;

    font-family:monospace;

    white-space:pre-wrap;
}
</style>

</head>

<body>

<div class="face" id="face">
    <div class="eye"></div>
    <div class="eye"></div>
</div>
<div id="teaching-panel">

    <div id="lesson"></div>
    <div id="visual"></div>
</div>

<script>
let audioEnabled = false;

document.body.addEventListener(
    "click",
    () => {

        if(audioEnabled)
            return;

        audioEnabled = true;

        let audio =
            new Audio("/audio?" + Date.now());

        audio.play()
        .then(()=>{
            console.log("Audio unlocked");
        })
        .catch(err=>{
            console.log(err);
        });

    },
    {once:true}
);
let lastLesson = "";

const positions = {
    left: -140,
    slightly_left: -70,
    center: 0,
    slightly_right: 70,
    right: 140
}


setInterval(async () => {

    let response =
        await fetch("/direction")

    let data =
        await response.json()

    let direction =
        data.direction

    document.getElementById("face").style.transform =
        `translateX(${positions[direction]}px)`

}, 150)


let visualShown = false;

setInterval(async ()=>{

    let response =
        await fetch("/teaching");

    let data =
        await response.json();

    if(data.content !== lastLesson){

        lastLesson = data.content;

        let lesson =
            document.getElementById("lesson");

        let visual =
            document.getElementById("visual");

        lesson.innerText =
            data.content;

        lesson.style.display = "block";

        visual.style.display = "none";

        setTimeout(()=>{

            lesson.style.display = "none";

            visual.style.display = "block";

        },5000);
    }

},1000);
setInterval(async ()=>{

    let response =
        await fetch("/visual");

    let data =
        await response.json();

    document.getElementById("visual").innerText =
        data.content;

},1000);

let lastAudio = 0;
let currentlyPlaying = false;

setInterval(async ()=>{

    if(currentlyPlaying || !audioEnabled)
        return;

    let response =
        await fetch("/audio_status");

    let data =
        await response.json();

    if(data.modified > lastAudio){

        lastAudio = data.modified;

        let audio =
            new Audio("/audio?" + Date.now());

        currentlyPlaying = true;

        audio.onended = ()=>{
            currentlyPlaying = false;
        };

        audio.onerror = ()=>{
            currentlyPlaying = false;
        };

        audio.play();

    }

},1000);


</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/direction')
def direction():

    try:

        with open("direction.txt") as f:
            value = f.read().strip()

    except:
        value = "center"

    return jsonify({
        "direction": value
    })

@app.route('/audio')
def audio():
    return send_file(
        "response.mp3",
        mimetype="audio/mpeg"
    )

last_audio_time = 0

@app.route('/audio_status')
def audio_status():

    import os

    try:
        modified = os.path.getmtime("response.mp3")
    except:
        modified = 0

    return jsonify({
        "modified": modified
    })
@app.route('/teaching')
def teaching():

    try:
        with open("teaching.txt") as f:
            content = f.read()

    except:
        content = "No lesson available"

    return {
        "content": content
    }
@app.route('/visual')
def visual():

    try:

        with open("visual.txt") as f:
            content = f.read()

    except:

        content = ""

    return {
        "content": content
    }
app.run(host='0.0.0.0', port=5001)

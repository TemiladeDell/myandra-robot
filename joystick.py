import os

from flask import Flask, request
import serial
import time
import subprocess

record_process = None


app = Flask(__name__)

# Arduino USB connection

arduino = serial.Serial(os.getenv("MYANDRA_SERIAL_PORT", "/dev/ttyACM0"), 9600, timeout=1)

time.sleep(2)

HTML = """

<!DOCTYPE html>

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body{
    text-align:center;
    font-family:Arial;
    background:#f5f5f5;
}

h1{
    margin-top:20px;
}

#container{
    width:300px;
    height:300px;
    margin:auto;
    position:relative;
}

#base{
    width:250px;
    height:250px;
    background:#dddddd;
    border-radius:50%;
    position:absolute;
    left:25px;
    top:25px;
}

#stick{
    width:80px;
    height:80px;
    background:#555555;
    border-radius:50%;
    position:absolute;
    left:110px;
    top:110px;
    touch-action:none;
}
#talkButton{
    font-size:24px;
    padding:15px 30px;
    margin-bottom:20px;
}
</style>

</head>
<body>

<h1>Myandra Joystick</h1>
<button id="talkButton">Start Listening</button>

<div id="container">
    <div id="base"></div>
    <div id="stick"></div>
</div>

<script>

let recording = false;

document.getElementById("talkButton")
.addEventListener("click", async function(){

    if(!recording){

        await fetch("/start_recording");

        this.innerText = "Stop Recording";

        recording = true;

    } else {

        await fetch("/stop_recording");

        this.innerText = "Start Recording";

        recording = false;
    }

});

const stick = document.getElementById("stick");

let dragging = false;

stick.addEventListener("touchstart", function() {
    dragging = true;
});

document.addEventListener("touchend", function() {

    dragging = false;

    stick.style.left = "110px";
    stick.style.top = "110px";

    fetch("/move?cmd=STOP");
});

document.addEventListener("touchmove", function(e) {

    if(!dragging) return;

    let touch = e.touches[0];

    let rect = document.getElementById("container").getBoundingClientRect();

    let x = touch.clientX - rect.left - 40;
    let y = touch.clientY - rect.top - 40;

    stick.style.left = x + "px";
    stick.style.top = y + "px";

    let cmd = "STOP";

    if(y < 80){
        cmd = "FORWARD";
    }
    else if(y > 180){
        cmd = "BACKWARD";
    }
    else if(x < 80){
        cmd = "LEFT";
    }
    else if(x > 180){
        cmd = "RIGHT";
    }

    fetch("/move?cmd=" + cmd);
});

</script>

</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/move')
def move():
    cmd = request.args.get('cmd', 'STOP')
    print("Sending:", cmd)
    arduino.write((cmd + '\n').encode())
    return "OK"

@app.route('/start_recording')
def start_recording():

    global record_process

    record_process = subprocess.Popen([
        "arecord",
        "-D",
        os.getenv("MYANDRA_AUDIO_DEVICE", "plughw:3,0"),
        "-f",
        "cd",
        "test.wav"
    ])

    return "OK"


@app.route('/stop_recording')
def stop_recording():

    global record_process

    if record_process:
        record_process.terminate()
        record_process = None

    open("talk.txt","w").close()

    return "OK"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

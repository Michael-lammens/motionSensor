<!DOCTYPE html>
<html>
  <head>
    <title>PJAMP Motion Tracking</title>
    <style>
      html, body {
        margin:0;
        background-color:black;
        color:white;
      }
      video {
        width:75vw;
        height:75vh;
        position:absolute;
        top:5vh;
        left:12.5vw;
      }
      button {
        width:6vw;
        height:6vh;
        position:absolute;
        padding:0;
        border:0.1vw solid gray;
        background-color:black;
        color:white;
        border-radius:7.5%;
        transition-duration:0.5s;
      }
      button:hover {
        background-color:gray;
      }
      button:active {
        background-color:darkgray;
      }
      .disabled {
        opacity:0.5;
      }
      .disabled:hover {
        background-color:black;
      }
      #viewVideo {
        top:85vh;
        left:47vw;
      }
      #viewImages, #next, #prev {
        top:92vh;
        left:47vw;
      }
      #next {
        left:54vw;
      }
      #prev {
        left:40vw;
      }
      #imageMenu {
        width:60vw;
        height:75vh;
        position:absolute;
        top:5vh;
        left:20vw;
        display:none;
      }
    </style>
  </head>

  <body>
    <video id="videoMenu" controls>
      <source src="output1.avi" type="video/avi">
      HTML Video Not Supported In This Browser
    </video>
    <img id="imageMenu" src="image0.jpg">

    <button id="viewVideo" class="disabled" onclick="enableButtons(this)">View Video</button>
    <button id="viewImages" class="enabled" onclick="enableButtons(this)">View Images</button>
    <button id="next" onclick="change(this,'next')">Next</button>
    <button id="prev" onclick="change(this,'prev')">Previous</button>

    <?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    //Create Connection
    $conn = new mysqli($servername, $username, $password);
    //Check Connection
    if($conn->connect_error){
      die("Connection Failed: " . $conn->connect_error);
    }
    ?>

    <script type="text/javascript">
      //Enables and Disables Buttons Based On Which Menu Is Open
      function enableButtons(buttonHTML){
        swapMenus(buttonHTML);
        buttonHTML.classList = "disabled";

        if(buttonHTML.id == "viewVideo"){
          document.getElementById("viewImages").classList = "enabled";
        } else if(buttonHTML.id == "viewImages"){
          document.getElementById("viewVideo").classList = "enabled";
        }
      }
      //Switches Between Video and Image Menus
      function swapMenus(buttonHTML){
        if(buttonHTML.id == "viewVideo" && buttonHTML.classList == "enabled"){
          document.getElementById("videoMenu").style.display = "block";
          document.getElementById("imageMenu").style.display = "none";
          //Plays Video When Back On Video
          document.getElementById("videoMenu").play();
        } else if(buttonHTML.id == "viewImages" && buttonHTML.classList == "enabled"){
          document.getElementById("videoMenu").style.display = "none";
          document.getElementById("imageMenu").style.display = "block";
          //Pauses Video While On Images
          document.getElementById("videoMenu").pause();
        }
      }
      //Navigates Through Selection Of Images and Videos
      function change(buttonHTML, direction){
        var currentImage = document.getElementById("imageMenu").src;
        currentImage = parseInt(currentImage[currentImage.split(".")[0].length - 1]);

        var currentVideo = document.getElementById("videoMenu").children[0].src;
        currentVideo = parseInt(currentVideo[currentVideo.split(".")[0].length - 1]);

        if(direction == "next"){
          if(document.getElementById("viewVideo").classList == "disabled"){
            var nextVideo = currentVideo + 1;
            document.getElementById("videoMenu").children[0].src = "output" + nextVideo + ".avi";
          } else {
            var nextImage = currentImage + 1;
            document.getElementById("imageMenu").src = "image" + nextImage + ".jpg";
          }
        } else if(direction == "prev"){
          if(document.getElementById("viewVideo").classList == "disabled" && currentVideo >= 2){
            var prevVideo = currentVideo - 1;
            document.getElementById("videoMenu").children[0].src = "output" + prevVideo + ".avi";
          } else if(currentImage >= 1){
            var prevImage = currentImage - 1;
            document.getElementById("imageMenu").src = "image" + prevImage + ".jpg";
          }
        }
      }
    </script>
  </body>
</html>

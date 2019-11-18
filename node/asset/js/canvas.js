var canv = {
  width: 960,
  height: 705
};

var pos = {
  drawable: false,
  x: -1,
  y:-1
};
var canvas, ctx;
var re1, re2, re3;

window.onload = function() {
  canvas = document.getElementById("canvas");
<<<<<<< HEAD:FrontEnd/draw_page/canvas.js
=======
  trash_button = document.getElementById("trash_b");
>>>>>>> dev_heo:node/asset/js/canvas.js
  ctx = canvas.getContext("2d");

  re1 = document.getElementById("recommend1");
  re2 = document.getElementById("recommend2");
  re3 = document.getElementById("recommend3");

  // event type
  canvas.addEventListener("mousedown", listener);
  canvas.addEventListener("mouseup", listener);
  canvas.addEventListener("mousemove", listener);
  canvas.addEventListener("mouseout", listener);
};

function recommend_clicked(image){
  recommend_border_init();
  switch (image) {
    case 1:
      re1.style.border = "5px solid #0000FF";
      break;
    case 2:
      re2.style.border = "5px solid #0000FF";
      break;
    case 3:
      re3.style.border = "5px solid #0000FF";
      break;
  }
}

function recommend_border_init(){
  re1.style.border = "1px solid #797979";
  re2.style.border = "1px solid #797979";
  re3.style.border = "1px solid #797979";
}

function listener(event){
  switch (event.type) {
    case "mousedown":
      initDraw(event);
      break;
    case "mousemove":
      if(pos.drawable)
        draw(event);
      break;
    case "mouseout":
    case "mouseup":
      finishDraw();
      break;

  }
}

function initDraw(event){
  ctx.beginPath();
  pos.drawable = true;
  var coors = getPosition(event);
  pos.X = coors.X;
  pos.Y = coors.Y;
  ctx.moveTo(pos.X, pos.Y);
}

function draw(event){
  var coors = getPosition(event);
  ctx.lineTo(coors.X, coors.Y);
  pos.X = coors.X;
  pos.Y = coors.Y;
  ctx.stroke();
}

function finishDraw(){
  pos.drawable = false;
  pos.X = -1;
  pos.Y = -1;
}

function getPosition(event){
  var x = event.pageX - canvas.offsetLeft - 10;
  var y = event.pageY - canvas.offsetTop - 380;
  return {X: x, Y: y};
}
<<<<<<< HEAD:FrontEnd/draw_page/canvas.js

function button_clicked(button){
  switch (button) {
    case 0:
      // send_button clicked
      break;
    case 1:
      // trash_button clicked
      ctx.clearRect(0, 0, canv.width, canv.height);
      ctx.beginPath();
      break;
    case 2:
      // cancel_button clicked
      break;
  }
=======
function clearCanvas()
{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();

    localStorage.removeItem('imgData');
>>>>>>> dev_heo:node/asset/js/canvas.js
}

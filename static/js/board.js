var start;
var width
var ctx;
var stone_size;
var canvas;

var isPiecePlaced  = new Array(19);
var turn =1;
var strongActivate = false;
can_put_strong = {1:true,2:true};
var observe_count = {1:5,2:5};
var observing = false;

var original_canvas;

for (var i = 0; i < 19; i++) {
  isPiecePlaced[i] = new Array(19).fill(false);
}

var stone_color ={
  1:{
    1:"#111010",
    0:"#3e3f3f"
  },
  2:{
    1:"#e0e0e0",
    0:"#bfbebf"
  }
}

function draw_grid(){
  canvas = document.getElementById("outerCanvas");
  var length = canvas.width;
  var rectangle_length = length*0.94;
  start = length*0.03;
  ctx = canvas.getContext("2d");
  ctx.strokeRect(start,start,rectangle_length,rectangle_length);
  width = rectangle_length/18;
  stone_size = width/2.1;
  let end_point = start+rectangle_length;
  for (let x = 1; x < 18; x ++) {
    let start_x = start+x*width;
    ctx.beginPath();
    ctx.moveTo(start_x,start);
    ctx.lineTo(start_x,end_point);
    ctx.stroke();
  }

  for (let y = 1; y < 18; y ++) {
    let start_y = start+y*width;
    ctx.beginPath();
    ctx.moveTo(start,start_y);
    ctx.lineTo(end_point,start_y);
    ctx.stroke();
  }

  let stars = [
    [4,4],[4,10],[4,16],
    [10,4],[10,10],[10,16],
    [16,4],[16,10],[16,16],
  ];
  for(let i=0;i<stars.length;i++){
    star = stars[i];
    var y = star[0];
    var x = star[1];

    ctx.beginPath();
    ctx.arc(start+(x-1)*width,start+(y-1)*width,width/11,0,2*Math.PI);
    ctx.fillStyle = "#000000";
    ctx.fill();
    ctx.stroke();
  }

}


function putStone(event,canvas){
  if(observing){
    return;
  }
  // クリックされた座標を取得
  clickX = event.clientX - canvas.getBoundingClientRect().left;
  clickY = event.clientY - canvas.getBoundingClientRect().top;
  clickX-=start;
  clickY-=start;

  var pos_x = Math.round(clickX / width);
  var pos_y = Math.round(clickY / width);
  if(!isAvailable(pos_y,pos_x)){
    return;
  }
  isPiecePlaced[pos_y][pos_x] = true;
  var code= stone_color[turn][strongActivate?1:0];
  draw_stone(pos_y,pos_x,code)

  can_put_strong[turn]=strongActivate? false :true;    

  change_turn();
  origin_strong = strongActivate
  strongActivate = false;
  updateStrongDisable(!can_put_strong[turn]);
  updateStrongButton();
  updateObserveButton();
  putStoneRequest(pos_y,pos_x,origin_strong);
}
// JavaScriptでCanvasに描画するコード
document.addEventListener("DOMContentLoaded", function() {
  draw_grid();
  sendReset();
  canvas.addEventListener('click', function(event) {
    putStone(event,canvas);
  });
});

function draw_stone(y,x,color_code){
  var nearestX = start+x * width;
  var nearestY = start+y * width;
  ctx.beginPath();
  ctx.arc(nearestX, nearestY, stone_size, 0, 2 * Math.PI);
  ctx.fillStyle = color_code;
  ctx.fill();
}

document.getElementById("observationButton").addEventListener("click", function() {
  if(observing){
    stopObserving();
    return;
  }
  if(!observe_count[turn]>0){
    return;
  }
  observe_count[turn]-=1;
  $.ajax({
    url: '/observe/',
    type: 'GET',
    data: {
    },
    dataType: 'json',
    success: function (data) {
        saveOriginalCanvas();
        let messageElement = document.getElementById("message");
        messageElement.textContent = data.message;
        draw_observed_board(data.board);
        document.getElementById("observationButton").textContent = "観測停止";
        observing = true;
    },
    error: function (error) {
        console.log('Error:', error);
    }
});
});

function stopObserving(){
  document.getElementById("observationButton").textContent = "観測";
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  observing = false;
  ctx.putImageData(original_canvas,0,0);
  document.getElementById("message").textContent="";
  updateObserveButton();
}

document.getElementById("strong").addEventListener("click", function() {
  strongActivate = !strongActivate;
  updateStrongButton();
});

document.getElementById("gameButton").addEventListener("click", function() 
{
  document.getElementById("message").textContent="";
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  draw_grid();
  isPiecePlaced  = new Array(19);
  turn =1;
  strongActivate = false;
  can_put_strong = {1:true,2:true};
  observe_count = {1:5,2:5};  
  for (var i = 0; i < 19; i++) {
    isPiecePlaced[i] = new Array(19).fill(false);
  }
  sendReset();
});

function sendReset(){
  $.ajax({
    url: '/start/',
    type: 'GET',
    data: {
    },
    dataType: 'json',
    success: function (data) {
      console.log(data.message);
    },
    error: function (error) {
        console.log('Error:', error);
    }
});
}

function resetStrongButton(){
  strongActivate = false;
  updateStrongButton();
}

function updateObserveButton(){
  button = document.getElementById("observationButton");
  button.disabled = observe_count[turn]==0;
}
function updateStrongButton() {
  const bonusButton = document.getElementById("strong");
  bonusButton.textContent = !strongActivate ? "強くする" : "弱くする ";
}
function getRandomNumber() {
  // Math.floorで小数点以下を切り捨て、1を加えて範囲を調整
  return Math.floor(Math.random() * 4) + 1;
}

function isAvailable(y,x){
  return !isPiecePlaced[y][x];
}

function putStoneRequest(y,x,origin_strong) {
  $.ajax({
      url: '/put_stone/',
      type: 'POST',
      data: {
        "y":y,
        "x":x,
        "strong":origin_strong?1:0
      },
      dataType: 'json',
      success: function (data) {
          // サーバーからのレスポンスを処理
          console.log(data.message);
      },
      error: function (error) {
          console.log('Error:', error);
      }
  });
}

function change_turn(){
  if(turn==1){
    turn=2;
  }else{
    turn=1;
  }
  document.getElementById("currentTurn").textContent = turn==1?"黒":"白"
}

function updateStrongDisable(disable){
  const bonusButton = document.getElementById("strong");
  bonusButton.disabled = disable;
}


function saveOriginalCanvas(){
  var canvas = document.getElementById("outerCanvas")
  original_canvas = ctx.getImageData(0,0,canvas.width,canvas.height);
}

function draw_observed_board(board){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  draw_grid();
  var colors = {
    1:"#000000",
    2:"#FFFFFF",
    11:"#AAAAAA",
    12:"#DDDDDD"
  }
  for(let i=0;i<board.length;i++){
    for(let j=0;j<board[0].length;j++){
      if(board[i][j]==0){
        continue;
      }
      draw_stone(i,j,colors[board[i][j]])
    }
  }
}
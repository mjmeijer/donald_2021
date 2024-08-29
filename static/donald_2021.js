//
// donald-2021 (c) copyright 2021-2023 Maarten Meijer / AUAS
//
Array.prototype.rotateRight = function( n ) {
  this.unshift.apply( this, this.splice( n, this.length ) );
  return this;
}

var blackColors = new Array(
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black' // named color
  );

var testCounter, age, awake, drugs, start, questions;

function setup() {
  createCanvas(windowWidth, windowHeight);
  text("Leeftijd (jaren)", 10, 30)
  age = createInput('', 'number');
  age.position(10,35);
  age.size(100);
  age.attribute("pattern" , "[0-9]*")
  age.style("text-align" , "right")

  text("Uren wakker (uren)", 10, 80)
  awake = createInput('', 'number');
  awake.position(10,85);
  awake.size(100);
  awake.attribute("pattern" , "[0-9]*")
  awake.style("text-align" , "right")

  text("Middelen gebruik afgelopen 12 uur", 10, 130)
  drugs = createSelect();
  drugs.position(10,135);
  drugs.option('zeg ik niet');
  drugs.option('geen');
  drugs.option('alcohol');
  drugs.option('pillen');
  drugs.option('alcohol+pillen');
  drugs.option('energiedrank');
  drugs.option('koffie');
  drugs.option('van alles wat');
  drugs.option('anders');
  drugs.selected('zeg ik niet')

  text("kleurenblind", 10, 180)
  cb = createSelect();
  cb.position(10,185);
  cb.option('zeg ik niet');
  cb.option('kleurenblind');
  cb.option('niet kleurenblind');
  drugs.selected('zeg ik niet')


  start = createButton('Starten');
  start.position(10, 230);
  start.mousePressed(startLoop);
  noLoop();
}

function startLoop() {
  questions = '' + age.value() + '\t' + awake.value() + '\t' + drugs.value() + '\t' + cb.value();
  removeElements();
  testCounter = 0;
  frameRate(60);
  background(10);
  stroke(0);
  loop();
}


function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

function deviceShaken() {
  fullscreen(true);
  background(10);
}

function distance(x1, y1, x2, y2) {
  return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

/* prevents the mobile browser from processing some default
 * touch events, like swiping left for "back" or scrolling
 * the page.
 */
function touchStarted(){
  if(isLooping()) return false;
}

function touchMoved(){
  if(isLooping()) return false;
}


function touchEnded() {
  if(isLooping()) {

  ellipse(mouseX, mouseY, 50, 50);

  if (distance(mouseX, mouseY, windowWidth/2, windowHeight/2) < 150) {
    fullscreen(!fullscreen());
    return;
  }
  // prevent default
  b = 0;
  if (mouseX > windowWidth / 2) {
    b += 2;
  }
  if (mouseY > windowHeight / 2) {
    b += 1;
  }
  lastButton = Array(0, 1, 3, 2)[b];
  return false;
  }
}

function ledring(x, y, colors) {
  push();
  translate(x, y);
  stroke(127, 127, 127);
  fill(10, 10, 10);
  circle(0, 0, 300);
  // show identifier
  fill('rgb(10,255,0)');
  textAlign(CENTER, CENTER);
  textSize(32);
//  text('level ' + testLevel, 0, -20);
  text(testID, 0, 0);
  textSize(16);
  text('level ' + testLevel, 0, -40);
  text(frameCount, 0, 40);
  // end show test level
  rotate (radians(15));
  for (i = 0; i < 12; i++) {
    fill(colors[i]);
    rotate (radians(-30));
    rectMode(CENTER);
    rect(0, -100, 40, 40);
    fill('grey');
    textSize(12);
    textAlign(CENTER, CENTER);
    text(i, 0, -130, 20, 20);
  }
  pop();
}

function showLeds(leds) {
  ledring(windowWidth / 2, windowHeight / 2, leds);
}

function buttons(x, y, w, h) {
  push();
  w2 = w / 2;
  h2 = h / 2;
  translate(x, y);
  stroke(127, 127, 127);
  fill(10, 10, 10, 127);
  rect(0, 0, w2, h2);
  rect(w2, 0, w2, h2);
  rect(0, h2, w2, h2);
  rect(w2, h2, w2, h2);
  pop();
}

function showButtons() {
  if(typeof custom_buttons === "function"){
    custom_buttons(0, 0, windowWidth, windowHeight);
  } else {
    buttons(0, 0, windowWidth, windowHeight);
  }
}

function postResults(req, rec, status, time) {
  gtag('event', 'result', {
    'event_category': status,
    'event_label': testID,
    'value': currentLevel
  });
  data = testID + '\t'
    + testCounter + '\t'
    + id + '\t'
    + T0_IDLE + '\t'
    + T1_WARN + '\t'
    + T2_SHOWTEST + '\t'
    + T3_DECAY + '\t'
    + T4_COUNTDOWN + '\t'
    + req + '\t'
    + rec + '\t'
    + status + '\t'
    + time  + '\t'
    + currentLevel + '\t'
    + ''+windowWidth+'x'+windowHeight + '\t'
    + questions;
  httpPost('/', data);
}


//
// below is the statemachine implementing the test program and UI
//
//

var activityState = 0;
var testLevel = 0;
var lastButton = -1;
var lastLevel = -1;
var currentLevel = -1;
var startFrame;
var test;
var game, reply;
function changeState(newState) {
  startFrame = frameCount;
  lastLevel = currentLevel;
  currentLevel = testLevel;
  lastButton = -1;
  activityState = newState;
//  print('new activityState : ' + activityState);
}


// State 0
function handleIdle() {
  showIdle();
  if (lastButton != -1) {
//    print("lastButton = " + lastButton);
    testLevel = 2;
    changeState(1);
  }
}

// State 1
function handlePrepare() {
  showPrepare();
  if (frameCount - startFrame > T1_WARN) {
    game = new Game(testLevel);
    reply = [];
    testCounter += 1;
//    print('game : ' + game.toString());
    changeState(2);
  }
}

// State 2
function handleShowTest() {
  if (currentLevel == -1) {
    changeState(3);
    return;
  }
  if (frameCount % T2_SHOWTEST == 0) {
    if(currentLevel > 0) {
      showTestStep(game.getValue(testLevel - currentLevel));
    }
    currentLevel = currentLevel - 1;
  } else if (frameCount % T2_SHOWTEST > T2_SHOWTEST - 10) {
    showLeds(blackColors);
  }
}

// State 3
function handleDecay() {
  showDecay();
  if (frameCount - startFrame > T3_DECAY) {
    changeState(4);
    return;
  }
}

// State 4
function handleCheckResponse() {
  if (frameCount - startFrame > T4_COUNTDOWN) {
    postResults(game.toString(), '' + reply, 'timeout', frameCount - startFrame);
    changeState(5);
    return;
  }
  showCountdown();
  switch(lastButton) {
  case -1:
    break;
  default:
    reply.push(lastButton);
//    print('expected : ' + game.getValue(testLevel - currentLevel) + ', received : ' + lastButton);
    if (lastButton != game.getValue(testLevel - currentLevel)) {
      postResults(game.toString(), '' + reply, 'wrong', frameCount - startFrame);
      lastButton = -1;
      changeState(7);
      return;
    }
    currentLevel = currentLevel - 1;
    if (currentLevel == 0) {
      postResults(game.toString(), '' + reply, 'correct', frameCount - startFrame);
      lastButton = -1;
      changeState(6);
      return;
    }
  }
  lastButton = -1;
}

// State 5
function handleTimeOut() {
  showTimeout();
  // TODO post the result as timeout
  if (frameCount - startFrame > T5_TIMEOUT) {
    if(typeof custom_timeout === "function"){
      changeState(custom_timeout());
    } else {
      testLevel = 0;
      changeState(0);
    }
//    print("Timeout!");
  }
}

// State 6
function handleSuccess() {
  showSuccess();
  // TODO post the result as success
  if (frameCount - startFrame > T6_CORRECT) {
    testLevel += 1;
//    print("Success! new test level : " + testLevel);
    changeState(1);
  }
}

// State 7
function handleFailure() {
  showFailure();
  // TODO post the result as failure
  if (frameCount - startFrame > T7_INCORRECT) {
    testLevel = max(testLevel - 1, 0) ;
//    print("Failure! new test level : " + testLevel);
    if (testLevel == 0) {
      changeState(0);
    } else {
      changeState(1);
    }
  }
}

// the short term memory tester program works from a gameloop or activity state machine
function draw() {
  // print('current activityState : ' + activityState + ', test level : ' + testLevel + ', current level : ' + currentLevel);
  switch(activityState) {
  case 0:
    handleIdle();
    break;
  case 1:
    handlePrepare();
    break;
  case 2:
    handleShowTest();
    break;
  case 3:
    handleDecay();
    break;
  case 4:
    handleCheckResponse();
    break;
  case 5:
    handleTimeOut();
    break;
  case 6:
    handleSuccess();
    break;
  case 7:
    handleFailure();
    break;
  default:
    break;
  }
}

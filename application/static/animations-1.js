//
// donald-2021 (c) copyright 2021-2023 Maarten Meijer / AUAS
//
//
// timings in frames not milliseconds!Running at 60 FPS
//
var id             = 'PARAMS-1';

var T0_IDLE        = 20; // one idle step
var T1_WARN        = 60;
var T2_SHOWTEST    = 40; // one test step
var T3_DECAY       = 120;
var T4_COUNTDOWN   = 300;
var T5_TIMEOUT     = 120;
var T6_CORRECT     = 120;
var T7_INCORRECT   = 120;

//
//  F0 shows the attention grabbing animation meant to seduce you to interact
//
//
var idleColors = new Array(
  180, // snigle digit grey scale
  'red', // named color
  '#fae', // three digit hex
  '#222222', // six digit hex
  'rgb(10,255,0)', // integer rgb value
  'rgba(0,255,0,0.25)', // integer rgba value
  'rgb(100%, 0%, 10%)', // percentge rgb notation
  'rgba(100%, 0%, 100%, 0.2)', // percentge rgba notation
  'grey',
  'blue',
  'pink',
  'green',
  'teal'
  );

function showIdle() {
  if (frameCount % T0_IDLE == 0) {
    showButtons();
    showLeds(idleColors);
    idleColors.rotateRight(1);
  }
}

//
//  F1 warns to prepare yourself to remeber the coming sequence
//
//
var prepColors = new Array(
  'pink', // named color
  'pink', // named color
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

function showPrepare() {
  if (frameCount % (T1_WARN / 12) == 0) {
    showButtons();
    showLeds(prepColors);
    prepColors.rotateRight(1);
  }
}

//
//  F2 display a single block of pixels
//
//
var   blokColors = new Array(
  'red', // named color
  'red', // named color
  'red', // named color
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

function showTestStep(index) {
  showButtons();
  blokColors.rotateRight(-3 * index); // rotate to proper position
  showLeds(blokColors);
  blokColors.rotateRight(3 * index); // rotate back for next block
}

//
//  F3 decay is where your short senory and term memory slowly fades away
//
//
var decayColors = new Array(
  'blue', // named color
  'blue', // named color
  'blue', // named color
  'blue', // named color
  'blue', // named color
  'blue', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black', // named color
  'black' // named color
  );

function showDecay() {
  if (frameCount % (T3_DECAY / 12) == 0) {
    showLeds(decayColors);
    decayColors.rotateRight(3);
  }
}

//
//  F4 display a countdown animation to stresss you more
//
//
var countColors = new Array(
  'teal', // named color
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

function showCountdown() {
  if (frameCount % (T4_COUNTDOWN / 12) == 0) {
    showButtons();
    showLeds(countColors);
    countColors.rotateRight(-1);
  }
}


//
//  F5 alas, you took too long to respond completely
//
//
var timeoutColors = new Array(
  'orange', // named color
  'yellow', // named color
  'orange', // named color
  'yellow', // named color
  'orange', // named color
  'yellow', // named color
  'orange', // named color
  'yellow', // named color
  'orange', // named color
  'yellow', // named color
  'orange', // named color
  'yellow' // named color
  );

function showTimeout() {
  if (frameCount % (T5_TIMEOUT / 12) == 0) {
    showButtons();
    showLeds(timeoutColors);
    timeoutColors.rotateRight(-1);
  }
}

//
//  F6 you entered the correct sequence, bravo!
//
//
var successColors = new Array(
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green', // named color
  'green' // named color
  );

function showSuccess() {
  // no animation yet in this code
  if (frameCount % (T6_CORRECT / 12) == 0) {
    showButtons();
    showLeds(successColors);
  }
}
//
//  F7 alas, you failed to enter the correct sequence
//
//
var failColors = new Array(
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red', // named color
  'red' // named color
  );

function showFailure() {
  // no animation yet in this code
  if (frameCount % (T7_INCORRECT / 12) == 0) {
    showButtons();
    showLeds(failColors);
  }
}

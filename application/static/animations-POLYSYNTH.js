//
//
// timings in frames not milliseconds!Running at 60 FPS
//
var id             = 'POLYSYNTH';

var T0_IDLE        = 20; // one idle step
var T1_WARN        = 120;
var T2_SHOWTEST    = 40; // one test step
var T3_DECAY       = 120;
var T4_COUNTDOWN   = 360;
var T5_TIMEOUT     = 120;
var T6_CORRECT     = 120;
var T7_INCORRECT   = 120;



//
//  custom_buttons - to customize the look of the buttons
//  uncomment and modify this code
//
// function custom_buttons(x, y, w, h) {
//   push();
//   w2 = w / 2;
//   h2 = h / 2;
//   translate(x, y);
//
//    bcolor = color(127, 127, 127, 127);
//   if (testLevel > 3) {
//     bcolor = color(0, 0, 0, 127);
//   }
//
//
//   stroke(127, 127, 127);
//   fill(bcolor);
//   rect(0, 0, w2, h2);
//   rect(w2, 0, w2, h2);
//   rect(0, h2, w2, h2);
//   rect(w2, h2, w2, h2);
//
//   fill('grey');
//   textSize(36);
//   textAlign(CENTER, CENTER);
//   w3 = w2/2;
//   h3 = h2/2;
//   text("0", w3, h3);
//   text("1", w3, h3 + h2);
//   text("2", w3 + w2, h3 + h2);
//   text("3", w3 + w2, h3);
//   pop();
// }

//
// uncomment and change this code when you want something else than reset to level 0 or timeout
//
//function custom_timeout()
//{
//  testLevel = Math.max(testLevel - 2,0);
// return 1; // new state
//}




//
//  F0 shows the attention grabbing animation meant to seduce you to interact
//
//
var idleColors = new Array(
  '#FE0000', // alternating bad combinations for collorblindness set 1
  '#FE0000',
  '#00AC00',
  '#00AC00',
  '#FE0000',
  '#FE0000',
  '#00AC00',
  '#00AC00',
  '#FE0000',
  '#FE0000',
  '#00AC00',
  '#00AC00'
  );

function showIdle() {
  if (frameCount % T0_IDLE == 0) {
    showButtons();
    showLeds(idleColors);
    idleColors.rotateRight(-1);
  }
}

//
//  F1 warns to prepare yourself to remember the coming sequence
//
//
var prepColors = new Array(
  '#01AC87', // alternating bad combinations for collorblindness set 2
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#01AC87',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400',
  '#EF0400'
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
  '#243FFE', // alternating bad combinations for collorblindness set 3
  '#243FFE',
  '#243FFE',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0',
  '#7030A0'
  );



let synth; // Our synthesizer
let notes = [`F4`, `G4`, `Ab4`, `Bb4`, `C4`, `Db4`, `Eb4`, `F5`]; // The scale for F minor

synth = new p5.PolySynth();


function showTestStep(index) {

  showButtons();
  blokColors.rotateRight(-3 * index); // rotate to proper position

  synth.play(notes[index], 0.2, 0, 0.4);

  showLeds(blokColors);
  blokColors.rotateRight(3 * index); // rotate back for next block
}

//
//  F3 decay is where your short senory and term memory slowly fades away
//
//
var decayColors = new Array(
  '#6332A0', // alternating bad combinations for collorblindness set 4
  '#6332A0',
  '#6332A0',
  '#6332A0',
  '#6332A0',
  '#6332A0',
  '#01AFF4',
  '#01AFF4',
  '#01AFF4',
  '#01AFF4',
  '#01AFF4',
  '#01AFF4',
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
  '#FE0000', // colorblind bad set 5
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
  '#01AC87', // bad set for colorblindness #2
  '#EF0400',
  '#01AC87',
  '#EF0400',
  '#01AC87',
  '#EF0400',
  '#01AC87',
  '#EF0400',
  '#01AC87',
  '#EF0400',
  '#01AC87',
  '#EF0400',
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
  '#00AC00', // green half of set 1
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
  '#00AC00',
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
  '#FE0000', // red half of set 1
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  '#FE0000',
  );

function showFailure() {
  // no animation yet in this code
  if (frameCount % (T7_INCORRECT / 12) == 0) {
    showButtons();
    showLeds(failColors);
  }
}

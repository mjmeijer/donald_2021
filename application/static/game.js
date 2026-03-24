//
// (c) Copyright 2021-2026 Maarten Meijer / Amsterdam University of Applied Science
//
// game.js
//
//  A game is represented by an array of random values (0-3)
//
//

function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}

function Game(levels) {
  this.levels = levels;
  this.values = [];
  for(var i = 0; i < levels; i++) {
    this.values.push(getRandomInt(4));
  }
}

Game.prototype.getValue = function(level) {
  return this.values[level];
}

Game.prototype.toString = function(level) {
  return '' + this.values;
}

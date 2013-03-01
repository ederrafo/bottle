/**
 * Created with PyCharm.
 * User: myth
 * Date: 13-2-19
 * Time: 下午1:31
 * To change this template use File | Settings | File Templates.
 */
var _ROWS_NUM = 21;
var _COLS_NUM = 12;

var _BRICKS = new Array();
_BRICKS[0] = [[0, 1, 0], [1, 1, 1]];
_BRICKS[1] = [[1, 0, 0], [1, 1, 1]];
_BRICKS[2] = [[0, 0, 1], [1, 1, 1]];
_BRICKS[3] = [[1, 1], [1, 1]];
_BRICKS[4] = [[1, 1, 0], [0, 1, 1]];
_BRICKS[5] = [[0, 1, 1], [1, 1, 0]];
_BRICKS[6] = [[1, 1, 1, 1]];

var _BRICKS_STYLE = new Array();
_BRICKS_STYLE[0] = 'background-color: #f00';
_BRICKS_STYLE[1] = 'background-color: #f90';
_BRICKS_STYLE[2] = 'background-color: #ff0';
_BRICKS_STYLE[3] = 'background-color: #9f0';
_BRICKS_STYLE[4] = 'background-color: #0f0';
_BRICKS_STYLE[5] = 'background-color: #0f9';
_BRICKS_STYLE[6] = 'background-color: #0ff';
_BRICKS_STYLE[7] = 'background-color: #09f';
_BRICKS_STYLE[8] = 'background-color: #00f';
_BRICKS_STYLE[9] = 'background-color: #90f';
_BRICKS_STYLE[10] = 'background-color: #f0f';
_BRICKS_STYLE[11] = 'background-color: #f09';

var currentBrick = _BRICKS[Random(0, _BRICKS.length - 1)];
var currentBrickStyle = _BRICKS_STYLE[Random(0, _BRICKS_STYLE.length - 1)];
var currentBrickOffsetRow = -1;
var currentBrickOffsetCol = 4;
var dropSpeed = new Array(0, 100, 200, 400, 800);
var dropSpeedMark = 1;
var userDropSpeed = dropSpeed[dropSpeed.length - 1];
var currentDropSpeed = userDropSpeed;
var turnReady = 1;
var totalScore = 0;
var thisElim = 0;
var dropSwitch = 0;
var droping;


//Create gridding
$(function(){
    $('#gridding').append('<table cellspacing=3>');
    for(var row = 0; row < _ROWS_NUM; row++){
        $('#gridding > table').append('<tr class="row_'+ row+ '">');
        for(var col = 0; col < _COLS_NUM; col++){
            $('.row_'+ row).append('<td id="r'+ row+ 'c'+ col+'" class="void"> ');
        }
    }
    $('#current_speed').html(dropSpeedMark);
});

//Start Droping
function Start(){
    if(dropSwitch == 0){
        dropSwitch = 1;
        BrickDroping();
    }else if(dropSwitch == 1){
        clearTimeout(droping);
        dropSwitch = 0;
        currentBrickOffsetRow--;
    }
    return dropSwitch;
}

//Random Brick
function Random(inLow, inHigh){
    var id = Math.floor(Math.random() * (inHigh - inLow + 1) + inLow);
    return id;
}

//Raise or Reduce Current Speed
function SpeedFastSlow(inRise){
    if(inRise == 'fast' && userDropSpeed > dropSpeed[0]){
        dropSpeedMark++;
        userDropSpeed = dropSpeed[dropSpeed.length - dropSpeedMark];
    }else if(inRise == 'slow' && userDropSpeed < dropSpeed[dropSpeed.length - 1]){
        dropSpeedMark--;
        userDropSpeed = dropSpeed[dropSpeed.length - dropSpeedMark];
    }
    currentDropSpeed = userDropSpeed;
    return dropSpeedMark;
}

//Initialize a New Brick
function InitializeBrick(){
    setTimeout(function(){
        EliminateRows();
        if(thisElim > 0){
            thisScore = thisElim * 2 - 1;
        }else{
            thisScore = 0;
        }
        totalScore += thisScore;
        $('#this_elim').html(thisElim);
        $('#this_score').html(thisScore);
        $('#total_score').html(totalScore);
    }, 100);
    currentBrick = _BRICKS[Random(0, _BRICKS.length - 1)];
    currentBrickStyle = _BRICKS_STYLE[Random(0, _BRICKS_STYLE.length - 1)];
    currentBrickOffsetRow = -1;
    currentBrickOffsetCol = 4;
    currentDropSpeed = userDropSpeed;
    BrickDroping();
}

//Display Brick
function DisplayBrick(inBrick, inBrickOffsetRow, inBrickOffsetCol){
    $('.void').attr('style', '');
    for(var i = 0; i < inBrick.length; i++){
        for(var j = 0; j < inBrick[i].length; j++){
            $(function(){
                if(inBrick[i][j] == 1){
                    var inX = inBrickOffsetRow + i;
                    var inY = inBrickOffsetCol + j;
                    $('#r'+ inX+ 'c'+ inY).attr('style', currentBrickStyle);
                }
            });
        }
    }
}

//Brick Drop to Stop
function BrickStop(inBrick){
    for(var i = 0; i < inBrick.length; i++){
        for(var j = 0; j < inBrick[i].length; j++){
            var nextCellRow = currentBrickOffsetRow + i;
            var nextCellCol = currentBrickOffsetCol + j;
            var nextCellClass = $('#r'+ nextCellRow+ 'c'+ nextCellCol).attr('class');
            if(inBrick[i][j] == 1 && nextCellClass == 'solid' || nextCellRow == _ROWS_NUM){
                for(var i = 0; i < inBrick.length; i++){
                    for(var j = 0; j < inBrick[i].length; j++){
                        $(function(){
                            if(inBrick[i][j] == 1){
                                var inX = currentBrickOffsetRow + i - 1;
                                var inY = currentBrickOffsetCol + j;
                                $('#r'+ inX+ 'c'+ inY).attr('class', 'solid');
                            }
                        });
                    }
                }
                if(currentBrickOffsetRow > 0){
                    InitializeBrick();
                }else{
                    var restart = confirm('Game Over! Your Total Score is '+ totalScore+ '. Are You Restart?')
                    if(restart == true){
                        window.location = location.href;
                    }
                }
                return 'stop';
            }
        }
    }
    return 'drop';
}

//Brick Move to Left or Right
function BrickLeftRight(inLeftRight){
    if(dropSwitch == 1){
        var toLeft = 1;
        if(inLeftRight == 'left' && currentBrickOffsetCol > 0){
            for(var i = 0; i < currentBrick.length; i++){
                var j = 0;
                while(currentBrick[i][j] != 1){
                    j++;
                }
                $(function(){
                    inX = currentBrickOffsetRow + i;
                    inY = currentBrickOffsetCol + j - 1;
                    var theLeftBrick = $('#r'+ inX+ 'c'+ inY).attr('class');
                    if(theLeftBrick == 'solid'){
                        toLeft = 0;
                    }
                });
            }
            if(toLeft == 1){
                currentBrickOffsetCol--;
            }
        }else if(inLeftRight == 'right' && currentBrickOffsetCol < _COLS_NUM - currentBrick[currentBrick.length - 1].length){
            for(var i = 0; i < currentBrick.length; i++){
                var j = currentBrick[i].length - 1;
                while(currentBrick[i][j] != 1){
                    j--;
                }
                $(function(){
                    inX = currentBrickOffsetRow + i;
                    inY = currentBrickOffsetCol + j + 1;
                    var theLeftBrick = $('#r'+ inX+ 'c'+ inY).attr('class');
                    if(theLeftBrick == 'solid'){
                        toLeft = 0;
                    }
                });
            }
            if(toLeft == 1){
                currentBrickOffsetCol++;
            }
        }
        DisplayBrick(currentBrick, currentBrickOffsetRow, currentBrickOffsetCol);
    }
}

//Move Down
function BrickDown(){
    //alert(droping);
    if(dropSwitch == 1 && currentDropSpeed != 0){
        currentDropSpeed = 0;
        clearTimeout(droping);
        BrickDroping();
    }
}

//Brick Turn
function BrickTurn(){
    if(dropSwitch == 1 && turnReady == 1){
        turnReady = 0;
        var turn = 1;
        $(function(){
            var turnWidth = currentBrick.length;
            if(currentBrick[0].length > currentBrick.length){
                turnWidth = currentBrick[0].length;
            }
            for(var i = currentBrickOffsetRow; i < currentBrickOffsetRow + turnWidth; i++){
                //Right
                var rightCol = currentBrickOffsetCol + turnWidth - 1;
                var rightClass = $('#r'+ i+ 'c'+ rightCol).attr('class');
                if(rightClass == 'solid'){
                    turn = 0;
                    break;
                }
            }
            if(turn == 1){
                for(var i = currentBrickOffsetCol; i < currentBrickOffsetCol + turnWidth; i++){
                    //Bottom
                    var btmRow = currentBrickOffsetRow + turnWidth - 1;
                    var btmClass = $('#r'+ btmRow+ 'c'+ i).attr('class');
                    if(btmClass == 'solid'){
                        turn = 0;
                        break;
                    }
                }
            }
            var turnBtmRow = currentBrickOffsetRow + currentBrick[0].length;
            if(turnBtmRow > _ROWS_NUM){
                turn = 0;
            }
        });
        if(turn == 1){
            var brickRows = currentBrick.length;
            var brickCols = currentBrick[0].length;
            var tempBrick = new Array();
            tempBrick = currentBrick.slice();

            currentBrick = new Array();
            for(var i = 0; i < brickCols; i++){
                currentBrick[i] = new Array();
                for(var j = 0; j < brickRows; j++){
                    currentBrick[i][j] = tempBrick[brickRows - j - 1][i];
                }
            }
            while(currentBrick[0].length + currentBrickOffsetCol > _COLS_NUM){
                BrickLeftRight('left');
            }
        }
        turnReady = 1;
        DisplayBrick(currentBrick, currentBrickOffsetRow, currentBrickOffsetCol);
    }
}

//Brick Drop
function BrickDroping(){
    if(dropSwitch == 1){
        currentBrickOffsetRow++;
        if(BrickStop(currentBrick) == 'stop'){//Reach Bottom
            //romoval full row
        }else if(BrickStop(currentBrick) == 'drop'){
            droping = setTimeout(function(){
                DisplayBrick(currentBrick, currentBrickOffsetRow, currentBrickOffsetCol);
                BrickDroping();
            }, currentDropSpeed);
        }
    }
}

//Eliminate Rows
function EliminateRows(){
    if(dropSwitch == 1){
        thisElim = 0;
        $(function(){
            for(var i = 0; i < _ROWS_NUM; i++){
                var thisRow = 0;
                for(var j = 0; j < _COLS_NUM; j++){
                    var checkClass = $('#r'+ i+ 'c'+ j).attr('class');
                    if(checkClass == 'solid'){
                        thisRow++;
                    }
                    if(checkClass == 'void'){
                        break;
                    }
                    if(thisRow == _COLS_NUM){
                        $('.row_'+ i+ ' td').attr('style', '').attr('class', 'void');
                        thisElim++;
                        for(var x = i; x > 0; x--){
                            for(var y = 0; y < _COLS_NUM; y++){
                                var preX = x - 1;
                                var inStyle = $('#r'+ preX+ 'c'+ y).attr('style');
                                var inClass = $('#r'+ preX+ 'c'+ y).attr('class');
                                $('#r'+ x+ 'c'+ y).attr('style', inStyle).attr('class', inClass);
                            }
                        }
                    }
                }
            }
        });
    }
}

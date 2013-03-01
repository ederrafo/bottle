/**
 * Created with PyCharm.
 * User: myth
 * Date: 13-2-19
 * Time: 下午1:31
 * To change this template use File | Settings | File Templates.
 */

var btnDownStyle = 'background-color: #ccc;'

$(function(){
    $('body').mousemove(function(){
        $('#clicker td').attr('style', '');
        $('#restart').attr('style', '');
    });
    $('#start').mousedown(function(){
        var dropSwitch = Start();
        var start;
        if(dropSwitch == 0){
            //clearTimeout(droping);
            start = 'START';
        }else{
            start = 'PAUSE';
        }
        $(this).attr('style', btnDownStyle).html(start);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#turn').mousedown(function(){
        BrickTurn();
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#down').mousedown(function(){
        BrickDown();
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#left').mousedown(function(){
        BrickLeftRight('left');
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#right').mousedown(function(){
        BrickLeftRight('right');
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#restart').mousedown(function(){
        var restart = confirm('Are you sure Restart?');
        if(restart == true){
            window.location = location.href;
        }
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#slow').mousedown(function(){
        var dropSpeedMark = SpeedFastSlow('slow');
        $('#current_speed').html(dropSpeedMark);
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    $('#fast').mousedown(function(){
        var dropSpeedMark = SpeedFastSlow('fast');
        $('#current_speed').html(dropSpeedMark);
        $(this).attr('style', btnDownStyle);
    }).mouseup(function(){
            $(this).attr('style', '');
        });

    if(window.event){
        $('body').keydown(function(event){
            switch(event.keyCode){
                //Blank: 32
                case 32:
                    var dropSwitch = Start();
                    var start;
                    if(dropSwitch == 0){
                        start = 'START';
                    }else{
                        start = 'PAUSE';
                    }
                    $('#start').attr('style', btnDownStyle).html(start);
                    break;
                //Up: 38
                case 38:
                    BrickTurn();
                    $('#turn').attr('style', btnDownStyle);
                    break;
                //Down: 40
                case 40:
                    BrickDown();
                    $('#down').attr('style', btnDownStyle);
                    break;
                //Left: 37
                case 37:
                    BrickLeftRight('left');
                    $('#left').attr('style', btnDownStyle);
                    break;
                //Right: 39
                case 39:
                    BrickLeftRight('right');
                    $('#right').attr('style', btnDownStyle);
                    break;
            }
        }).keyup(function(event){
                $('#clicker td').attr('style', '');
            });
    }else{
        $(window).keydown(function(event){
            switch(event.keyCode){
                //Blank: 32
                case 32:
                    var dropSwitch = Start();
                    if(dropSwitch == 0){
                        start = 'START';
                    }else{
                        start = 'PAUSE';
                    }
                    $('#start').attr('style', btnDownStyle).html(start);
                    break;
                //Up: 38
                case 38:
                    BrickTurn();
                    $('#turn').attr('style', btnDownStyle);
                    break;
                //Down: 40
                case 40:
                    BrickDown();
                    $('#down').attr('style', btnDownStyle);
                    break;
                //Left: 37
                case 37:
                    BrickLeftRight('left');
                    $('#left').attr('style', btnDownStyle);
                    break;
                //Right: 39
                case 39:
                    BrickLeftRight('right');
                    $('#right').attr('style', btnDownStyle);
                    break;
            }
        }).keyup(function(event){
                $('#clicker td').attr('style', '');
            });
    }
});
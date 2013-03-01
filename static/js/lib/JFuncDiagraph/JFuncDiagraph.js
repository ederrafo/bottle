/*
 * JFuncDiagraph v0.4.1
 * http://www.oglen.net/demo/JFuncDiagraph/
 *
 * Copyright 2011, Justin Fang
 *
 * Date: 2011-12-2
 */

function JFuncDiagraph(context, width, height, xp, yp, zoom, bg){

    this.context = context;
    this.width = width;
    this.height = height;

    this.xp = xp;
    this.yp = yp;

    this.zoom = zoom;
    this.brkMax = 800000;

    if(typeof JFuncDiagraph._initialized == "undefined"){

        JFuncDiagraph.prototype.drawEachFuncDiagraph = function(arr){

            var succArr = 1;
            var iBrk = 100;

            this.deltaSMax = 1;
            this.deltaSMin = 0.5;

            this.yMax = this.yp / this.zoom;
            this.yMin = (this.yp - this.height) / this.zoom;

            this.xMin = -this.xp / this.zoom;
            this.xMax = (-this.xp + this.width) / this.zoom;

            this.theMin = 2e-20;

            var tempA, tempB;

            if(Math.abs(this.xMax) > Math.abs(this.xMin)){
                tempA = Math.abs(this.xMax);
            }else{
                tempA = Math.abs(this.xMin);
            }

            if(Math.abs(this.yMax) > Math.abs(this.yMin)){
                tempB = Math.abs(this.yMax);
            }else{
                tempB = Math.abs(this.yMin);
            }

            this.rMax = Math.pow(Math.pow(tempA, 2) + Math.pow(tempB, 2), 0.5);

            for(var j = 0; j < arr.length; j++){

                var succ = 0;
                if(arr[j] && arr[j][2] == 1){
                    try{
                        this.context.fillStyle = arr[j][1];

                        var sem;
                        var exprs = arr[j][0];
                        var expr = new Array();
                        var n = 0;

                        var qArea = new Array();

                        do{
                            sem = exprs.search(/;/);

                            if(exprs.length > 0){
                                if(sem == -1){
                                    expr[n] = $.trim(exprs.slice(0, exprs.length));
                                    break;
                                }else{
                                    expr[n] = $.trim(exprs.slice(0, sem));
                                    exprs = exprs.slice(sem+1, exprs.length);
                                }
                            }else{
                                break;
                            }
                            n++;
                        }while(sem != -1)

                        //****************************************************

                        if(expr.length > 1){

                            var para = 0;

                            for(var l = 0; l < expr.length; l++){
                                if(expr[l].search(/q/) != -1){
                                    if(para < 2){
                                        expr[l] = new Function('q', 'return ' + expr[l]);
                                    }else{
                                        qArea[0] =  new Function('return ' + $.trim(expr[l].slice(expr[l].search(/\(/)+1, expr[l].search(/,/))));
                                        qArea[1] =  new Function('return ' + $.trim(expr[l].slice(expr[l].search(/,/)+1, expr[l].search(/\)/))));
                                    }
                                    para++;
                                }else{
                                    expr[l] = new Function('x', 'return ' + expr[l]);
                                    para--;
                                }
                            }

                            if(para == expr.length){
                                //parametric equation

                                this.context.fillStyle = arr[j][1];

                                if(typeof qArea[0] == 'function')
                                    var q = qArea[0]();
                                else
                                    var q = 0;

                                var tempQ = null;
                                var tempX = null;
                                var tempY = null;

                                var deltaQ = 1 / this.zoom;
                                var brk = 0;

                                do {
                                    if(tempQ == null){

                                        var x = expr[0](q);
                                        var y = expr[1](q);

                                        tempX = x;
                                        tempY = y;
                                        tempQ = q;

                                    }else{
                                        var i = 0;
                                        tempQ = q;

                                        do{
                                            var x = expr[0](tempQ);
                                            var y = expr[1](tempQ);


                                            if(y > this.yMax || y < this.yMin){
                                                break;
                                            }

                                            deltaX = Math.abs(x - tempX);
                                            deltaY = Math.abs(y - tempY);

                                            var c = Math.pow(deltaY * this.zoom, 2) + Math.pow(deltaX * this.zoom, 2);
                                            var cMax = Math.pow(this.deltaSMax, 2);
                                            var cMin = Math.pow(this.deltaSMin, 2);

                                            if(c > cMax){

                                                if(deltaQ > this.theMin){
                                                    deltaQ = deltaQ / 2;
                                                    tempQ = q + deltaQ;
                                                }else{
                                                    deltaQ = this.theMin;
                                                    tempQ = q + deltaQ;
                                                    break;
                                                }
                                            }

                                            if(c < cMin){
                                                deltaQ = deltaQ * 2;
                                                tempQ = q + deltaQ;
                                            }

                                            if(i > iBrk){
                                                break;
                                            }
                                            i++;

                                        }while(c > cMax || c < cMin)

                                        tempX = x;
                                        tempY = y;

                                    }

                                    if(typeof y != 'function' && y)
                                        succ = 1;

                                    xi = x * this.zoom;
                                    yi = y * this.zoom;

                                    this.context.fillRect(xi-1, yi, 1, 1);

                                    q += deltaQ;

                                    if(brk > this.brkMax)
                                        break;
                                    brk++;

                                    if(typeof qArea[1] == 'function'){
                                        if(q > qArea[1]())
                                            break;
                                    }else{
                                        if(!(Math.abs(x) < this.rMax && Math.abs(y) < this.rMax))
                                            break;
                                    }
                                } while (1);

                            }else if(para == -expr.length){

                                for(var m = 0; m < expr.length; m++){


                                    this.context.fillStyle = arr[j][1];

                                    var x = this.xMin;

                                    var tempX = null;
                                    var tempY = null;

                                    var deltaX = 1 / this.zoom;
                                    var deltaY = null;

                                    var brk = 0;

                                    do {
                                        if(tempY == null){
                                            var y = expr[m](x);
                                            tempY = y;

                                        }else{
                                            var i = 0;
                                            tempX = x;

                                            do{
                                                y = expr[m](tempX);

                                                if(y > this.yMax || y < this.yMin){
                                                    break;
                                                }

                                                deltaY = Math.abs(y - tempY);

                                                var c = Math.pow(deltaY * this.zoom, 2) + Math.pow(deltaX * this.zoom, 2);
                                                var cMax = Math.pow(this.deltaSMax, 2);
                                                var cMin = Math.pow(this.deltaSMin, 2);

                                                if(c > cMax){

                                                    if(deltaX > this.theMin){
                                                        deltaX = deltaX / 2;
                                                        tempX = x + deltaX;
                                                    }else{
                                                        deltaX = this.theMin;
                                                        tempX = x + deltaX;
                                                        break;
                                                    }
                                                }

                                                if(c < cMin){

                                                    if(deltaX > 1 / this.zoom){
                                                        deltaX = 1 / this.zoom;
                                                        tempX = x + deltaX;
                                                        break;
                                                    }else{
                                                        deltaX = deltaX * 2;
                                                        tempX = x + deltaX;
                                                    }
                                                }

                                                if(i > iBrk){
                                                    break;
                                                }
                                                i++;

                                            }while(c > cMax || c < cMin)

                                            tempY = y;

                                        }

                                        if(typeof y != 'function' && y)
                                            succ = 1;

                                        xi = x * this.zoom;
                                        yi = y * this.zoom;

                                        this.context.fillRect(xi-1, yi, 1, 1);

                                        x += deltaX;

                                        if(brk > this.brkMax)
                                            break;
                                        brk++;

                                    } while (x <= this.xMax);
                                }
                            }else{

                                return false;
                            }

                        }else{
                            expr[0] = new Function('x', 'return ' + expr[0]);

                            this.context.fillStyle = arr[j][1];

                            var x = this.xMin;

                            var tempX = null;
                            var tempY = null;

                            var deltaX = 1 / this.zoom;
                            var deltaY = null;

                            var brk = 0;

                            do {

                                if(tempY == null){
                                    var y = expr[0](x);
                                    tempY = y;

                                }else{
                                    var i = 0;
                                    tempX = x;

                                    do{
                                        var y = expr[0](tempX);

                                        if(y > this.yMax || y < this.yMin){
                                            break;
                                        }

                                        deltaY = Math.abs(y - tempY);

                                        var c = Math.pow(deltaY * this.zoom, 2) + Math.pow(deltaX * this.zoom, 2);
                                        var cMax = Math.pow(this.deltaSMax, 2);
                                        var cMin = Math.pow(this.deltaSMin, 2);

                                        if(c > cMax){

                                            if(deltaX > this.theMin){
                                                deltaX = deltaX / 2;
                                                tempX = x + deltaX;
                                            }else{
                                                deltaX = this.theMin;
                                                tempX = x + deltaX;
                                                break;
                                            }
                                        }

                                        if(c < cMin){

                                            if(deltaX > 1 / this.zoom){
                                                deltaX = 1 / this.zoom;
                                                tempX = x + deltaX;
                                                break;
                                            }else{
                                                deltaX = deltaX * 2;
                                                tempX = x + deltaX;
                                            }
                                        }

                                        if(i > iBrk){
                                            break;
                                        }
                                        i++;

                                    }while(c > cMax || c < cMin)

                                    tempY = y;

                                }

                                if(typeof y != 'function' && y)
                                    succ = 1;

                                xi = x * this.zoom;
                                yi = y * this.zoom;

                                this.context.fillRect(xi-1, yi, 1, 1);
                                x += deltaX;

                                if(brk > this.brkMax)
                                    break;
                                brk++;

                            } while (x <= this.xMax);
                        }
                    }catch(e){
                        return false;
                    }

                }else{
                    succ = 1;
                }
                succArr &= succ;
                succ = 0;
            }
            return succArr;
        }
        JFuncDiagraph.prototype.position = function(xp, yp){
            this.xp = xp;
            this.yp = yp;

            this.xl = - xp;
            this.xr = - xp + this.width;

            this.clear(bg);
            this.context.save();
            this.context.translate(this.xp, this.yp);
            this.context.scale(1, -1);
        }

        JFuncDiagraph.prototype.zoomInOut = function(zoom){
            this.zoom = zoom;

            this.clear(bg);
            this.context.save();
            this.context.translate(this.xp, this.yp);
            this.context.scale(1, -1);
        }

        JFuncDiagraph.prototype.clear = function(color){
            this.context.restore();
            this.context.fillStyle = color;
            this.context.fillRect(0, 0, this.width, this.height);
        }

        JFuncDiagraph.prototype.drawCoord = function(axisColor, gridColor){

            this.context.beginPath();
            this.context.strokeStyle = gridColor;

            for(var i = -1; i > (this.yp - this.height) / this.zoom; i--){
                this.context.moveTo(- this.xp, i * this.zoom + 0.5);
                this.context.lineTo(this.width - this.xp, i * this.zoom + 0.5);
            }
            for(var i = 1; i < this.yp / this.zoom; i++){
                this.context.moveTo(- this.xp, i * this.zoom + 0.5);
                this.context.lineTo(this.width - this.xp, i * this.zoom + 0.5);
            }
            for(var i = -1; i > - this.xp / this.zoom; i--){
                this.context.moveTo(i * this.zoom - 0.5, this.yp - this.height);
                this.context.lineTo(i * this.zoom - 0.5, this.yp);
            }
            for(var i = 1; i < (this.width - this.xp) / this.zoom; i++){
                this.context.moveTo(i * this.zoom - 0.5, this.yp - this.height);
                this.context.lineTo(i * this.zoom - 0.5, this.yp);
            }

            this.context.closePath();
            this.context.stroke();

            this.context.beginPath();
            this.context.strokeStyle = axisColor;

            this.context.moveTo(- this.xp, 0.5);
            this.context.lineTo(this.width - this.xp, 0.5);

            this.context.moveTo(-0.5, this.yp - this.height);
            this.context.lineTo(-0.5, this.yp);
            this.context.stroke();
        }

        JFuncDiagraph._initialized == true;
    }
    this.clear(bg);

    this.context.save();
    this.context.translate(this.xp, this.yp);
    this.context.scale(1, -1);

}
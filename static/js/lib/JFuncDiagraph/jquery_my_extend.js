//My jQuery extends
jQuery.fn.extend({
    shake: function(inPeriod, inAmplitude, inDamping){

        this.each(function(){

            var actor = $(this);

            if(typeof(this.marginL) == 'undefined'){

                var marginL = actor.css('margin-left');
                marginL = parseInt(marginL.substr(0, marginL.length - 2));

                if(isNaN(marginL)){
                    this.marginL = 0;
                }else{
                    this.marginL = marginL;
                }
            }

            if(typeof(this.marginR) == 'undefined'){

                var marginR = actor.css('margin-right');
                marginR = parseInt(marginR.substr(0, marginR.length - 2));

                if(isNaN(marginR)){
                    this.marginR = 0;
                }else{
                    this.marginR = marginR;
                }
            }
            if(typeof(this.i) == 'undefined'){
                this.i = 1;
            }

            var amplitude = Math.floor(inAmplitude * Math.pow(inDamping, this.i));

            if(this.i % 2 == 0){
                marginL = this.marginL + amplitude;
                marginR = this.marginR - amplitude;
            }else{
                marginL = this.marginL - amplitude;
                marginR = this.marginR + amplitude;
            }
            this.i++;

            actor.animate({
                marginLeft: marginL + "px",
                marginRight: marginR + "px"
            }, inPeriod / 4, function(){

                if(amplitude > 0){
                    actor.shake(inPeriod, amplitude, inDamping);
                }else{
                    this.i = 1;
                }

            });

        });
    },
    undulate: function(inPeriod, inAmplitude, inDamping){
        this.each(function(){

            var actor = $(this);

            if(typeof(this.marginT) == 'undefined'){

                var marginT = actor.css('margin-top');
                marginT = parseInt(marginT.substr(0, marginT.length - 2));

                if(isNaN(marginT)){
                    this.marginT = 0;
                }else{
                    this.marginT = marginT;
                }
            }

            if(typeof(this.marginB) == 'undefined'){

                var marginB = actor.css('margin-bottom');
                marginB = parseInt(marginB.substr(0, marginB.length - 2));

                if(isNaN(marginB)){
                    this.marginB = 0;
                }else{
                    this.marginB = marginB;
                }
            }
            if(typeof(this.i) == 'undefined'){
                this.i = 1;
            }

            var amplitude = Math.floor(inAmplitude * Math.pow(inDamping, this.i));

            if(this.i % 2 == 0){
                marginT = this.marginT + amplitude;
                marginB = this.marginB - amplitude;
            }else{
                marginT = this.marginT - amplitude;
                marginB = this.marginB + amplitude;
            }
            this.i++;

            actor.animate({
                marginTop: marginT + "px",
                marginBottom: marginB + "px"
            }, inPeriod / 4, function(){

                if(amplitude > 0){
                    actor.undulate(inPeriod, amplitude, inDamping);
                }else{
                    this.i = 1;
                }

            });

        });
    },
    fadeOutReset: function(inDelay){
        return this.each(function(){
            var obj = $(this);
            obj.stop().animate({
                opacity: 0
            }, 0, function(){
                obj.animate({
                    opacity: 1
                } ,500, function(){
                    obj.animate({
                        opacity: 0
                    }, inDelay);
                });
            });
        });
    }
});
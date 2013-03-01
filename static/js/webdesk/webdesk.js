$(document).ready(function(){

    $('body').disableSelection();

    $(window).resize(function(){
        WindowAlign();
    });

    var count_win     = 0;
    var count_clo     = 0;
    var janela_name = '';

    function WindowAlign()
    {
        $(window).width();
        $(window).height();

        $('#centro #janela').each(function(i){

            if(!$(this).attr('title'))
            {
                if(i<=3)
                {
                    posX = 20;
                    posY = (220*i)+(($(window).width()/2)-(220+320));
                }
                if(i>3)
                {
                    posX = 260;
                    posY = ((220*i)-(220*4))+(($(window).width()/2)-(220+320));
                }
                $(this).animate({
                    'top'        :''+posX+'px',
                    'left'        :''+posY+'px',
                    'width'        :'400px',
                    'height'    :'400px'
                },{
                    queue        :false,
                    duration    :600,
                    easing        :'easeOutBack'
                });
            }

        });
    }

    function WindowFocus(winSel,focusType,buttonFull,focusReturn)
    {
        if(focusType)
        {
            WindowFocus('#centro #janela');
            $(winSel).attr('title','max');
            $(winSel).css({
                'z-index'    :'55',
                'opacity'    :'1'
            }).animate({
                    scale        :[1],
                    'top'        :$('input[name=win_posY]',winSel).val(),
                    'left'        :$('input[name=win_posX]',winSel).val(),
                    'width'        :$('input[name=win_sizeX]',winSel).val()+'px',
                    'height'    :$('input[name=win_sizeY]',winSel).val()+'px'
                },300,'easeOutBack',function(){
                    $(this).draggable('enable').resizable('enable');
                    $('#func li',this).show(0,function(){
                        if(!buttonFull)    $('.maximize',real_this).hide();
                    });
                    $('iframe',this).fadeIn(600);
                    $(this).animate({boxShadow:'0 0 50px rgba(0,0,0,0.8)'},600);
                });
        }
        else
        {
            $(winSel).removeAttr('title');
            $(winSel+' iframe').hide(0,function(){
                $(this).parents('#janela').css({
                    'z-index'    : '50',
                    'opacity'    : '0.3',
                    'box-shadow': 'none'
                }).animate({
                        scale         : [0.5]
                    },{
                        queue        :false,
                        duration    :300,
                        easing        :'easeOutBack',
                        complete: function(){
                            $(this).draggable('disable').resizable('disable');
                            $('#func li',this).hide();
                            if(!focusReturn) WindowAlign();
                        }
                    });
            });
        }
    }

    function WindowCreate(imgTitle,title,name,content,sizeX,sizeY,resizeEnable,buttonFull)
    {
        if(!$('#centro #janela[align='+name+']').attr('id'))
        {
            WindowFocus('#centro #janela');

            count_win++;
            count_clo++;

            html_window  = '<div id="janela" class="janela_'+count_win+'" align="'+name+'" title="max">';
            html_window += '<input type="hidden" name="win_sizeX" value="'+sizeX+'">';
            html_window += '<input type="hidden" name="win_sizeY" value="'+sizeY+'">';
            html_window += '<input type="hidden" name="win_posX" value="'+(count_clo*5)+'px">';
            html_window += '<input type="hidden" name="win_posY" value="'+(count_clo*5)+'px">';
            html_window += '<div id="content">';
            html_window += '<ul>';
            html_window += '    <li id="cabecalho">';
            html_window += '    <ul>';
            html_window += '        <li id="mini"><img src="'+http_url+'/icones/dock/'+imgTitle+'.png" alt=""></li>';//http://webdesktop.levelhard.com.br
            html_window += '        <li id="text"><p>'+title+'</p></li>';
            html_window += '        <li id="func">';
            html_window += '        <ul>';
            html_window += '            <li class="iconize"><img src="'+http_url+'/icones/janela/view_multicolumn.png" alt=""></li>';
            html_window += '            <li class="maximize"><img src="'+http_url+'/icones/janela/windows_fullscreen.png" alt=""></li>';
            html_window += '            <li class="close"><img src="'+http_url+'/icones/janela/window_suppressed.png" alt=""></li>';
            html_window += '        </ul>';
            html_window += '        </li>';
            html_window += '    </ul>';
            html_window += '    </li>';
            html_window += '    <li id="conteudo"><iframe src="" allowtransparency="1"></iframe></li>';
            html_window += '</ul>';
            html_window += '</div>';
            html_window += '</div>';

            $('#centro').append(html_window);
            //===========Monta e Anima Janela
            $('.janela_'+count_win).css({'z-index':'55'}).animate({
                'width'        :''+sizeX+'px',
                'height'    :''+sizeY+'px',
                'top'        :''+(count_clo*5)+'px',
                'left'        :''+(count_clo*5)+'px',
                'opacity'    :'1',
            },600,'easeOutBack',function(){
                $('#conteudo iframe',this).hide().attr('src',content);
                $(this).animate({boxShadow:'0 0 50px rgba(0,0,0,0.8)'},600,function(){
                    $('#conteudo iframe',this).fadeIn(600);
                });
                //===========Ativa Drag de Janela
                $(this).draggable({
                    containment        : 'parent',
                    cursor            : 'move',
                    handle             : '#cabecalho',
                    cancel            : 'img',
                    iframeFix        : true,
                    scroll            : false,
                    start            : function(){
                        $('#conteudo iframe',this).hide();
                        $(this).css({'box-shadow':'none'});
                    },
                    stop            : function(){
                        $('input[name=win_posX]',this).val($(this).css('left'));
                        $('input[name=win_posY]',this).val($(this).css('top'));
                        $('#conteudo iframe',this).fadeIn(600);
                        $(this).animate({boxShadow:'0 0 50px rgba(0,0,0,0.8)'},600);
                    }
                });
                //===========Ativa Resize de Janela
                if(resizeEnable)
                {
                    $(this).resizable({
                        containment        : 'parent',
                        minWidth        : 350,
                        minHeight        : 100,
                        animate            : true,
                        animateEasing    : 'easeOutBack',
                        start            : function(){
                            $('#conteudo iframe',this).hide();
                            $('#wrap-window').hide();
                            $(this).css({'box-shadow':'none'});
                        },
                        stop            : function(){
                            $('#wrap-window').fadeOut(600);
                            $('#conteudo iframe',this).fadeIn(600);
                            $(this).animate({boxShadow:'0 0 50px rgba(0,0,0,0.8)'},600);
                        }
                    });
                }
                //===========Desativa FullScreen
                if(!buttonFull)
                {
                    $('.maximize',this).hide();
                }
            });
            //===========Efeitos nos Icones da Janela
            $('.janela_'+count_win+' #cabecalho img').hover(function(){
                $(this).stop().animate({opacity:'0.6'},600);
            },function(){
                $(this).stop().animate({opacity:'1'},600);
            });
            //===========Focus na Janela
            $('.janela_'+count_win).click(function(){
                if($(this).css('opacity')<1)
                {
                    WindowFocus(this,1,buttonFull);
                }
            });
            //===========Funções Clique
            $('.janela_'+count_win+' #func li').click(function(){
                //===========Desfoque de Janela
                if($(this).attr('class') == 'iconize')
                {
                    $(this).parents('#janela').removeAttr('title');
                    $(this).parents('#janela').animate({'opacity':'1'},100,function(){
                        real_this = this;
                        $('iframe',this).hide(0,function(){
                            $(real_this).css({
                                'z-index'        :'50',
                                'opacity'        :'0.3',
                                'box-shadow'    : 'none'
                            }).animate({
                                    scale            :[0.5]
                                },300,'easeOutBack',function(){
                                    $(this).draggable('disable').resizable('disable');
                                    $('#func li',this).hide();
                                    WindowAlign();
                                });
                        });
                    });
                }
                //===========Maximiza Janela
                if($(this).attr('class') == 'maximize')
                {
                    $(this).parents('#janela').animate({'opacity':'1',boxShadow:'none'},0,function(){
                        real_this = this;
                        $('iframe',this).animate({'opacity':'0'},0,function(){
                            $(real_this).animate({
                                'width'        :'100%',
                                'height'    :'100%',
                                'top'        :-46,
                                'left'        :-8
                            },600,'easeInBack',function(){
                                $('#cabecalho',this).animate({'top':'-30px','opacity':'0.2'},0,function(){
                                    $(this).hover(function(){
                                        $(this).stop().animate({'top':'0px','opacity':'1'},300);
                                    },function(){
                                        $(this).stop().animate({'top':'-30px','opacity':'0.2'},300);
                                    });
                                    $('.iconize',this).hide();
                                    $('.maximize img',this).attr('src',http_url+'/icones/janela/windows_nofullscreen.png');
                                    $('.maximize',this).attr('class','minimize');
                                    $('iframe',real_this).animate({'opacity':'1'},function(){
                                        $('#wrap').hide();
                                    });
                                });
                            });
                        });
                    });
                }
                //===========Minimiza Janela
                if($(this).attr('class') == 'minimize')
                {
                    $(this).parents('#janela').animate({'opacity':'1'},0,function(){
                        real_this = this;
                        $('#cabecalho',real_this).unbind('mouseenter mouseleave');
                        $('#cabecalho',real_this).animate({'top':'-38px','opacity':'1'},0,function(){
                            $('iframe',real_this).animate({'opacity':'0'},0,function(){
                                $(real_this).animate({
                                    'width'        :''+sizeX+'px',
                                    'height'    :''+sizeY+'px',
                                    'top'        :''+(count_clo*5)+'px',
                                    'left'        :''+(count_clo*5)+'px',
                                },600,'easeOutBack',function(){
                                    $(this).animate({boxShadow:'0 0 15px rgba(0,0,0,0.8)'},0);
                                    $('.iconize',this).show();
                                    $('.minimize img',this).attr('src',http_url+'/icones/janela/windows_fullscreen.png');
                                    $('.minimize',this).attr('class','maximize');
                                    $('iframe',real_this).animate({'opacity':'1'},function(){
                                        $('#wrap').hide();
                                    });
                                });
                            });
                        });
                    });
                }
                //===========Fecha Janela
                if($(this).attr('class') == 'close')
                {
                    $('#wrap').show();
                    $(this).parents('#janela').animate({'opacity':'1',boxShadow:'none'},0,function(){
                        real_this = this;
                        $('iframe',this).hide(0,function(){
                            $(real_this).animate({scale:[0],'opacity':'0'},600,'easeInBack',function(){
                                count_clo--
                                $(this).remove();
                                $('#wrap').hide();
                                WindowAlign();
                            });
                        });
                    });
                }
            });
        }
        else
        {
            WindowFocus('#centro #janela[align='+name+']',1,buttonFull);
        }

    }

    $('#wrap, #loader').show();
    $('#menu li').transform({scale:[0]});
    window.onload = function(){

        $('#wrap, #loader').fadeOut(300,function(){
            //=============Logo Montador
            for(i=1;i<=$('#logo p').length;i++)
            {
                $('#logo p:nth-child('+i+')').delay(i*100).animate({rotate:'360deg','top':'0px','left':'0px','opacity':'1'},800,'easeOutBack');
            }
            //=============Menu Montador
            for(a=1;a<=$('#menu li').length;a++)
            {
                $('#menu li:nth-child('+a+')').delay(a*50).animate({scale:[1]},800,'easeOutBack');
            }
            //=============Logo Drag
            $('#logo p').draggable({ containment: '#centro' });
        });
        //=============Menu Sortable
        $('#menu-sort').sortable({containment:'parent'});
        //=============Menu Hover
        $('#menu li').hover(function(){
            $('img',this).animate({translateY:'-15px',scale:[1.2],boxShadow:'0 15px 30px rgba(0,0,0,1)'},{queue:false,duration:600,easing:'easeOutBack'});
        },function(){
            $('img',this).animate({translateY:'0px',scale:[1.0],boxShadow:'0 1px 3px rgba(0,0,0,0.6)'},{queue:false,duration:600,easing:'easeOutBack'});
        });
        //=============Menu Click
        $('#menu li').click(function(){

            if($(this).attr('class') == 'agenda')
            {
                WindowCreate('wallet','WebAgenda 1.7',$(this).attr('class'),'http://webdesktop.levelhard.com.br/conteudo/agenda','918','575');
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'diretorio')
            {
                WindowCreate('icon_downloads','File Manager 1.0',$(this).attr('class'),'http://webdesktop.levelhard.com.br/conteudo/diretorio','480','480',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'admin')
            {
                WindowCreate('xcode','Painel de Controle Geral',$(this).attr('class'),'http://admin.levelhard.com','900','520',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'odontograma')
            {
                WindowCreate('pages','Odontograma',$(this).attr('class'),'http://webdesktop.levelhard.com.br/conteudo/odontograma/','965','470');
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'jogo')
            {
                WindowCreate('chess','jQuery Games',$(this).attr('class'),'http://webdesktop.levelhard.com.br/conteudo/jogo','520','520',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'video')
            {
                WindowCreate('icon_imovie','Galeria de Videos',$(this).attr('class'),'http://webdesktop.levelhard.com.br/conteudo/video','840','520',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'desenho')
            {
                //http://webdesktop.levelhard.com.br/conteudo/desenho
                WindowCreate('textedit','HTML5 SketchPad',$(this).attr('class'),'/webdesk/desenho','640','480');
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'webclin')
            {
                WindowCreate('icon_textedit','WebClin 2.0',$(this).attr('class'),'http://webclin.levelhard.com','1000','580',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }
            if($(this).attr('class') == 'browser')
            {
                WindowCreate('icon_chrome','jBrowser 1.0',$(this).attr('class'),'http://levelhard.com.br/','800','480',1,1);
                $('#wrap').fadeIn(300);
                $('img',this).animate({bottom:'50px'},300,function(){
                    $(this).animate({bottom:'0px'},600,'easeOutBounce',function(){
                        $('#wrap').fadeOut(300);
                    });
                });
            }

        });
        //=============Altera Logo
        $('input[name=intera]').keyup(function(e){

            if(e.keyCode == 13)
            {
                if($('input[name=intera]').val())
                {
                    $('#menu li').unbind('keyup');

                    var teste = '';
                    $.each($(this).val(),function(i,l){
                        teste = teste+'<p>'+l+'</p>';
                    });
                    $('#logo').html(teste);

                    for(i=1;i<=$('#logo p').length;i++)
                    {
                        $('#logo p:nth-child('+i+')').delay(i*100).animate({rotate:'360deg','top':'0px','left':'0px','opacity':'1'},800,'easeOutBack');
                    }
                    $('#logo p').draggable({containment:'#centro'});
                    $('input[name=intera]').val('');
                }
            }

        });

    }

});
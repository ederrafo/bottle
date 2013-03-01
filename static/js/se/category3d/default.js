var meny = Meny.create({
    menuElement: document.querySelector( '.meny' ),

    contentsElement: document.querySelector( '.contents' ),

    position: Meny.getQuery().p || 'left',

    height: 200,

    width: 260,

    threshold: 40
});

if( Meny.getQuery().u && Meny.getQuery().u.match( /^http/gi ) ) {
    var contents = document.querySelector( '.contents' );
    contents.style.padding = '0px';
    contents.innerHTML = '<div class="cover"></div><iframe src="'+ Meny.getQuery().u +'" style="width: 100%; height: 100%; border: 0; position: absolute;"></iframe>';
}
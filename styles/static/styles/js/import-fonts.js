async function importFonts(fonts){
    const head = document.head
    style = document.createElement('style');

    for (let font of fonts){
        style.appendChild(document.createTextNode(`@import url('${font.link}');`));
    }

    head.appendChild(style);
}

async function getFonts(){
    const fonts = await fetch(`/styles/fonts`);

    return await fonts.json();
}

getFonts().then(fonts =>
    importFonts(fonts)
)

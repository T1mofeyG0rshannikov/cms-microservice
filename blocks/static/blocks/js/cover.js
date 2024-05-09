function setCoverDarkness(block_ancor, darkness){
    darkness = 100 - darkness;
    darkness = darkness / 100;
    console.log(darkness);

    document.getElementById(block_ancor).style.backgroundColor = `rgba(0,0,0, ${darkness})!important;`;
}

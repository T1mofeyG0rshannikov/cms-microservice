function initMobileSwiper(){
    const swiper = new Swiper(".mySwiper", {
        spaceBetween: 20,
        slidesPerView: 1,
        navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
        },
        loop: true,
    });

    swiper.slideTo(1);
}

function initDesctopSwiper(columns){
    const swiper = new Swiper(".mySwiper", {
        spaceBetween: 40,
        slidesPerView: columns,
        navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
        },
        keyboard: true,
        loop: true,
    });
}

function initSwiper(desctopColumns){
    const pageWidth = document.documentElement.scrollWidth;

    console.log(pageWidth)
    console.log(pageWidth < 760)
    if (pageWidth < 760){
        initMobileSwiper();
    }

    else{
        initDesctopSwiper(desctopColumns);
    }
}

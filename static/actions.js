window.onload = function() {
    new Swiper('.swiper', {
        direction: 'horizontal',
        loop: true,
        effect: 'fade',
        autoplay: {
            delay: 3000, //slide stwich time in ms
            disableOnInteraction: true,
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        scrollbar: {
            el: '.swiper-scrollbar',
        },
    })
}
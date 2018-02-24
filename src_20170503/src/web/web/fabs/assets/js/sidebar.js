/**
var swiper2 = new Swiper('.swiper-container.s2', {
    scrollbar: '.s2 .swiper-scrollbar',
    direction: 'vertical',
    slidesPerView: 'auto',
    mousewheelControl: true,
    freeMode: true
});
var swiper = new Swiper('.swiper-container.s1', {
    scrollbar: '.s1 .swiper-scrollbar',
    direction: 'vertical',
    slidesPerView: 'auto',
    mousewheelControl: true,
    freeMode: true
});
var swiper3 = new Swiper('.swiper-container.s3', {
    scrollbar: '.s3 .swiper-scrollbar',
    direction: 'vertical',
    slidesPerView: 'auto',
    mousewheelControl: true,
    freeMode: true
});
 **/



/**
$('nav a').click(function(e) {
    $('nav a.active').removeClass('active');
    //$('.navContent div').addClass('hidden');
    var $this = $(this);
    if (!$this.hasClass('active')) {
        $this.addClass('active');

    }
    var content = $($this.attr('href'));
    if(content){
        content.siblings().addClass('hidden');
        content.removeClass('hidden');
    }
    e.preventDefault();
});
**/

$('nav a').click(function(e) {
    $('nav a.active').removeClass('active');
    var $this = $(this);
    if (!$this.hasClass('active')) {
        $this.addClass('active');

    }
    var content = $($this.attr('href'));
    if(content){
        content.siblings().addClass('hidden');
        content.removeClass('hidden');
    }
    e.preventDefault();
});

$('#body_switch').click(function(e){
    var $this = $('#page_sidebar');
    if($this.hasClass('xd-unfold')){
        $this.removeClass('xd-unfold');
    }else{
        $this.addClass('xd-unfold');
    }
    e.preventDefault();
});


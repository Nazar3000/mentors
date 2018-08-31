$(document).ready(function() {

    // menu mobile
    $('.header-trigger').click(function() {
        $('nav ul').slideToggle(500);
    });
    $(window).resize(function() {
        if ($(window).width() >500) {
            $('nav ul').removeAttr('style');
        }
    });

    // accorderon show

    $(function($){
        var contents = $('.issues-content');
        var titles = $('.issues-title');
        titles.on('click',function(){
            var title = $(this);
            contents.filter(':visible').slideUp(function(){
                $(this).prev('.issues-title').removeClass('is-opened');
            });

            var content = title.next('.issues-content');

            if (!content.is(':visible')) {
                content.slideDown(function(){title.addClass('is-opened')});
            }
        });
    });

    // carousel main page

    $(document).ready(function(){
        $(".owl-carousel").owlCarousel({
            loop:true,
            nav:true,
            dots:true,
            // animateOut: 'fadeOut',
            responsive:{
                0:{
                    items:1
                }
            }
        });
    });


});




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

    // accorderon  main page show

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

    // all message

    $(function($){
        var contents = $('.tape-dialog-all-content');
        var titles = $('.tape-dialog-all');

        titles.on('click',function(){
            var title = $(this);

            contents.filter(':visible').slideUp(function(){
                $(this).siblings('.tape-dialog-all').removeClass('is-opened');
            });
            var content = title.siblings('.tape-dialog-all-content');
            if (!content.is(':visible')) {
                content.slideDown(function(){title.addClass('is-opened')});
            }
        });
    });

    // carousel main page

    $(document).ready(function(){
        $(".owl-carousel").owlCarousel({
            loop:false,
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

    // open diary block

    $('.block-open-more').click(function (event) {
        event.preventDefault();

        var parent = $(this).parents('.diary-block');
        var parent_id = parent.data('id');

        parent.slideToggle(400);
        $('.diary-block-open[data-id='+parent_id+']').slideToggle(400);

    });

    $('.diary-block-close').click(function (event) {
        event.preventDefault();
        var parent = $(this).parents('.diary-block-open');
        var parent_id = parent.data('id');

        $(this).parents('.diary-block-open').slideToggle(400);
        $('.diary-block[data-id='+parent_id+']').slideToggle(400);
    });

    // slider diary

    $('#vertical').lightSlider({
        gallery:true,
        item:1,
        vertical:true,
        verticalHeight:250,
        vThumbWidth:70,
        thumbItem:4,
        thumbMargin:0,
        slideMargin:0,
    });


    // add img

    $("#files, #file").change(function() {
        filename = this.files[0].name;
        // console.log(filename);
    });

    $('input[type=file]').change(function(){
        files = this.files;
        $('.tape-add-img-name').append(files[0].name);
    });

});




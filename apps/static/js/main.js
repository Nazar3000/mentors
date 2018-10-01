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

    $("#files, #file, #filess").change(function() {
        filename = this.files[0].name;
        // console.log(filename);
    });

    $('input[type=file]').change(function(){
        files = this.files;
        $('.tape-add-img-name').append(files[0].name);
    });

    // select2

    $('.js-example-basic-single').select2();

    // star rate script

    /* 1. Visualizing things on Hover - See next part for action on click */
    $('#stars li').on('mouseover', function(){
        var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on

        // Now highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function(e){
            if (e < onStar) {
                $(this).addClass('hover');
            }
            else {
                $(this).removeClass('hover');
            }
        });

    }).on('mouseout', function(){
        $(this).parent().children('li.star').each(function(e){
            $(this).removeClass('hover');
        });
    });

    /* 2. Action to perform on click */
    $('#stars li').on('click', function(){
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');

        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }

        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
    });

    //  admin menu

    $(".admin-menu-on").hide();

    $(".admin-menu-off").click(
        function() {
            $(".admin-menu-on").slideToggle('fast');
        },
        function() {
            $(".admin-menu-on").slideToggle('fast');
        }
    );


    // relativeanchor

    $('a[rel="relativeanchor"]').click(function() {
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top - 20
        }, 1000);
        return false;
    });

    $('.career-add').click(function(){
        $('.career-modal-reg').fadeIn(500);
    });

    $('.career-card-close').click(function(){
        $('.career-modal-reg').fadeOut(400);
    });

    $('.complaint').click(function(){
        $('.complaint-modal').fadeIn(500);
    });

    $('.complaint-close').click(function(){
        $('.complaint-modal').fadeOut(400);
    });

    $('.rate-place').click(function(){
        $('.rate-place-modal').fadeIn(500);
    });

    $('.rate-place-close').click(function(){
        $('.rate-place-modal').fadeOut(400);
    });



    // go top auto

    $(function() {
        $.fn.scrollToTop = function() {
            $(this).hide().removeAttr("href");
            if ($(window).scrollTop() >= "250") $(this).fadeIn("slow")
            var scrollDiv = $(this);
            $(window).scroll(function() {
                if ($(window).scrollTop() <= "250") $(scrollDiv).fadeOut("slow")
                else $(scrollDiv).fadeIn("slow")
            });
            $(this).click(function() {
                $("html, body").animate({scrollTop: 0}, "slow")
            })
        }
    });
    $(function() {
        $("#go-top").scrollToTop();
    });


});




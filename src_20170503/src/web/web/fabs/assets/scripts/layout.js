var Layout = function () {

    var layoutImgPath = 'assets/images';

    var layoutCssPath = 'assets/styles';

    var resBreakpointMd = Fabs.getResponsiveBreakpoint('md');

    var handleSidebarAndContentHeight = function () {
        var content = $('.page-content');
        var sidebar = $('.page-sidebar');
        var body = $('body');
        var height;

        if (body.hasClass("page-footer-fixed") === true && body.hasClass("page-sidebar-fixed") === false) {
            var available_height = Fabs.getViewPort().height - $('.page-footer').outerHeight() - $('.page-header').outerHeight();
            if (content.height() < available_height) {
                content.attr('style', 'min-height:' + available_height + 'px');
            }
        } else {
            if (body.hasClass('page-sidebar-fixed')) {
                height = _calculateFixedSidebarViewportHeight();
                if (body.hasClass('page-footer-fixed') === false) {
                    height = height - $('.page-footer').outerHeight();
                }
            } else {
                var headerHeight = $('.page-header').outerHeight();
                var footerHeight = $('.page-footer').outerHeight();

                if (Fabs.getViewPort().width < resBreakpointMd) {
                    height = Fabs.getViewPort().height - headerHeight - footerHeight;
                } else {
                    height = sidebar.height() + 20;
                }

                if ((height + headerHeight + footerHeight) <= Fabs.getViewPort().height) {
                    height = Fabs.getViewPort().height - headerHeight - footerHeight;
                }
            }
            content.attr('style', 'min-height:' + height + 'px');
        }
    };

    var handleSidebarMenuActiveLink = function(mode, el) {
        var menu = $('.page-sidebar-menu');


       /* angular.element(menu).find('ui > li > a.open').removeClass('open')
        angular.element(menu).find('a.acvive').removeClass('acvive')
        menu.find('li').each(function (){
            console.log($(this).html());
        })
        menu.find('ul > li > a > .open').removeClass('open');
        menu.find('li > a > .selected').remove();
        if (menu.hasClass('page-sidebar-menu-hover-submenu') === false) {
            menu.find('li.open').each(function(){
                if ($(this).children('.sub-menu').size() === 0) {
                    $(this).removeClass('open');
                    $(this).find('> a > .arrow.open').removeClass('open');
                }
            });
        } else {
            menu.find('li.open').removeClass('open');
        }*/
        /*el.parents('li').each(function () {
            $(this).addClass('active');
            $(this).find('> a > span.arrow').addClass('open');

            if ($(this).parent('ul.page-sidebar-menu').size() === 1) {
                $(this).find('> a').append('<span class="selected"></span>');
            }

            if ($(this).children('ul.sub-menu').size() === 1) {
                $(this).addClass('open');
            }
        });

        if (mode === 'click') {
            if (Fabs.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) {
                $('.page-header .responsive-toggler').click();
            }
        }*/

        /*

        if (mode === 'click' || mode === 'set') {
            el = $(el);
        } else if (mode === 'match') {
            menu.find("li > a").each(function() {
                var path = $(this).attr("href").toLowerCase();

                if (path.length > 1 && url.substr(1, path.length - 1) == path.substr(1)) {
                    el = $(this);
                    return;
                }
            });
        }

        if (!el || el.size() == 0) {
            return;
        }

        if (el.attr('href').toLowerCase() === 'javascript:;' || el.attr('href').toLowerCase() === '#') {
            return;
        }

        var slideSpeed = parseInt(menu.data("slide-speed"));
        var keepExpand = menu.data("keep-expanded");

        menu.find('li.active').removeClass('active');
        menu.find('li > a > .selected').remove();

        if (menu.hasClass('page-sidebar-menu-hover-submenu') === false) {
            menu.find('li.open').each(function(){
                if ($(this).children('.sub-menu').size() === 0) {
                    $(this).removeClass('open');
                    $(this).find('> a > .arrow.open').removeClass('open');
                }
            });
        } else {
            menu.find('li.open').removeClass('open');
        }

        el.parents('li').each(function () {
            $(this).addClass('active');
            $(this).find('> a > span.arrow').addClass('open');

            if ($(this).parent('ul.page-sidebar-menu').size() === 1) {
                $(this).find('> a').append('<span class="selected"></span>');
            }

            if ($(this).children('ul.sub-menu').size() === 1) {
                $(this).addClass('open');
            }
        });

        if (mode === 'click') {
            if (Fabs.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) {
                $('.page-header .responsive-toggler').click();
            }
        }*/
    };

    var handleSidebarMenu = function () {
        $('.page-sidebar-menu > u').on('click', 'li > a', function (e) {

            if ($('body').hasClass('page-sidebar-closed') &&  $(this).parent('li').parent('.page-sidebar-menu').size() === 1) {
                return;
            }

            var hasSubMenu = $(this).next().hasClass('sub-menu');

            if (Fabs.getViewPort().width >= resBreakpointMd && $(this).parents('.page-sidebar-menu-hover-submenu').size() === 1) { // exit of hover sidebar menu
                return;
            }

            if (hasSubMenu === false) {
                if (Fabs.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) {
                    $('.page-header .responsive-toggler').click();
                }
                return;
            }

            if ($(this).next().hasClass('sub-menu always-open')) {
                return;
            }

            var parent = $(this).parent().parent();
            var the = $(this);
            var menu = $('.page-sidebar-menu');
            var sub = $(this).next();

            var autoScroll = menu.data("auto-scroll");
            var slideSpeed = parseInt(menu.data("slide-speed"));
            var keepExpand = menu.data("keep-expanded");

            if (keepExpand !== true) {
                parent.children('li.open').children('a').children('.arrow').removeClass('open');
                parent.children('li.open').children('.sub-menu:not(.always-open)').slideUp(slideSpeed);
                parent.children('li.open').removeClass('open');
            }

            var slideOffeset = -200;

            if (sub.is(":visible")) {
                $('.arrow', $(this)).removeClass("open");
                $(this).parent().removeClass("open");
                sub.slideUp(slideSpeed, function () {
                    if (autoScroll === true && $('body').hasClass('page-sidebar-closed') === false) {
                        if ($('body').hasClass('page-sidebar-fixed')) {
                            menu.slimScroll({
                                'scrollTo': (the.position()).top
                            });
                        } else {
                            Fabs.scrollTo(the, slideOffeset);
                        }
                    }
                    handleSidebarAndContentHeight();
                });
            } else if (hasSubMenu) {
                $('.arrow', $(this)).addClass("open");
                $(this).parent().addClass("open");
                sub.slideDown(slideSpeed, function () {
                    if (autoScroll === true && $('body').hasClass('page-sidebar-closed') === false) {
                        if ($('body').hasClass('page-sidebar-fixed')) {
                            menu.slimScroll({
                                'scrollTo': (the.position()).top
                            });
                        } else {
                            Fabs.scrollTo(the, slideOffeset);
                        }
                    }
                    handleSidebarAndContentHeight();
                });
            }

            e.preventDefault();
        });

        $('.page-sidebar').on('click', ' li > a.ajaxify', function (e) {
            e.preventDefault();
            Fabs.scrollTop();

            var url = $(this).attr("href");
            var menuContainer = $('.page-sidebar ul');
            var pageContent = $('.page-content');
            var pageContentBody = $('.page-content .page-content-body');

            menuContainer.children('li.active').removeClass('active');
            menuContainer.children('arrow.open').removeClass('open');

            $(this).parents('li').each(function () {
                $(this).addClass('active');
                $(this).children('a > span.arrow').addClass('open');
            });
            $(this).parents('li').addClass('active');

            if (Fabs.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) {
                $('.page-header .responsive-toggler').click();
            }

            Fabs.startPageLoading();

            var the = $(this);

            $.ajax({
                type: "GET",
                cache: false,
                url: url,
                dataType: "html",
                success: function (res) {
                    if (the.parents('li.open').size() === 0) {
                        $('.page-sidebar-menu > li.open > a').click();
                    }

                    Fabs.stopPageLoading();
                    pageContentBody.html(res);
                    Layout.fixContentHeight();
                    Fabs.initAjax();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    Fabs.stopPageLoading();
                    pageContentBody.html('<h4>Could not load the requested content.</h4>');
                }
            });
        });

        $('.page-content').on('click', '.ajaxify', function (e) {
            e.preventDefault();
            Fabs.scrollTop();

            var url = $(this).attr("href");
            var pageContent = $('.page-content');
            var pageContentBody = $('.page-content .page-content-body');

            Fabs.startPageLoading();

            if (Fabs.getViewPort().width < resBreakpointMd && $('.page-sidebar').hasClass("in")) {
                $('.page-header .responsive-toggler').click();
            }

            $.ajax({
                type: "GET",
                cache: false,
                url: url,
                dataType: "html",
                success: function (res) {
                    Fabs.stopPageLoading();
                    pageContentBody.html(res);
                    Layout.fixContentHeight();
                    Fabs.initAjax();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    pageContentBody.html('<h4>Could not load the requested content.</h4>');
                    Fabs.stopPageLoading();
                }
            });
        });


        $(document).on('click', '.page-header-fixed-mobile .page-header .responsive-toggler', function(){
            Fabs.scrollTop();
        });


        handleFixedSidebarHoverEffect();


        $('.page-sidebar').on('click', '.sidebar-search .remove', function (e) {
            e.preventDefault();
            $('.sidebar-search').removeClass("open");
        });


        $('.page-sidebar .sidebar-search').on('keypress', 'input.form-control', function (e) {
            if (e.which == 13) {
                $('.sidebar-search').submit();
                return false;
            }
        });


        $('.sidebar-search .submit').on('click', function (e) {
            e.preventDefault();
            if ($('body').hasClass("page-sidebar-closed")) {
                if ($('.sidebar-search').hasClass('open') === false) {
                    if ($('.page-sidebar-fixed').size() === 1) {
                        $('.page-sidebar .sidebar-toggler').click();
                    }
                    $('.sidebar-search').addClass("open");
                } else {
                    $('.sidebar-search').submit();
                }
            } else {
                $('.sidebar-search').submit();
            }
        });


        if ($('.sidebar-search').size() !== 0) {
            $('.sidebar-search .input-group').on('click', function(e){
                e.stopPropagation();
            });

            $('body').on('click', function() {
                if ($('.sidebar-search').hasClass('open')) {
                    $('.sidebar-search').removeClass("open");
                }
            });
        }
    };

    var _calculateFixedSidebarViewportHeight = function () {
        var sidebarHeight = Fabs.getViewPort().height - $('.page-header').outerHeight();
        if ($('body').hasClass("page-footer-fixed")) {
            sidebarHeight = sidebarHeight - $('.page-footer').outerHeight();
        }

        return sidebarHeight;
    };

    var handleFixedSidebar = function () {
        var menu = $('.page-sidebar-menu');

        Fabs.destroySlimScroll(menu);

        if ($('.page-sidebar-fixed').size() === 0) {
            handleSidebarAndContentHeight();
            return;
        }

        if (Fabs.getViewPort().width >= resBreakpointMd) {
            menu.attr("data-height", _calculateFixedSidebarViewportHeight());
            Fabs.initSlimScroll(menu);
            handleSidebarAndContentHeight();
        }
    };

    var handleFixedSidebarHoverEffect = function () {
        var body = $('body');
        if (body.hasClass('page-sidebar-fixed')) {
            $('.page-sidebar').on('mouseenter', function () {
                if (body.hasClass('page-sidebar-closed')) {
                    $(this).find('.page-sidebar-menu').removeClass('page-sidebar-menu-closed');
                }
            }).on('mouseleave', function () {
                if (body.hasClass('page-sidebar-closed')) {
                    $(this).find('.page-sidebar-menu').addClass('page-sidebar-menu-closed');
                }
            });
        }
    };

    var handleSidebarToggler = function () {
        var body = $('body');
        if ($.cookie && $.cookie('sidebar_closed') === '1' && Fabs.getViewPort().width >= resBreakpointMd) {
            $('body').addClass('page-sidebar-closed');
            $('.page-sidebar-menu').addClass('page-sidebar-menu-closed');
        }


        $('body').on('click', '.sidebar-toggler', function (e) {
            var sidebar = $('.page-sidebar');
            var sidebarMenu = $('.page-sidebar-menu');
            $(".sidebar-search", sidebar).removeClass("open");

            if (body.hasClass("page-sidebar-closed")) {
                body.removeClass("page-sidebar-closed");
                sidebarMenu.removeClass("page-sidebar-menu-closed");
                if ($.cookie) {
                    $.cookie('sidebar_closed', '0');
                }
            } else {
                body.addClass("page-sidebar-closed");
                sidebarMenu.addClass("page-sidebar-menu-closed");
                if (body.hasClass("page-sidebar-fixed")) {
                    sidebarMenu.trigger("mouseleave");
                }
                if ($.cookie) {
                    $.cookie('sidebar_closed', '1');
                }
            }

            $(window).trigger('resize');
        });
    };

    var handleHorizontalMenu = function () {

        $('.page-header').on('click', '.hor-menu a[data-toggle="tab"]', function (e) {
            e.preventDefault();
            var nav = $(".hor-menu .nav");
            var active_link = nav.find('li.current');
            $('li.active', active_link).removeClass("active");
            $('.selected', active_link).remove();
            var new_link = $(this).parents('li').last();
            new_link.addClass("current");
            new_link.find("a:first").append('<span class="selected"></span>');
        });


        $('.page-header').on('click', '.search-form', function (e) {
            $(this).addClass("open");
            $(this).find('.form-control').focus();

            $('.page-header .search-form .form-control').on('blur', function (e) {
                $(this).closest('.search-form').removeClass("open");
                $(this).unbind("blur");
            });
        });


        $('.page-header').on('keypress', '.hor-menu .search-form .form-control', function (e) {
            if (e.which == 13) {
                $(this).closest('.search-form').submit();
                return false;
            }
        });


        $('.page-header').on('mousedown', '.search-form.open .submit', function (e) {
            e.preventDefault();
            e.stopPropagation();
            $(this).closest('.search-form').submit();
        });


        $('[data-hover="megamenu-dropdown"]').not('.hover-initialized').each(function() {
            $(this).dropdownHover();
            $(this).addClass('hover-initialized');
        });

        $(document).on('click', '.mega-menu-dropdown .dropdown-menu', function (e) {
            e.stopPropagation();
        });
    };

    var handleTabs = function () {
        // fix content height on tab click
        $('body').on('shown.bs.tab', 'a[data-toggle="tab"]', function () {
            handleSidebarAndContentHeight();
        });
    };

    var handleGoTop = function () {
        var offset = 300;
        var duration = 500;

        if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
            $(window).bind("touchend touchcancel touchleave", function(e){
                if ($(this).scrollTop() > offset) {
                    $('.scroll-to-top').fadeIn(duration);
                } else {
                    $('.scroll-to-top').fadeOut(duration);
                }
            });
        } else {
            $(window).scroll(function() {
                if ($(this).scrollTop() > offset) {
                    $('.scroll-to-top').fadeIn(duration);
                } else {
                    $('.scroll-to-top').fadeOut(duration);
                }
            });
        }

        $('.scroll-to-top').click(function(e) {
            e.preventDefault();
            $('html, body').animate({scrollTop: 0}, duration);
            return false;
        });
    };

    var handle100HeightContent = function () {

        var target = $('.full-height-content');
        var height;

        height = Fabs.getViewPort().height -
            $('.page-header').outerHeight(true) -
            $('.page-footer').outerHeight(true) -
            $('.page-title').outerHeight(true) -
            $('.page-bar').outerHeight(true);

        if (target.hasClass('portlet')) {
            var portletBody = target.find('.portlet-body');

            if (Fabs.getViewPort().width < resBreakpointMd) {
                Fabs.destroySlimScroll(portletBody.find('.full-height-content-body'));
                return;
            }

            height = height -
                target.find('.portlet-title').outerHeight(true) -
                parseInt(target.find('.portlet-body').css('padding-top')) -
                parseInt(target.find('.portlet-body').css('padding-bottom')) - 2;

            if (target.hasClass("full-height-content-scrollable")) {
                height = height - 35;
                portletBody.find('.full-height-content-body').css('height', height);
                Fabs.initSlimScroll(portletBody.find('.full-height-content-body'));
            } else {
                portletBody.css('min-height', height);
            }
        } else {
            if (Fabs.getViewPort().width < resBreakpointMd) {
                Fabs.destroySlimScroll(target.find('.full-height-content-body'));
                return;
            }

            if (target.hasClass("full-height-content-scrollable")) {
                height = height - 35;
                target.find('.full-height-content-body').css('height', height);
                Fabs.initSlimScroll(target.find('.full-height-content-body'));
            } else {
                target.css('min-height', height);
            }
        }
    };
    var handlerTable = function(){
        $("table tr").click(function() {
            //遍历所有的行，移除class:selected
            $.each($("table tr"), function(i, n) {
                $(n).removeClass("table-advance");
            });
            console.log("test");
            $(this).addClass("table-advance");
        });
    };


    return {

        initHeader: function() {
            handleHorizontalMenu();
        },

        setSidebarMenuActiveLink: function(mode, el) {
            handleSidebarMenuActiveLink(mode, el);
        },

        initSidebar: function() {
            //handleFixedSidebar();
            handleSidebarMenu();
            //handleSidebarToggler();

            //handleSidebarMenuActiveLink('match');

            Fabs.addResizeHandler(handleFixedSidebar);
        },

        initContent: function() {
            handle100HeightContent();
            handleTabs();
            handlerTable();

            Fabs.addResizeHandler(handleSidebarAndContentHeight);
            Fabs.addResizeHandler(handle100HeightContent);
        },

        initFooter: function() {
            handleGoTop();
        },

        init: function () {
            this.initHeader();
            this.initSidebar();
            this.initContent();
            this.initFooter();
        },

        fixContentHeight: function () {
            handleSidebarAndContentHeight();
        },

        initFixedSidebarHoverEffect: function() {
            handleFixedSidebarHoverEffect();
        },

        initFixedSidebar: function() {
            handleFixedSidebar();
        },

        getLayoutImgPath: function () {
            return Fabs.getAssetsPath() + layoutImgPath;
        },

        getLayoutCssPath: function () {
            return Fabs.getAssetsPath() + layoutCssPath;
        }
    };

}();
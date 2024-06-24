/* ===========================================================
 * bootstrap-modal.js v2.1
 * ===========================================================
 * Copyright 2012 Jordan Schroter
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */


!function ($) {

    "use strict"; // jshint ;_;

    /* MODAL CLASS DEFINITION
    * ====================== */

    var Modal = function (element, options) {
        this.init(element, options);
    };

    Modal.prototype = {

        constructor: Modal,

        init: function (element, options) {
            var that = this,
                manager;

            this.options = options;

            this.$element = $(element)
                .delegate('[data-dismiss="modal"]', 'click.dismiss.modal', $.proxy(this.hide, this));

            this.$element.data('modal', this);

            this.options.remote && this.$element.find('.modal-body').load(this.options.remote);

            manager = $('body').data('modalmanager');

            manager.appendModal(this);

            this.manager = manager;

            this.$element.on('focusin', function(e) {
                if (e.target != element) {
                    that.activeElement = e.target;
                }
            });

            this.$element.on('focusout', function(e) {
                if (e.relatedTarget) {
                    if (e.relatedTarget && that.manager.elzIndex(e.relatedTarget) < that.zIndex) {
                        that.restoreFocus();
                    }
                }
                else {
                    if (that.options.item_options && that.options.item_options.close_focusout) {
                        that.options.item._close_form(that.options.item_options.form_type);
                    }
                }
            });

            this.show();

            this.zIndex = this.manager.elzIndex(element);
        },

        restoreFocus: function () {
            var tabs,
                el = this.activeElement;
            if (el) {
                if (!this.elementIsActive(el)) {
                    this.focusNext(el);
                }
                else {
                    $(el).focus();
                }
            }
            else {
                tabs = this.tabList();
                if (tabs.length) {
                    $(tabs[0]).focus();
                }
                else {
                    this.$element.focus();
                }
            }
        },

        elementIsActive: function (el) {
            return !(el.disabled || el.hidden || el.readOnly || el.type === 'hidden' || el.offsetParent === null);
        },

        toggle: function () {
            return this[!this.isShown ? 'show' : 'hide']();
        },

        show: function () {
            var e = $.Event('show');

            if (this.isShown) return;

            if (this.options.item_options && this.options.item_options.transition) {
                this.$element.addClass('fade');
            }

            this.$element.trigger(e);

            if (e.isDefaultPrevented()) return;

            this.escape();

            this.options.loading && this.loading();

            this.tab();
        },

        hide: function (e) {
            e && e.preventDefault();

            e = $.Event('hide');

            this.$element.trigger(e);

            if (!this.isShown || e.isDefaultPrevented()) return (this.isShown = true);

            this.isShown = false;

            this.escape();

            this.tab();

            this.isLoading && this.loading();

            this.$element
                .removeClass('in')
                .removeClass('animated')
                .removeClass(this.options.attentionAnimation)
                .removeClass('modal-overflow')
                .attr('aria-hidden', true);

            $.support.transition && this.$element.hasClass('fade') ?
                this.hideWithTransition() :
                this.hideModal();
        },

        layout: function () {
            var that = this,
                prop = this.options.height ? 'height' : 'max-height',
                value = this.options.height || this.options.maxHeight,
                width;

            if (this.options.item_options && this.options.item_options.width) {
                width = this.options.item_options.width;
            }
            else if (this.options.width) {
                width = this.options.width;
            }
            else {
                width = this.$element.width();
            }

            if (width){
                if (width > $(window).width()) {
                    width = parseInt($(window).width() * 0.96);
                }
                this.$element.css('width', width);

                if (this.options.item_options && this.options.item_options.left !== undefined) {
                    this.$element.css('left', 0).css('margin-left', this.options.item_options.left);
                }
                else {
                    this.$element.css('margin-left', function () {
                        if (/%/ig.test(width)){
                            return -(parseInt(width) / 2) + '%';
                        } else {
                            return -($(this).width() / 2) + 'px';
                        }
                    });
                }
            } else {
                this.$element.css('width', '');
                this.$element.css('margin-left', '');
            }

            this.$element.find('.modal-body')
                .css('overflow', '')
                .css(prop, '');
            if (this.options.item_options && this.options.item_options.top !== undefined) {
                this.$element.css('top', 0).css('margin-top', this.options.item_options.top);
            }
            else {
                if (value){
                    this.$element.find('.modal-body')
                        .css('overflow', 'auto')
                        .css(prop, value);
                }

                var modalOverflow = $(window).height() - 10 < this.$element.height();
                if (modalOverflow || this.options.modalOverflow) {
                    this.$element
                        .css('margin-top', 0)
                        .addClass('modal-overflow');
                } else {
                    this.$element
                        .css('margin-top', 0 - this.$element.height() / 2)
                        .removeClass('modal-overflow');
                }
            }
        },

        getTabChildren: function(el, result) {
            var i,
                len,
                nodes;
            if (el.nodeType === 1) {
                if (el.tabIndex >= 0) {
                    result.push(el);
                }
                nodes = el.childNodes;
                if (nodes) {
                    len = nodes.length;
                    for (i = 0; i < len; i++) {
                        this.getTabChildren(nodes[i], result);
                    }
                }
            }
        },

        tabList: function() {
            var self = this,
                i,
                len,
                el,
                els0 = [],
                els1 = [],
                result = [];
            this.getTabChildren(this.$element.get(0), result);

            for (i = 0, len = result.length; i < len; i++) {
                el = result[i];
                if (this.elementIsActive(el)) {
                    if (el.tabIndex === 0) {
                        els0.push(el);
                    }
                    else {
                        els1.push(el);
                    }
                }
            }
            els1.sort(function(a, b) {
                return a.tabIndex - b.tabIndex;
            });
            result = els1.concat(els0);
            return result;
        },

        tab: function () {
            var key,
                that = this;
            if (this.isShown && this.options.consumeTab) {
                this.$element.on('keydown.tabindex.modal', function (e) {
                    var tabs,
                        curIndex;
                    key = e.which;
                    if (key === 9 ||
                        ((e.target.tagName !== 'TABLE') && !$(e.target).hasClass('dbtableinput') && (e.target.tagName !== 'TEXTAREA'))
                        && (key === 38 || key === 40)){
                        if (e.target === that.$element.get(0)) {
                            tabs = that.tabList();
                            if (tabs.length) {
                                $(tabs[0]).focus();
                            }
                        }
                        else if (e.target.tabIndex >= 0) {
                            tabs = that.tabList();
                            curIndex = tabs.indexOf(e.target);
                            if (curIndex !== -1) {
                                if ((!e.shiftKey && key === 9) || key === 40){
                                    curIndex++;
                                }
                                else {
                                    curIndex--;
                                }
                                if (curIndex < 0) {
                                    curIndex = tabs.length -1;
                                }
                                if (curIndex > tabs.length -1) {
                                    curIndex = 0;
                                }
                                $(tabs[curIndex]).focus();
                                e.preventDefault();
                                e.stopPropagation();
                            }
                        }
                    }
                })
            } else if (!this.isShown) {
                this.$element.off('keydown.tabindex.modal');
            }
        },

        escape: function () {
            var that = this;
            if (this.isShown && this.options.keyboard) {
                if (!this.$element.attr('tabindex')) this.$element.attr('tabindex', -1);

                this.$element.on('keyup.dismiss.modal', function (e) {
                    e.which == 27 && that.hide();
                });
            } else if (!this.isShown) {
                this.$element.off('keyup.dismiss.modal')
            }
        },

        hideWithTransition: function () {
            var that = this
                , timeout = setTimeout(function () {
                    that.$element.off($.support.transition.end);
                    that.hideModal();
                }, 500);

            this.$element.one($.support.transition.end, function () {
                clearTimeout(timeout);
                that.hideModal();
            });
        },

        hideModal: function () {
            var prop = this.options.height ? 'height' : 'max-height';
            var value = this.options.height || this.options.maxHeight;

            if (value){
                this.$element.find('.modal-body')
                    .css('overflow', '')
                    .css(prop, '');
            }

            this.$element
                .hide()
                .trigger('hidden');
        },

        removeLoading: function () {
            this.$loading.remove();
            this.$loading = null;
            this.isLoading = false;
        },

        loading: function (callback) {
            callback = callback || function () {};

            var animate = this.$element.hasClass('fade') ? 'fade' : '';

            if (!this.isLoading) {
                var doAnimate = $.support.transition && animate;

                this.$loading = $('<div class="loading-mask ' + animate + '">')
                    .append(this.options.spinner)
                    .appendTo(this.$element);

                if (doAnimate) this.$loading[0].offsetWidth; // force reflow

                this.$loading.addClass('in');

                this.isLoading = true;

                doAnimate ?
                    this.$loading.one($.support.transition.end, callback) :
                    callback();

            } else if (this.isLoading && this.$loading) {
                this.$loading.removeClass('in');

                var that = this;
                $.support.transition && this.$element.hasClass('fade')?
                    this.$loading.one($.support.transition.end, function () { that.removeLoading() }) :
                    that.removeLoading();

            } else if (callback) {
                callback(this.isLoading);
            }
        },

        focus: function () {
            var $focusElem = this.$element.find(this.options.focusOn);

            $focusElem = $focusElem.length ? $focusElem : this.$element;

            $focusElem.focus();
        },

        attention: function (){
            // NOTE: transitionEnd with keyframes causes odd behaviour

            if (this.options.attentionAnimation){
                this.$element
                    .removeClass('animated')
                    .removeClass(this.options.attentionAnimation);

                var that = this;

                setTimeout(function () {
                    if (that.$element) {
                        that.$element
                            .addClass('animated')
                            .addClass(that.options.attentionAnimation);
                    }
                }, 0);
            }
            this.focus();
        },


        destroy: function () {
            var e = $.Event('destroy');
            this.$element.trigger(e);
            if (e.isDefaultPrevented()) return;

            this.teardown();
        },

        teardown: function () {
            if (!this.$parent.length){
                this.$element.remove();
                this.$element = null;
                return;
            }

            if (this.$parent !== this.$element.parent()){
                this.$element.appendTo(this.$parent);
            }

            this.$element.off('.modal');
            this.$element.removeData('modal');
            this.$element
                .removeClass('in')
                .attr('aria-hidden', true);
        },

        focusNext: function(el) {
            var tabs = this.tabList(),
                i;
            if (!el) {
                el = document.activeElement;
            }
            i = tabs.indexOf(el);
            if (i !== -1) {
                i++;
                if (i > tabs.length -1) {
                    i = 0;
                }
                $(tabs[i]).focus();
            }
            else if (tabs.length) {
                $(tabs[0]).focus();
            }
        }
    };


    /* MODAL PLUGIN DEFINITION
    * ======================= */

    $.fn.modal = function (option, args) {
        return this.each(function () {
            var $this = $(this),
                data = $this.data('modal'),
                options = $.extend({}, $.fn.modal.defaults, $this.data(), typeof option == 'object' && option);

            if (!data) $this.data('modal', (data = new Modal(this, options)));
            if (typeof option == 'string') data[option]()
        })
    };

    $.fn.modal.defaults = {
        item_options: null,
        keyboard: true,
        backdrop: true,
        loading: false,
        width: null,
        height: null,
        maxHeight: null,
        modalOverflow: false,
        consumeTab: true,
        focusOn: null,
        replace: false,
        resize: true,
        attentionAnimation: 'shake',
        spinner: '<div class="loading-spinner" style="width: 200px; margin-left: -100px;"><div class="progress progress-striped active"><div class="bar" style="width: 100%;"></div></div></div>'
    };

    $.fn.modal.Constructor = Modal;


    /* MODAL DATA-API
    * ============== */

    $(function () {
        $(document).off('click.modal').on('click.modal.data-api', '[data-toggle="modal"]', function ( e ) {
            var $this = $(this),
                href = $this.attr('href'),
                $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))), //strip for ie7
                option = $target.data('modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data());

            e.preventDefault();
            $target
                .modal(option)
                .one('hide', function () {
                    $this.focus();
                })
        });
    });

}(window.jQuery);

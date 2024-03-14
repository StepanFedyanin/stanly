'use strict';

var inputCount = 2;
var sitekey = '6LfDtY4UAAAAANEBfbIswo6tCV7SjUyrSfci02aQ';

export function getOSName() {
    var OSName = "Unknown";

    if (navigator.appVersion.indexOf("Win")!=-1) OSName = "Windows";
    else if (navigator.appVersion.indexOf("Mac")!=-1) OSName = "MacOS";
    else if (navigator.appVersion.indexOf("X11")!=-1) OSName = "UNIX";
    else if (navigator.appVersion.indexOf("Linux")!=-1) OSName = "Linux";

    return OSName;
}

export function getNewLineType(OSName) {
    var newLine = '\n';
    if (OSName == "Windows") newLine = '\r\n';
    else if (OSName == "MacOS") newLine = '\n';
    else if (OSName == "UNIX") newLine = '\n';
    else if (OSName == "Linux") newLine = '\n';

    return newLine;
}

export function confirmEmptySubmit(classForm) {
    let $form = $('.' + classForm);
    let $zeroed = $form.find('.js-zeroed');
    // let $close = $form.find('.js-fancybox-close');
    let isConfirm = true;
    let $inputs = $form.find('input');
    let $modal = $('#confirm');

    $zeroed.click(function() {
        $.each($inputs, function() {
            let $this = $(this);

            if ($this.val() == '') {
                $this.val('0');
            }
        });

        $form.trigger('submit');
    });

    // $close.click(function() {
    //     $.fancybox.close();
    // });

    $.each($inputs, function() {
        let $this = $(this);

        if ($this.val() == '') {
            $.fancybox.open({
              src  : $modal,
              type : 'html',
              opts : {
                    buttons: [],
                    padding: 0,
                    smallBtn: false,
                    helpers:  {
                        overlay : {
                            css : {
                                'background-color' : 'rgba(0,0,0,.3)'
                            }
                        }
                    }
              },
            });
            isConfirm = false;
            return false;
        }
    });

    return isConfirm;
}

export function sendMailForm(classForm) {
    var $form = $('.' + classForm);
    let $formCover = $form.find('.js-form-cover');
    let $fieldset = $form.find('.js-fieldset');
    let isSended = false;
    let next_step = $form.find('[name="next_step"]').val();
    let calc_name = $form.find('[name="calc_name"]').val();
    let action = $form.find('[name="action"]').val();
    let url = $form.attr('action');
    let csrfmiddlewaretoken = $form.find('[name="csrfmiddlewaretoken"]').val();

    $form.length && $form.on('submit', function(e) {
        let email = $form.find('[name="email"]').val();

        if (!isSended) {
            isSended = true;
            $formCover.show();
            $fieldset.prop('disabled', 'disabled');

            $.ajax({
                url,
                data: {
                    calc_name,
                    email,
                    action
                },
                method: 'POST',
                dataType: 'html',
                headers: {
                    'X-CSRFToken': csrfmiddlewaretoken
                },
                success: function(res) {
                    if (res == 'OK') {
                        $form.html('<b>Сообщение успешно отправлено на почту ' + email +'!</b>');
                        if (next_step)
                            window.location.href = next_step;
                    }
                },
                error: function(res) {
                    if (res.responseText == 'email') {
                        alert('Введите корректный e-mail!');
                    } else {
                        alert('Ошибка! Попробуйте позже!');
                    }
                    isSended = false;
                    $formCover.hide();
                    $fieldset.prop('disabled', '');
                }
            });
        }

        return false;
    });
};

export function addInputWithValue(value, place) {
    let $place = $(place);
    value = value || '';
    let html = `<div class="step-page__scale">
                    <input type="text" class="step-page__scale-input input" name="scale-${inputCount}" placeholder="Введите название" value="${value}">
                    <button onclick="removeScale(this)" type="button" class="step-page__scale-remove">Удалить шкалу</button>
                </div>`;

    $place.append(html);
    inputCount++;
}

export function removeScale(button) {
    $(button).parent().remove();
}

export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export function getCaptcha(csrfmiddlewaretoken) {
    typeof grecaptcha !== 'undefined' && grecaptcha.ready(function() {
        grecaptcha.execute(
            sitekey,
            { action: 'statpsy' }
        )
        .then(function(token) {
            $.ajax({
                url: '/all/g_captcha/',
                data: {
                    'token': token
                },
                // headers: {
                //     'X-CSRFToken': csrfmiddlewaretoken
                // },
                method: 'POST'
            });
        });
    });
}

export function clearStorage() {
    let csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    delete sessionStorage[CALC_NAME];
    $.ajax({
        url: '/all/ajax/session_clear/',
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(res) {
            window.location.href = '';
        }
    });
}

export function getAjaxByUrl(url, success) {
    let csrftoken = getCookie('csrftoken');
    // console.log('getAjaxByUrl');
    $.ajax({
        type: 'GET',
        headers: {
            'X-CSRFToken': csrftoken
        },
        url,
        dataType: 'json',
        success: function (data) {
            // console.log('success');
            if (typeof data.html == 'undefined') {
                throw Error('no success data');
            } else {
                success(JSON.parse(data.html).html);
            }

        }
    });
}

// function open_payment_methods(inner, htmlForm) {
//     let $form = $(inner).closest('.js-robokassa-form');
//     $(htmlForm).fancybox({
//         "onClosed": function(){
//           // fancybox is closed, run myOtherFunct()
//        }
//     });
// }

export function getPaymentFormAjax(data) {
    let url = '/all/ajax/get_payment_form/';
    // let csrftoken = $this.parent().find('[name="csrfmiddlewaretoken"]').val();
    // let data = {
    //     calc_name,
    //     IncCurrLabel,
    //     price_type
    // };

    $fieldset.prop('disabled', 'disabled');
    isChanged = true;

    $.ajax({
        url,
        data,
        method: 'POST',
        dataType: 'html',
        headers: {
            // 'X-CSRFToken': csrftoken
        },
        success: function(res) {
            $.fancybox.open({
              src  : res,
              type : 'html',
              opts : {
                    buttons: [],
                    padding: 0,
                    smallBtn: false,
                    // btnTpl: {
                    //   close:
                    //     '<button data-fancybox-close class="popup-payment__close""></button>"'
                    // }
              }
            });
            $fieldset.prop('disabled', '');
            isChanged = false;
        },
        error: function(res) {
            // console.log(res);
            alert('Ошибка! Попробуйте позже!');
            $fieldset.prop('disabled', '');
            isChanged = false;
        },
    });

    return;
};


export function getPaymentMethodsAjax(e) {
    let $this = $(this);;
    let calc_name;
    let IncCurrLabel;
    let price_type;

    if (e && typeof e.data !== 'undefined'){
        calc_name = e.data.calc_name;
        IncCurrLabel = e.data.IncCurrLabel;
        price_type = e.data.price_type;
    } else {
        alert('Ошибка! Попробуйте позже!');
        return;
    }


    let url = '/all/ajax/get_payment_methods/';
    let isChanged = false;

    let $fieldset = $this.parent();

    if (!isChanged) {
        let csrftoken = $this.parent().find('[name="csrfmiddlewaretoken"]').val(); 
        let data = {
            calc_name,
            IncCurrLabel,
            price_type
        };

        $fieldset.prop('disabled', 'disabled');
        isChanged = true;

        $.ajax({
            url,
            data,
            method: 'POST',
            dataType: 'html',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                $.fancybox.open({
                  src  : res,
                  type : 'html',
                  opts : {
                        buttons: [],
                        padding: 0,
                        smallBtn: false,
                        // btnTpl: {
                        //   close:
                        //     '<button data-fancybox-close class="popup-payment__close""></button>"'
                        // }
                  }
                });
                $fieldset.prop('disabled', '');
                isChanged = false;
            },
            error: function(res) {
                // console.log(res);
                alert('Ошибка! Попробуйте позже!');
                $fieldset.prop('disabled', '');
                isChanged = false;
            },
        });
    }

    return;
};

export function changePaymentMethodsAjax(select) {
    let $this = $(select);
    let calc_name = $this.parent().find('[name=shpcalc_name]').val();
    let price_type = $this.parent().find('[name=shpprice_type]').val();
    let IncCurrLabel = $this.val();

    let url = '/all/get_payment_methods_ajax/';
    let isChanged = false;

    let $fieldset = $this.parent();

    if (!isChanged) {
        let csrftoken = $this.parent().find('[name="csrfmiddlewaretoken"]').val(); 
        let data = {
            calc_name,
            IncCurrLabel,
            price_type
        };

        $fieldset.prop('disabled', 'disabled');
        isChanged = true;

        $.ajax({
            url,
            data,
            method: 'POST',
            dataType: 'html',
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(res) {
                $.fancybox.destroy();
                $.fancybox.open(res);
                $fieldset.prop('disabled', '');
                isChanged = false;
            },
            error: function(res) {
                // console.log(res);
                alert('Ошибка! Попробуйте позже!');
                $fieldset.prop('disabled', '');
                isChanged = false;
            },
        });
    }

    return;
}


export function submitForm() {
    let formWrapperClass = '.js-robokassa-form';

    let $form = $(formWrapperClass).find('form');

    click_ya_payment_from_form($form);
    click_ga_payment();

    // console.log($form);
    $form.submit();
}

export function smoothAnchorSlide() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            let href = this.getAttribute('href');

            if (href !== '' && href !== '#')
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });

            return true;
        });
    });
}; 

export function openFancybox(html) {
    $.fancybox.destroy();
    $.fancybox.open({
      src  : html,
      type : 'html',
      opts : {
          buttons: [],
          padding: 0,
          smallBtn: false,
      }
    });
}

export function promoApply(button) {
    let $this = $(button);
    let $form = $this.closest('.js-robokassa-form');
    let isApply = true;
    $wrapper = $this.closest('.js-payment-place');
    let $fieldset = $wrapper.find('.js-fieldset');
    let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();

    $fieldset.prop('disabled', 'disabled');

    if (isApply){
        let promo     = $wrapper.find('[name="shppromo"]').val();
        let calc_name = $wrapper.find('[name="shpcalc_name"]').val();
        let url       = '/all/accounts/apply_promo/';

        $.ajax({
            url,
            data: {
                promo,
                calc_name,
            },
            method: 'POST',
            dataType: 'html',
            headers: {
                'X-CSRFToken': csrftoken
            },
            cache: false,
            success: function(res) {
                $wrapper.html(res);
                isApply = false;
            },
            error: function(res) {
                // console.log(res);
                if (res.responseText == 'NOT EXIST') {
                    alert('Ошибка! Промокод с таким названием не существует!');
                } else if (res.responseText == 'USED') {
                    alert('Ошибка! Промокод уже использован вами!');
                } else {
                    alert('Ошибка! Попробуйте позже!');
                }
                $fieldset.prop('disabled', '');
                isApply = false;
            }
        });
    }

    return false;
}


export function click_ya_payment_from_form($form) {
  if (typeof ym !== 'undefined') {
    let ym_params = {
    };

    if ($form && $form.find('input[name="shpfull_price"]').length) {
        ym_params['order_price'] = $form.find('input[name="shpfull_price"]').val();
    }

    ym(YM_ID, 'reachGoal', 'pay', ym_params);
  }
}

export function click_ga_payment() {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'robokassa_form', 'pay');
  }
}

export function paymentFilter(el) {
    let $this = $(el);
    let $filterItems = $('.js-filter-item');
    let $paymentList = $('.js-payment-list');
    let filter = $this.data('filter');
    let activeClass = 'is-active';
    let $target = $paymentList.find(`[data-filter-target=${filter}]`);

    $filterItems.removeClass(activeClass);
    $this.addClass(activeClass);

    if (filter !== 'all' && $target.length) {
        $paymentList.children().hide();
        $target.show();
    } else {
        $paymentList.children().show();
    }

}

export function selectPaymentMethod(el) {
    let $this = $(el);
    let $paymentMethods = $this.closest('.js-payment-methods');
    let calc_name = $paymentMethods.data('calc_name');
    let price_type = $paymentMethods.data('price_type');
    let IncCurrLabel = $this.data('value');
    let url = '/all/ajax/get_payment_form/';
    let csrftoken = $paymentMethods.find('[name="csrfmiddlewaretoken"]').val();
    let $hiddenFormPlace = $paymentMethods.find('.js-hidden-form-place');

    $.ajax({
        url,
        data: {
            calc_name,
            price_type,
            IncCurrLabel
        },
        method: 'POST',
        dataType: 'html',
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(res) {
            $hiddenFormPlace.html(res);
        },
        error: function(res) {
            alert('Ошибка! Попробуйте позже!');
        }
    });

}

export function showPassword() {
    let $showPassword = $('.js-show-password');

    $showPassword.length && $showPassword.click(function() {

        let $this = $(this);
        let $inputPassword = $this.prev();

        if ($inputPassword.attr("type") == "password") {

          $inputPassword.attr("type", "text");

        } else {

          $inputPassword.attr("type", "password");

        }

        return false;

    });
}

export function preloader() {
    let preloader = document.getElementById("preloader");
    if (preloader) {
        setTimeout(() => {
            preloader.style.display = "block";
        }, 400);
    } else {
        console.log('No preloader');
    }
};

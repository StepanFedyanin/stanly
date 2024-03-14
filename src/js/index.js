'use strict';

/* index.js */

import {
    getOSName,
    getNewLineType,
    confirmEmptySubmit,
    addInputWithValue,
    removeScale,
    getCookie,
    getCaptcha,
    clearStorage,
    smoothAnchorSlide,
    sendMailForm,
    openFancybox,
    getAjaxByUrl,
    getPaymentMethodsAjax,
    changePaymentMethodsAjax,
    submitForm,
    promoApply,
    click_ya_payment_from_form,
    click_ga_payment,
    paymentFilter,
    selectPaymentMethod,
    showPassword,
    preloader,

} from './utils';

window.STEP = $('body').data('step');
window.CALC_NAME = $('body').data('calc-name');

(function Main() {
     
  const indexjs = () => {

    // console.log('index.js working...');

    if( window && window.innerWidth > 600 ) {
    }

    main();

    if (STEP == 'index') {
      index();
    } else if (STEP == 'scales') {
      stepScales();
    } else if (STEP == 'set-groups') {
      stepGroups();
    } else if (STEP == 'prepare') {
      stepPrepare();
    } else if (STEP == 'short-result') {
      stepShort();
    } else if (STEP == 'full-result') {
      stepFull();
    } else if (STEP == 'profile') {
      profile();
    } else if (STEP == 'password') {
      password();
    } else if (STEP == 'login') {
      login();
    } else if (STEP == 'signup') {
      signup();
    }

    // stepDocx();

    ya();

  };

  document.addEventListener("DOMContentLoaded", indexjs);
  document.addEventListener('DOMContentLoaded', smoothAnchorSlide);

})();

function main() {
  let $signupButton = $('.js-signup');
  let $loginButton = $('.js-login');
  let $calcMenuParent = $('.js-menu-parent .calc-menu__link');
  let $robokassaForm = $('.js-robokassa-form').find('form');
  let $getPaymentMethodsButton = $('.js-get-payment-methods');
  let $achievementClose = $('.js-achievement-close');
  let $popupOpen = $('.js-popup-with-content');

  $signupButton.length && $signupButton.click(
    function(e) {
      getAjaxByUrl('/all/accounts/signup_ajax/', success);

      function success(html) {
        openFancybox(html);
        signup();
      }
    }
  );

  $loginButton.length && $loginButton.click(
    function(e) {
      getAjaxByUrl('/all/accounts/login_ajax/', success);

      function success(html) {
        openFancybox(html);
        login();
      }
    }
  );

  $calcMenuParent.length && $calcMenuParent.click(function(e) {
    let $this = $(this);
    let $targetEl = $this.parent();
    let $child = $targetEl.children('ul');
    let activeClass = 'is-active';

    $child.slideToggle();
    $targetEl.toggleClass(activeClass);
  });

  $achievementClose.length && $achievementClose.click(function(e) {
    let $this = $(this);
    let url = '/all/ajax/achievement_close/';
    // let csrfmiddlewaretoken = $this.parent().find('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        url,
        method: 'POST',
        dataType: 'html',
        headers: {
            // 'X-CSRFToken': csrfmiddlewaretoken
        },
        success: function(res) {
          $this.parent().slideToggle();
        },
        error: function(res) {
          alert('Ошибка! Попробуйте позже!');
        },
    });

  });

  $.each($getPaymentMethodsButton, function(i, item) {
    $(item).click(
      {
        'calc_name': $(item).data('calc-name'),
        'price_type': $(item).parent().find('[name=price_type]').val()
      },
      getPaymentMethodsAjax
    );
  });


  $popupOpen.length && $popupOpen.click(function(e) {
    let $this = $(this);
    let url = $this.data('url');
    let data = {
      calc_name: $this.data('calc-name'),
    };

    $.ajax({
        url,
        data,
        method: 'POST',
        dataType: 'html',
        success: function(res) {
            $.fancybox.open({
              src  : res,
              type : 'html',
              opts : {
                buttons: ['close'],
                padding: 0,
                smallBtn: false,
                btnTpl: {
                  close:
                    '<button data-fancybox-close class="popup__close""></button>"'
                }
              },
            });
        },
        error: function(res) {
            alert('Ошибка! Попробуйте позже!');
        },
    });
  });
}

function login() {
  let $form = $('.js-login-form');
  let $popup = $('.js-popup');
  let $reset = $('.js-password-reset');
  let $fieldset = $form.find('.js-fieldset');
  let $errors = $form.find('.js-error');
  let $inputs = $fieldset.find('input');
  let url = $form.attr('action');
  let data = {};
  let isSended = false;
  let csrfmiddlewaretoken = $form.find('[name="csrfmiddlewaretoken"]').val(); 
  let $redirect = $form.find('[name="next"]');
  let redirect_to = '';
  let $signupButton = $popup.find('.js-signup');

  if ($redirect.length) {
      redirect_to = $redirect.val();
  }

  $form.length && $form.submit(function(e) {
    if (!isSended) {

      $.each($inputs, function() {
          let $this = $(this);
          data[$this.attr('name')] = $this.val();
      });

      $errors.html('');
      $fieldset.prop('disabled', 'disabled');
      isSended = true;

      $.ajax({
          url,
          data: data,
          method: 'POST',
          dataType: 'json',
          headers: {
              'X-CSRFToken': csrfmiddlewaretoken
          },
          success: function(res) {
            $fieldset.prop('disabled', '');

            if ($.isEmptyObject(res["errors"])) {
                window.location.href = redirect_to;
            } else {
              let errors = res["errors"];
              for(let key in errors) {
                  $errors.append(`<p class="error">${errors[key]}</p>`);
              }
              isSended = false;
            }
          },
          error: function(res) {
            alert('Ошибка! Попробуйте позже!');
            $fieldset.prop('disabled', '');
            isSended = false;
          },
      });
    }

    return false;
  });

  $reset.length && $reset.click(function(e) {
    let $this = $(this);
    let url = $this.attr('href');

    $.ajax({
        url,
        method: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': csrfmiddlewaretoken
        },
        success: function(res) {
          let json = JSON.parse(res.html);
          openFancybox(json.html);
          resetPasswordAjax();
        },
        error: function(res) {
          alert('Ошибка! Попробуйте позже!');
        },
    });

    return false;
  });

  $signupButton.length && $signupButton.click(
    function(e) {
      getAjaxByUrl('/all/accounts/signup_ajax/', success);

      function success(html) {
        openFancybox(html);
        signup();
      }
    }
  );

  showPassword();
}

function resetPasswordAjax() {
  let $form = $('.js-reset-form');
  let $popup = $('.js-popup');
  let $fieldset = $form.find('.js-fieldset');
  let $errors = $form.find('.js-error');
  let $inputs = $fieldset.find('input');
  let url = $form.attr('action');
  let data = {};
  let isSended = false;
  let csrfmiddlewaretoken = $form.find('[name="csrfmiddlewaretoken"]').val(); 

  $form.length && $form.submit(function(e) {
    if (!isSended) {

      $.each($inputs, function() {
          let $this = $(this);
          data[$this.attr('name')] = $this.val();
      });

      $errors.html('');
      $fieldset.prop('disabled', 'disabled');
      isSended = true;

      $.ajax({
          url,
          data: data,
          method: 'POST',
          dataType: 'json',
          headers: {
              'X-CSRFToken': csrfmiddlewaretoken
          },
          success: function(res) {
            $fieldset.prop('disabled', '');

            if ($.isEmptyObject(res["errors"])) {
                let url = '/all/accounts/reset_password_done_ajax/';

                $.ajax({
                      url,
                      method: 'GET',
                      dataType: 'html',
                      headers: {
                          // 'X-CSRFToken': csrfmiddlewaretoken
                      },
                      success: function(res) {
                        $form.parent().parent().html(res);
                      },
                      error: function(res) {
                        alert('Ошибка! Попробуйте позже!');
                      },
                  });

                if ($.fancybox) {
                    // $.fancybox.destroy();
                }

            } else {
                let errors = res["errors"];

                for(let key in errors) {
                    $errors.append(`<p class="error">${errors[key]}</p>`);
                }
            }

            isSended = false;
            $fieldset.prop('disabled', '');
          },
          error: function(res) {
            alert('Ошибка! Попробуйте позже!');
            $fieldset.prop('disabled', '');
            isSended = false;
          },
      });
    }

    return false;
  });

  showPassword();
}

function index() {

}

function signup() {
  let $form = $('.js-signup-form');
  let $popup = $('.js-popup');
  let $fieldset = $form.find('.js-fieldset');
  let $errors = $form.find('.js-error');
  let $inputs = $fieldset.find('input');
  let url = $form.attr('action');
  let data = {};
  let isSended = false;
  let csrfmiddlewaretoken = $form.find('[name="csrfmiddlewaretoken"]').val();
  let $redirect = $form.find('[name="next"]');
  let redirect_to = '';
  let $loginButton = $popup.find('.js-login');

  if ($redirect.length) {
      redirect_to = $redirect.val();
  }

  $form.length && $form.submit(function(e) {
    if (!isSended) {
        let email;

        $.each($inputs, function() {
            let $this = $(this);
            data[$this.attr('name')] = $this.val();

            if ($this.attr('name') == 'email')
              email = $this.val();
        });

        $errors.html('');
        $fieldset.prop('disabled', 'disabled');
        isSended = true;
        $.ajax({
            url,
            data,
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken
            },
            success: function(res) {
                $fieldset.prop('disabled', '');

                if ($.isEmptyObject(res["errors"])) {
                    let url = '/all/accounts/verification_sent_ajax/';

                    $.ajax({
                          url,
                          data: {
                            'email': email
                          },
                          method: 'GET',
                          dataType: 'html',
                          headers: {
                              // 'X-CSRFToken': csrfmiddlewaretoken
                          },
                          success: function(res) {
                            $form.parent().parent().html(res);
                          },
                          error: function(res) {
                            alert('Ошибка! Попробуйте позже!');
                          },
                      });
                } else {
                    let errors = res["errors"];
                    for(let key in errors) {
                        $errors.append(`<p class="error">${errors[key]}</p>`);
                    }
                    isSended = false;
                }
            },
            error: function(res) {
                alert('Ошибка! Попробуйте позже!');
                $fieldset.prop('disabled', '');
                isSended = false;
            },
        });
    }

    return false;
  });

  $loginButton.length && $loginButton.click(
    function(e) {
      getAjaxByUrl('/all/accounts/login_ajax/', success);

      function success(html) {
        openFancybox(html);
        login();
      }
    }
  );

  showPassword();

}

function stepDocx() {
  let $form = $('.js-form');
  sendMailForm('js-form');
}

function stepShort() {
  let $form = $('.js-form-send-promo');
  let $fieldset = $form.find('.js-fieldset');

  if ($form.length) {
    let $letters = $fieldset.find('input');

    $letters.on('paste', function(e) {
      let text = e.originalEvent.clipboardData.getData('text/plain');

      for (let i=0; i < text.length; i++) {
        $letters[i] && $($letters[i]).val(text[i]);
      }

      return false;
    });

    $letters.on('keyup', function(e) {
      if (!e.ctrlKey) {
        let $this = $(this);
        let letter = e.originalEvent.key;
        let tabindex = parseInt($this.attr('tabindex'));

        if (e.which <= 90 && e.which >= 48) {
          $this.val(letter);

          if (tabindex < 9) {
            $(`input[tabindex=${tabindex + 1}]`).focus();
          }

        } else if (e.which == 8) {
          if (tabindex > 1) {
            $(`input[tabindex=${tabindex - 1}]`).focus();
          }
        }
        return false;
      }
    });

    let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();
    let url = $form.attr('action');
    let isSended = false;

    $form.submit(function(e) {
      if (!isSended) {
        let promo = '';

        $.each($fieldset.find('input'), function(i, item) {
          promo += $(item).val();
        });

        if (promo.length == 8) {
          isSended = true;
          $fieldset.prop('disabled', 'disabled');

          $.ajax({
              url,
              data: {
                promo
              },
              method: 'POST',
              dataType: 'html',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(res) {
                  if (res == 'OK') {
                      // window.location.href = next_step;
                  } else {
                      isSended = false;
                      $fieldset.prop('disabled', '');
                  }
              },
              error: function(res) {
                  if (res.responseText == 'NOT EXIST') {
                      alert('Промокод не существует!');
                  } else if (res.responseText == 'USED') {
                      alert('Промокод уже использован!');
                  } else {
                      alert('Ошибка! Попробуйте позже!');
                  }
                  $fieldset.prop('disabled', '');
                  isSended = false;
              }
          });
        } else {
          alert('Введите корректный промокод!');
        }
      }

      return false;
    });
  }
}

function stepFull() {
}

function stepGroups() {
    let group_number = $('[name="group_number"]').val();
    let step = $('[name="step"]').val();
    // let calc_name = $('[name="calc_name"]').val();

    let $form = $('.js-form-group');
    let $groupData = $('.js-group-data');
    let classError = 'error';
    let $groupName = $('#group_name');
    let $groupCount = $('#group_count');
    let $hideOnClick = $('.js-hide-on-click');
    let isShowGroup = false;
    let isSended = false;
    let csrftoken = $('[name="csrfmiddlewaretoken"]').val();

    var STORAGE = JSON.parse(sessionStorage[CALC_NAME]);

    if (STORAGE['group_name_' + group_number]
        && STORAGE['group_count_' + group_number]
        && STORAGE['group_data_' + group_number]) {
        isShowGroup = true;
    }

    if (STORAGE['group_name_' + group_number])
        $groupName.val(STORAGE['group_name_' + group_number]);

    if (STORAGE['group_count_' + group_number])
        $groupCount.val(STORAGE['group_count_' + group_number]);

    $form.length && $form.submit(function(e) {
        let $this = $(this);
        let isValidForm = true;

        $('.' + classError).removeClass(classError);

        if (!$groupName.val()) {
            $groupName.addClass(classError);
            $groupName.prev().addClass(classError);
            isValidForm = false;
        }

        if ( !$groupCount.val() || !parseInt($groupCount.val()) ) {
            $groupCount.addClass(classError);
            $groupCount.prev().addClass(classError);
            isValidForm = false;
        }

        if (isValidForm && !isSended) {
            let url = $this.attr('action');
            let data = {};

            isSended = true;

            STORAGE['group_name_' + group_number] = data['group_name'] = $groupName.val();
            STORAGE['group_count_' + group_number] = data['group_count'] = parseInt($groupCount.val());

            data['step'] = step;
            data['group_number'] = group_number;
            data['calc_name'] = CALC_NAME;
            sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);

            $.ajax({
                url,
                data,
                method: 'POST',
                dataType: 'html',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function(res) {
                    $groupData.html(res);
                    $hideOnClick.hide();
                    $groupData.on('paste', 'input', pasteFromBufferToTable);
                    isSended = false;
                    getGroupInputs();
                    addTableHScroll();
                },
                error: function(res) {
                    if (res.responseText == 'count') {
                      let anotherGroupName = group_number == 1 ? STORAGE['group_name_2'] : STORAGE['group_name_1'];
                      let anotherGroupCount = group_number == 1 ? STORAGE['group_count_2'] : STORAGE['group_count_1'];
                      alert('В группе ' + anotherGroupName + ' ' + anotherGroupCount +' человек, ' + 
                      'поэтому в текущей группе должно быть тоже ' + anotherGroupCount + ' человек. ' +
                      'Группы должны быть равны по количеству участников.');
                    } else if (res.responseText == 'NO_SCALES') {
                      alert('Нет шкал для заполнения! Сначала заполните шкалы на предыдущем шаге');
                    }
                    isSended = false;
                }
            });
        } else {
            console.log('Invalid info.');
        }

        e.preventDefault();
        e.stopPropagation();
    });

    if (isShowGroup)
        $form.trigger('submit');

    function pasteFromBufferToTable(e) {
        var $this = $(this);

        $.each(e.originalEvent.clipboardData.items, function(i, v) {
            if (v.type === 'text/plain'){
                v.getAsString(function(text){
                    var newLine = getNewLineType(getOSName());
                    var spaces = new RegExp('[(\s*)]');
                    var corr = 0;
                    var x = $this.closest('td').index() - 1, // - th
                        y = $this.closest('tr').index();
                    text = text.trim(newLine);

                    $.each(text.split(new RegExp('[' + newLine + ']')), function(i2, v2) {
                        if (v2 == '') {
                            corr++;
                            return true;
                        }

                        $.each(v2.split('\t'), function(i3, v3) {
                            v3 = v3.trim(' ');
                            var row = y+i2, col = x+i3;
                            var $targetInput = $this.closest('tbody').find('tr:eq('+(row-corr)+') td:eq('+col+') input');
                            $targetInput.length && $targetInput.val(v3);
                        });
                    });
                });
            }
        });
        return false;
    }
}

function stepPrepare() {
  var STORAGE = JSON.parse(sessionStorage[CALC_NAME]);

  let $form = $('.js-form');
  let next_step = $('[name="next_step"]').val();
  let calc_name = $('[name="calc_name"]').val();
  let group_count = $('[name="group_count"]').val();

  let $fieldset = $('.js-fieldset');
  let url = $form.attr('action');
  let csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
  let $json = $('[name="json"]');
  let isSended = false;
  let data = {};

  for (let i = 1; i <= group_count; i++) {
      data['group_name_' + i] = STORAGE['group_name_' + i];
      data['group_count_' + i] = STORAGE['group_count_' + i];
      data['group_data_' + i] = STORAGE['group_data_' + i];
  }

  data['group_quantity'] = STORAGE['group_quantity'];

  render();

  data = JSON.stringify(data);
  $json.val(data);

  function render() {
      let groups = {};

      let $table = $('.js-table');
      let $change = $('.js-group-change-link');

      for (let i = 1; i <= group_count; i++) {
          try {
              groups['group_data_' + i] = STORAGE['group_data_' + i];
          } catch (ex) {
              console.error(ex);
          }

          if (Object.keys(groups['group_data_' + i]).length) {
              addBody(STORAGE['group_count_' + i], groups['group_data_' + i], STORAGE['group_name_' + i], i);
          } else {
              console.error('no data');
          }
      }

      $.each($change, function(i, elem) {
          let $this = $(this);
          let $name = $this.find('.js-group-name');
          let $count = $this.find('.js-group-count');

          if (STORAGE['group_name_' + (i + 1)])
              $name.text(STORAGE['group_name_' + (i + 1)]);

          if (STORAGE['group_count_' + (i + 1)])
              $count.text(STORAGE['group_count_' + (i + 1)]);

          $this.attr('href', `/all/${calc_name}/steps/${i + 2}/`);
      });

      
      function addBody(count, group_data, group_name, group_number) {
          let template = '';
          for (let i = 0; i < count; i ++) {
              template += `<tr class="table__tbody-tr table__group-row--${group_number}">`;
              template += `<th class="table__tbody-th" scope="row">Группа "${group_name}" / Испытуемый ${(i + 1)}</th>`;
              for (let scale in group_data) {
                  template += `<td class="table__tbody-td">${group_data[scale][i+1]}</span></td>`;
              }
              template += '</tr>';
          }
          $($table.find('tbody')).append(template);
      }
  }

  $form.length && $form.submit(function() {
      if (!isSended) {

          isSended = true;
          $fieldset.prop('disabled', 'disabled');

          $.ajax({
              url,
              data: {
                  calc_name,
                  json: $json.val()
              },
              method: 'POST',
              dataType: 'html',
              headers: {
                  'X-CSRFToken': csrfmiddlewaretoken
              },
              success: function(res) {
                  if (res == 'OK') {
                      preloader();
                      window.location.href = next_step;
                  } else {
                      isSended = false;
                      $fieldset.prop('disabled', '');
                  }
              },
              error: function(res) {
                  isSended = false;
                  alert('Ошибка! Попробуйте позже!');
                  $fieldset.prop('disabled', '');
              }
          });
      }

      return false;
  });
}

function stepScales() {
  let $newScaleInput = $('.js-add-new-input');
  let newInputPlace = '.js-scale-group';
  let $inputPlace = $('.js-scale-group');
  let $formScales = $('.js-form-scales');
  let $formUpload = $('.js-form-upload');
  let $group_quantity = $('[name="group_quantity"]');
  let $quantity = $('.js-quantity');
  let $errorQuantity = $('.js-quantity-error');
  let classError = 'error';
  let scales = [];
  let next_step = $('[name="next_step"]').val();
  let isSended = false;
  let $clearSotarage = $('.js-clear-storage');

  if (typeof sessionStorage[CALC_NAME] == 'undefined') {
    sessionStorage[CALC_NAME] = '{}';
  }

  if (sessionStorage[CALC_NAME] == '{}') {
    $clearSotarage.hide();
  }

  var STORAGE = JSON.parse(sessionStorage[CALC_NAME]);

  if (STORAGE['scales']) {
      scales = STORAGE['scales'];
  }

  if (STORAGE['group_quantity']) {
      $group_quantity.val(STORAGE['group_quantity']);
  }

  if (scales.length) {
      $inputPlace.html('');
      for (let input in scales) {
          addInputWithValue(scales[input], newInputPlace);
      }
  }

  $newScaleInput.click(function() {
      addInputWithValue(false, newInputPlace);
  });

  $formScales.length && $formScales.submit(function(e) {
      let $this = $(this);
      let csrftoken = $this.find('[name="csrfmiddlewaretoken"]').val();
      let $fieldset = $this.find('.js-fieldset');
      let url = $this.attr('action');
      let group_quantity;
      let data = {};
      let newScales = [];

      if (!isSended) {
          let $inputs = $('.js-scale-group').find('input');
          let $error = $('.js-scale-error');

          isSended = true;
          $error.removeClass(classError);

          $errorQuantity.length && $errorQuantity.removeClass(classError);
          $fieldset.prop('disabled', 'disabled');

          $.each($inputs, function(i) {
              let $this = $(this);
              newScales.push($this.val());
              data[i] = $this.val();
          });

          data['calc_name'] = CALC_NAME;

          if ($('[name="group_quantity"]').length) {
              data['group_quantity'] = parseInt($('[name="group_quantity"]').val());
              STORAGE['group_quantity'] = data['group_quantity'];
          }

          $.ajax({
              url,
              data,
              method: 'POST',
              dataType: 'html',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(res) {
                  if (res == 'OK') {
                      STORAGE['scales'] = newScales;
                      sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
                      window.location.href = next_step;
                  }
              },
              error: function(res) {
                  if (res.responseText == 'ERROR') {
                      $error.addClass(classError);
                  } else if (res.responseText == 'QUANTITY'){
                      $errorQuantity.addClass(classError);
                  } else {
                      alert('Ошибка! Попробуйте позже!');
                  }

                  isSended = false;
                  $fieldset.prop('disabled', '');
              }
          });
      }

      return false;
  });

  $inputPlace.on('paste', 'input', function(e) {
      let $this = $(this);
      let scaleInput = '.js-scale-input';

      $.each(e.originalEvent.clipboardData.items, function(i, val) {
          if (val.type === 'text/plain'){
              val.getAsString(function(text){
                  let newLine = getNewLineType(getOSName());
                  let y = $this.closest(scaleInput).index();
                  let corr = 0;
                  text = text.trim(newLine);
                  let values = text.split(new RegExp('[' + newLine + '|\t]'));
                  
                  $.each(values, function(i_row, val_row) {
                      if (val_row == '') {
                          corr++;
                          return true;
                      }
                      val_row = val_row.trim(' ');
                      let index = y + i_row - corr;
                      let $targetInput = $inputPlace.find(`${scaleInput}:eq(${index}) input`);
                      if (!$targetInput.length) {
                          addInputWithValue(val_row, newInputPlace);
                      } else {
                          $targetInput.val(val_row);
                      }
                  });
              });
          }
      });

      return false;
  });

  $formUpload.length && $formUpload.submit(function(e) {
      let $this = $(this);

      if (!isSended) {
          let csrftoken = $this.find('[name="csrfmiddlewaretoken"]').val();
          let $error = $this.find('.js-scale-error');
          let $fieldset = $this.find('.js-fieldset');
          let url = $this.attr('action');
          // let file = document.getElementById('file').files[0];
          let data = new FormData($this[0]);

          isSended = true;
          $error.removeClass(classError);
          $fieldset.prop('disabled', 'disabled');

          $.ajax({
              url,
              data,
              cache: false,
              contentType: false,
              processData: false,
              enctype: 'multipart/form-data',
              method: 'POST',
              dataType: 'json',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(res) {
                  STORAGE['scales'] = res;
                  sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
                  window.location.href = '';
              },
              error: function(res) {
                  isSended = false;
                  alert('Ошибка! Попробуйте позже!');
                  $fieldset.prop('disabled', '');
              }
          });
      }

      return false;
  });

  $clearSotarage && $clearSotarage.click(function() {
      clearStorage();
  });
}

function getGroupInputs() {
  let $form = $('.js-form-values');
  let group_number = $form.find('[name="group_number"]').val();
  let group_name = $form.find('[name="group_name"]').val();
  let group_count = $form.find('[name="group_count"]').val();
  let $inputs = $form.find('tbody input');
  let next_step = $('[name="next_step"]').val();
  let isSended = false;
  let classError = 'error';
  let $formUpload = $('.js-form-upload');

  var STORAGE = JSON.parse(sessionStorage[CALC_NAME]);

  if (typeof STORAGE['group_data_' + group_number] !== 'undefined') {
      let group_data = STORAGE['group_data_' + group_number];

      $.each($inputs, function() {
          let $this = $(this);
          if (
              typeof group_data[$this.data('scale')] !== 'undefined' &&
              typeof group_data[$this.data('scale')][$this.data('person')] !== 'undefined'
          )
          $this.val(group_data[$this.data('scale')][$this.data('person')]);
      });
  }

  $form.length && $form.submit(function(e) {
      let isConfirm = confirmEmptySubmit('js-form-values');

      if (isConfirm && !isSended) {
          let $this = $(this);
          let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();
          let values = {};
          let $fieldset = $this.find('.js-fieldset');
          let url = $this.attr('action');

          $.each($inputs, function() {
              let $this = $(this);

              if (!values[$this.data('scale')]) {
                  values[$this.data('scale')] = {};
              }

              let prepare_value = parseFloat($this.val().replace(/,/, '.'));
              values[$this.data('scale')][$this.data('person')] = prepare_value;

              if (isNaN(values[$this.data('scale')][$this.data('person')])) {
                  values[$this.data('scale')][$this.data('person')] = 0;
              }
          });

          isSended = true;
          $fieldset.prop('disabled', 'disabled');

          $.ajax({
              url,
              data: {
                  'group_data': JSON.stringify(values),
                  group_count,
                  group_name,
                  group_number,
                  calc_name: CALC_NAME
              },
              method: 'POST',
              dataType: 'html',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(res) {
                  if (res == 'OK') {
                      STORAGE['group_data_' + group_number] = values;
                      sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
                      window.preloader();
                      window.location.href = next_step;
                  } else {
                      isSended = false;
                      $fieldset.prop('disabled', '');
                  }
              },
              error: function(res) {
                  let error = JSON.parse(res.responseText);
                  if (error['DATA_ERROR']) {
                      alert(`Стандартное отклонение шкалы ${error['DATA_ERROR']} равно 0 - вычисление не возможно. Для того, чтобы была возможность произвести вычисления нужно, чтобы значения шкалы ${error['DATA_ERROR']} отличались друг от друга`);
                  } else {
                      alert('Ошибка! Попробуйте позже!');
                  }

                  isSended = false;
                  $fieldset.prop('disabled', '');
              }
          });
      }

      return false;
  });

  $formUpload.length && $formUpload.submit(function(e) {
      let $this = $(this);

      if (!isSended) {
          let csrftoken = $this.find('[name="csrfmiddlewaretoken"]').val();
          let $error = $this.find('.js-scale-error');
          let $fieldset = $this.find('.js-fieldset');
          let url = $this.attr('action');
          // let file = document.getElementById('file').files[0];
          let data = new FormData($this[0]);

          // isSended = true;
          $error.removeClass(classError);
          // $fieldset.prop('disabled', 'disabled');

          $.ajax({
              url,
              data: data,
              cache: false,
              contentType: false,
              processData: false,
              enctype: 'multipart/form-data',
              method: 'POST',
              dataType: 'json',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              success: function(res) {
                  STORAGE['group_data_' + group_number] = res;
                  sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
                  window.location.href = '';
              },
              error: function(res) {
                  isSended = false;
                  alert('Ошибка! Попробуйте позже!');
                  $fieldset.prop('disabled', '');
              }
          });
      }

      return false;
  });
}

function ya() {
  if(typeof ym !== 'undefined') {
    let ym_params = {
    };

    $(document).on('submit', '.js-ym-registration', function(e) {
      ym(YM_ID, 'reachGoal', 'registration', ym_params);
    });

    $(document).on('submit', '.js-ym-autorization', function(e) {
      ym(YM_ID, 'reachGoal', 'autorization', ym_params);
    });

    $(document).on('submit', '.js-ym-pay', function(e) {
      if ($('input[name="OutSum"]').length) {
        ym_params['order_price'] = $('input[name="OutSum"]').val();
      }

      ym(YM_ID, 'reachGoal', 'pay', ym_params);
    });
  }

  if (typeof ga !== 'undefined') {
    $(document).on('submit', '.js-ym-registration', function(e) {
      ga('send', 'event', 'account', 'registration');
    });

    $(document).on('submit', '.js-ym-autorization', function(e) {
      ga('send', 'event', 'account', 'autorization');
    });

    $(document).on('submit', '.js-ym-pay', function(e) {
      ga('send', 'event', 'robokassa_form', 'pay');
    });
  }
}

function profile() {
  let $form = $('.js-form-create-promo');
  let $promoDelete = $('.js-delete-promo');

  let $addEmailShow = $('.js-show-add-email');
  let $addEmailForm = $('.js-add-email-form');

  let isSended = false;
  let classError = 'error';

  $form.length && $form.submit(function(e) {
    if (!isSended) {
        let $this = $(this);
        let $fieldset = $this.find('.js-fieldset');
        let $error = $this.find('.js-promo-error');
        let csrftoken = $this.find('[name="csrfmiddlewaretoken"]').val();
        let url = $this.attr('action');
        let $promoLetters = $('.js-promo-letters');
        let promo = '';

        $.each($promoLetters.find('input'), function(i, item) {
          promo += $(item).val();
        });

        console.log(promo);

        isSended = true;
        $fieldset.prop('disabled', 'disabled');
        $error.removeClass(classError);

        $.ajax({
            url,
            data: {
              promo
            },
            method: 'POST',
            dataType: 'html',
            headers: {
                'X-CSRFToken': csrftoken
            },
            cache: false,
            success: function(res) {
                console.log(res);
                window.location.href = '';
                // if (res == 'OK') {
                // } else {
                //     isSended = false;
                //     $fieldset.prop('disabled', '');
                // }
            },
            error: function(res) {
                console.log(res);
                if (res.responseText == 'EXIST') {
                    alert('Ошибка! Промокод с таким названием уже существует!');
                } else {
                    $error.addClass(classError);
                }
                isSended = false;
                $fieldset.prop('disabled', '');

                // alert('Ошибка! Попробуйте позже!');
            }
        });
    }

    return false;
  });

  if ($form.length) {
    let $letters = $form.find('input');

    $letters.on('keyup', function(e) {
      let $this = $(this);
      let letter = e.originalEvent.key;
      let tabindex = parseInt($this.attr('tabindex'));

      if (e.which <= 90 && e.which >= 48) {
        $this.val(letter);

        if (tabindex < 9) {
          $(`input[tabindex=${tabindex + 1}]`).focus();
        }

      } else if (e.which == 8) {
        if (tabindex > 1) {
          $(`input[tabindex=${tabindex - 1}]`).focus();
        }
      }
    });

    $form.submit(function(e) {
      return false;
    });
  }

  $promoDelete.length && $promoDelete.click(function(e) {
      if (confirm('Вы действительно хотите удалить промокод?')){
          let $this = $(this);
          let csrftoken = $('[name="csrfmiddlewaretoken"]').val();
          let promo = $this.data('promo');
          let url = '/all/accounts/delete_promo/';

          $.ajax({
              url,
              data: {
                  promo
              },
              method: 'POST',
              dataType: 'html',
              headers: {
                  'X-CSRFToken': csrftoken
              },
              cache: false,
              success: function(res) {
                  if ($this.closest('tr').remove())
                      alert('Промокод удалён');
              },
              error: function(res) {
                  if (res.responseText == 'NOT EXIST') {
                      alert('Ошибка! Промокод с таким названием не существует!');
                  } else {
                      alert('Ошибка! Попробуйте позже!');
                  }
              }
          });
      }

      return false;
  });

  $addEmailShow.length && $addEmailForm.length && $addEmailShow.click(function(e) {

    if ($addEmailForm.css('display') === 'none') {
      $addEmailForm.slideToggle();
    }

  });
}

function password() {
  let $form = $('.js-form-password-reset');

  let isSended = false;
  let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();
  let $fieldset = $form.find('.js-fieldset');
  let classError = 'error';
  let $error = $form.find('.js-error');

  $form.length && $form.submit(function(e) {
    if (!isSended) {
        let $this_form = $(this);
        let url = $this_form.attr('action');
        let $password1 = $this_form.find('input[name="password1"]');
        let $password2 = $this_form.find('input[name="password2"]');
        let data = {
          'password1': $password1.val(),
          'password2': $password2.val()
        };

        isSended = true;
        $fieldset.prop('disabled', 'disabled');
        $error.removeClass(classError);
        $this_form.find('input').removeClass(classError);
        $error.html('');

        $.ajax({
            url,
            data,
            method: 'POST',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            cache: false,
            success: function(res) {
              $this_form.html('<p>Пароль успешно изменён!</p>');
              // if (res.location) {
              //   window.location.href = res.location;
              // } else {
              //   window.location.href = '/all/';
              // }
            },
            error: function(res) {
              for (let input in res.responseJSON.form.fields) {
                let $input = $this_form.find(`input[name="${input}"]`);
                let field = res.responseJSON.form.fields[input];
                let errors = '';

                for (let i in field.errors) {
                   errors += field.errors[i] + "<br>";
                }

                if (errors.length) {
                  $input.addClass(classError);
                  $input.next().html(errors);
                }
              }

              $error.addClass(classError);
              isSended = false;
              $fieldset.prop('disabled', '');
            }
        });
    }

    return false;
  });

  showPassword();
}

function addTableHScroll() {
  let $table = $('.js-table');
  let $tableWrapper = $table.parent();
  let $tableCopy = $('.js-table-copy');
  let classActive = 'active';

  $('.js-thead-copy').innerHeight($table.find('.table__thead-th').innerHeight());
  $('.js-tcell-copy').innerHeight($table.find('.table__tbody-th').innerHeight() - 2); // border

  $tableWrapper.scroll(function(e) {
    if ($tableWrapper.scrollLeft() > 10) {
      $tableCopy.addClass(classActive);
    } else {
      $tableCopy.removeClass(classActive);
    }
  });
}

window.YM_ID = '57165547';
window.ya = ya;
window.removeScale = removeScale;
window.submitForm = submitForm;
window.promoApply = promoApply;
window.getPaymentMethodsAjax = getPaymentMethodsAjax;
window.changePaymentMethodsAjax = changePaymentMethodsAjax;
window.click_ya_payment_from_form = click_ya_payment_from_form;
window.click_ga_payment = click_ga_payment;
window.paymentFilter = paymentFilter;
window.selectPaymentMethod = selectPaymentMethod;
window.showPassword = showPassword;
window.preloader = preloader;

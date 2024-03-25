/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/extract-svg-sprite-webpack-plugin/lib/css-loader.js!./node_modules/sass-loader/dist/cjs.js?!./src/css/style.scss":
/*!********************************************************************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/extract-svg-sprite-webpack-plugin/lib/css-loader.js!./node_modules/sass-loader/dist/cjs.js??ref--7-4!./src/css/style.scss ***!
  \********************************************************************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./node_modules/style-loader/lib/addStyles.js":
/*!****************************************************!*\
  !*** ./node_modules/style-loader/lib/addStyles.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/

var stylesInDom = {};

var	memoize = function (fn) {
	var memo;

	return function () {
		if (typeof memo === "undefined") memo = fn.apply(this, arguments);
		return memo;
	};
};

var isOldIE = memoize(function () {
	// Test for IE <= 9 as proposed by Browserhacks
	// @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
	// Tests for existence of standard globals is to allow style-loader
	// to operate correctly into non-standard environments
	// @see https://github.com/webpack-contrib/style-loader/issues/177
	return window && document && document.all && !window.atob;
});

var getTarget = function (target, parent) {
  if (parent){
    return parent.querySelector(target);
  }
  return document.querySelector(target);
};

var getElement = (function (fn) {
	var memo = {};

	return function(target, parent) {
                // If passing function in options, then use it for resolve "head" element.
                // Useful for Shadow Root style i.e
                // {
                //   insertInto: function () { return document.querySelector("#foo").shadowRoot }
                // }
                if (typeof target === 'function') {
                        return target();
                }
                if (typeof memo[target] === "undefined") {
			var styleTarget = getTarget.call(this, target, parent);
			// Special case to return head of iframe instead of iframe itself
			if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
				try {
					// This will throw an exception if access to iframe is blocked
					// due to cross-origin restrictions
					styleTarget = styleTarget.contentDocument.head;
				} catch(e) {
					styleTarget = null;
				}
			}
			memo[target] = styleTarget;
		}
		return memo[target]
	};
})();

var singleton = null;
var	singletonCounter = 0;
var	stylesInsertedAtTop = [];

var	fixUrls = __webpack_require__(/*! ./urls */ "./node_modules/style-loader/lib/urls.js");

module.exports = function(list, options) {
	if (typeof DEBUG !== "undefined" && DEBUG) {
		if (typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};

	options.attrs = typeof options.attrs === "object" ? options.attrs : {};

	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (!options.singleton && typeof options.singleton !== "boolean") options.singleton = isOldIE();

	// By default, add <style> tags to the <head> element
        if (!options.insertInto) options.insertInto = "head";

	// By default, add <style> tags to the bottom of the target
	if (!options.insertAt) options.insertAt = "bottom";

	var styles = listToStyles(list, options);

	addStylesToDom(styles, options);

	return function update (newList) {
		var mayRemove = [];

		for (var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];

			domStyle.refs--;
			mayRemove.push(domStyle);
		}

		if(newList) {
			var newStyles = listToStyles(newList, options);
			addStylesToDom(newStyles, options);
		}

		for (var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];

			if(domStyle.refs === 0) {
				for (var j = 0; j < domStyle.parts.length; j++) domStyle.parts[j]();

				delete stylesInDom[domStyle.id];
			}
		}
	};
};

function addStylesToDom (styles, options) {
	for (var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];

		if(domStyle) {
			domStyle.refs++;

			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}

			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];

			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}

			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles (list, options) {
	var styles = [];
	var newStyles = {};

	for (var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = options.base ? item[0] + options.base : item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};

		if(!newStyles[id]) styles.push(newStyles[id] = {id: id, parts: [part]});
		else newStyles[id].parts.push(part);
	}

	return styles;
}

function insertStyleElement (options, style) {
	var target = getElement(options.insertInto)

	if (!target) {
		throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");
	}

	var lastStyleElementInsertedAtTop = stylesInsertedAtTop[stylesInsertedAtTop.length - 1];

	if (options.insertAt === "top") {
		if (!lastStyleElementInsertedAtTop) {
			target.insertBefore(style, target.firstChild);
		} else if (lastStyleElementInsertedAtTop.nextSibling) {
			target.insertBefore(style, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			target.appendChild(style);
		}
		stylesInsertedAtTop.push(style);
	} else if (options.insertAt === "bottom") {
		target.appendChild(style);
	} else if (typeof options.insertAt === "object" && options.insertAt.before) {
		var nextSibling = getElement(options.insertAt.before, target);
		target.insertBefore(style, nextSibling);
	} else {
		throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");
	}
}

function removeStyleElement (style) {
	if (style.parentNode === null) return false;
	style.parentNode.removeChild(style);

	var idx = stylesInsertedAtTop.indexOf(style);
	if(idx >= 0) {
		stylesInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement (options) {
	var style = document.createElement("style");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}

	if(options.attrs.nonce === undefined) {
		var nonce = getNonce();
		if (nonce) {
			options.attrs.nonce = nonce;
		}
	}

	addAttrs(style, options.attrs);
	insertStyleElement(options, style);

	return style;
}

function createLinkElement (options) {
	var link = document.createElement("link");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}
	options.attrs.rel = "stylesheet";

	addAttrs(link, options.attrs);
	insertStyleElement(options, link);

	return link;
}

function addAttrs (el, attrs) {
	Object.keys(attrs).forEach(function (key) {
		el.setAttribute(key, attrs[key]);
	});
}

function getNonce() {
	if (false) {}

	return __webpack_require__.nc;
}

function addStyle (obj, options) {
	var style, update, remove, result;

	// If a transform function was defined, run it on the css
	if (options.transform && obj.css) {
	    result = typeof options.transform === 'function'
		 ? options.transform(obj.css) 
		 : options.transform.default(obj.css);

	    if (result) {
	    	// If transform returns a value, use that instead of the original css.
	    	// This allows running runtime transformations on the css.
	    	obj.css = result;
	    } else {
	    	// If the transform function returns a falsy value, don't add this css.
	    	// This allows conditional loading of css
	    	return function() {
	    		// noop
	    	};
	    }
	}

	if (options.singleton) {
		var styleIndex = singletonCounter++;

		style = singleton || (singleton = createStyleElement(options));

		update = applyToSingletonTag.bind(null, style, styleIndex, false);
		remove = applyToSingletonTag.bind(null, style, styleIndex, true);

	} else if (
		obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function"
	) {
		style = createLinkElement(options);
		update = updateLink.bind(null, style, options);
		remove = function () {
			removeStyleElement(style);

			if(style.href) URL.revokeObjectURL(style.href);
		};
	} else {
		style = createStyleElement(options);
		update = applyToTag.bind(null, style);
		remove = function () {
			removeStyleElement(style);
		};
	}

	update(obj);

	return function updateStyle (newObj) {
		if (newObj) {
			if (
				newObj.css === obj.css &&
				newObj.media === obj.media &&
				newObj.sourceMap === obj.sourceMap
			) {
				return;
			}

			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;

		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag (style, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (style.styleSheet) {
		style.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = style.childNodes;

		if (childNodes[index]) style.removeChild(childNodes[index]);

		if (childNodes.length) {
			style.insertBefore(cssNode, childNodes[index]);
		} else {
			style.appendChild(cssNode);
		}
	}
}

function applyToTag (style, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		style.setAttribute("media", media)
	}

	if(style.styleSheet) {
		style.styleSheet.cssText = css;
	} else {
		while(style.firstChild) {
			style.removeChild(style.firstChild);
		}

		style.appendChild(document.createTextNode(css));
	}
}

function updateLink (link, options, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	/*
		If convertToAbsoluteUrls isn't defined, but sourcemaps are enabled
		and there is no publicPath defined then lets turn convertToAbsoluteUrls
		on by default.  Otherwise default to the convertToAbsoluteUrls option
		directly
	*/
	var autoFixUrls = options.convertToAbsoluteUrls === undefined && sourceMap;

	if (options.convertToAbsoluteUrls || autoFixUrls) {
		css = fixUrls(css);
	}

	if (sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = link.href;

	link.href = URL.createObjectURL(blob);

	if(oldSrc) URL.revokeObjectURL(oldSrc);
}


/***/ }),

/***/ "./node_modules/style-loader/lib/urls.js":
/*!***********************************************!*\
  !*** ./node_modules/style-loader/lib/urls.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports) {


/**
 * When source maps are enabled, `style-loader` uses a link element with a data-uri to
 * embed the css on the page. This breaks all relative urls because now they are relative to a
 * bundle instead of the current page.
 *
 * One solution is to only use full urls, but that may be impossible.
 *
 * Instead, this function "fixes" the relative urls to be absolute according to the current page location.
 *
 * A rudimentary test suite is located at `test/fixUrls.js` and can be run via the `npm test` command.
 *
 */

module.exports = function (css) {
  // get current location
  var location = typeof window !== "undefined" && window.location;

  if (!location) {
    throw new Error("fixUrls requires window.location");
  }

	// blank or null?
	if (!css || typeof css !== "string") {
	  return css;
  }

  var baseUrl = location.protocol + "//" + location.host;
  var currentDir = baseUrl + location.pathname.replace(/\/[^\/]*$/, "/");

	// convert each url(...)
	/*
	This regular expression is just a way to recursively match brackets within
	a string.

	 /url\s*\(  = Match on the word "url" with any whitespace after it and then a parens
	   (  = Start a capturing group
	     (?:  = Start a non-capturing group
	         [^)(]  = Match anything that isn't a parentheses
	         |  = OR
	         \(  = Match a start parentheses
	             (?:  = Start another non-capturing groups
	                 [^)(]+  = Match anything that isn't a parentheses
	                 |  = OR
	                 \(  = Match a start parentheses
	                     [^)(]*  = Match anything that isn't a parentheses
	                 \)  = Match a end parentheses
	             )  = End Group
              *\) = Match anything and then a close parens
          )  = Close non-capturing group
          *  = Match anything
       )  = Close capturing group
	 \)  = Match a close parens

	 /gi  = Get all matches, not the first.  Be case insensitive.
	 */
	var fixedCss = css.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi, function(fullMatch, origUrl) {
		// strip quotes (if they exist)
		var unquotedOrigUrl = origUrl
			.trim()
			.replace(/^"(.*)"$/, function(o, $1){ return $1; })
			.replace(/^'(.*)'$/, function(o, $1){ return $1; });

		// already a full url? no change
		if (/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(unquotedOrigUrl)) {
		  return fullMatch;
		}

		// convert the url to a full url
		var newUrl;

		if (unquotedOrigUrl.indexOf("//") === 0) {
		  	//TODO: should we add protocol?
			newUrl = unquotedOrigUrl;
		} else if (unquotedOrigUrl.indexOf("/") === 0) {
			// path should be relative to the base url
			newUrl = baseUrl + unquotedOrigUrl; // already starts with '/'
		} else {
			// path should be relative to current directory
			newUrl = currentDir + unquotedOrigUrl.replace(/^\.\//, ""); // Strip leading './'
		}

		// send back the fixed url(...)
		return "url(" + JSON.stringify(newUrl) + ")";
	});

	// send back the fixed css
	return fixedCss;
};


/***/ }),

/***/ "./src/css/style.scss":
/*!****************************!*\
  !*** ./src/css/style.scss ***!
  \****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../node_modules/mini-css-extract-plugin/dist/loader.js!../../node_modules/css-loader/dist/cjs.js!../../node_modules/extract-svg-sprite-webpack-plugin/lib/css-loader.js!../../node_modules/sass-loader/dist/cjs.js??ref--7-4!./style.scss */ "./node_modules/mini-css-extract-plugin/dist/loader.js!./node_modules/css-loader/dist/cjs.js!./node_modules/extract-svg-sprite-webpack-plugin/lib/css-loader.js!./node_modules/sass-loader/dist/cjs.js?!./src/css/style.scss");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../../node_modules/style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./src/js/index.js":
/*!*************************!*\
  !*** ./src/js/index.js ***!
  \*************************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./src/js/utils.js");


/* index.js */

window.STEP = $('body').data('step');
window.CALC_NAME = $('body').data('calc-name');
(function Main() {
  const indexjs = () => {
    // console.log('index.js working...');

    if (window && window.innerWidth > 600) {}
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
  document.addEventListener('DOMContentLoaded', _utils__WEBPACK_IMPORTED_MODULE_0__["smoothAnchorSlide"]);
})();
function main() {
  let $signupButton = $('.js-signup');
  let $loginButton = $('.js-login');
  let $calcMenuParent = $('.js-menu-parent .calc-menu__link');
  let $robokassaForm = $('.js-robokassa-form').find('form');
  let $getPaymentMethodsButton = $('.js-get-payment-methods');
  let $achievementClose = $('.js-achievement-close');
  let $popupOpen = $('.js-popup-with-content');
  $signupButton.length && $signupButton.click(function (e) {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getAjaxByUrl"])('/all/accounts/signup_ajax/', success);
    function success(html) {
      Object(_utils__WEBPACK_IMPORTED_MODULE_0__["openFancybox"])(html);
      signup();
    }
  });
  $loginButton.length && $loginButton.click(function (e) {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getAjaxByUrl"])('/all/accounts/login_ajax/', success);
    function success(html) {
      Object(_utils__WEBPACK_IMPORTED_MODULE_0__["openFancybox"])(html);
      login();
    }
  });
  $calcMenuParent.length && $calcMenuParent.click(function (e) {
    let $this = $(this);
    let $targetEl = $this.parent();
    let $child = $targetEl.children('ul');
    let activeClass = 'is-active';
    $child.slideToggle();
    $targetEl.toggleClass(activeClass);
  });
  $achievementClose.length && $achievementClose.click(function (e) {
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
      success: function (res) {
        $this.parent().slideToggle();
      },
      error: function (res) {
        alert('Ошибка! Попробуйте позже!');
      }
    });
  });
  $.each($getPaymentMethodsButton, function (i, item) {
    $(item).click({
      'calc_name': $(item).data('calc-name'),
      'price_type': $(item).parent().find('[name=price_type]').val()
    }, _utils__WEBPACK_IMPORTED_MODULE_0__["getPaymentMethodsAjax"]);
  });
  $popupOpen.length && $popupOpen.click(function (e) {
    let $this = $(this);
    let url = $this.data('url');
    let data = {
      calc_name: $this.data('calc-name')
    };
    $.ajax({
      url,
      data,
      method: 'POST',
      dataType: 'html',
      success: function (res) {
        $.fancybox.open({
          src: res,
          type: 'html',
          opts: {
            buttons: ['close'],
            padding: 0,
            smallBtn: false,
            btnTpl: {
              close: '<button data-fancybox-close class="popup__close""></button>"'
            }
          }
        });
      },
      error: function (res) {
        alert('Ошибка! Попробуйте позже!');
      }
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
  $form.length && $form.submit(function (e) {
    if (!isSended) {
      $.each($inputs, function () {
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
        success: function (res) {
          $fieldset.prop('disabled', '');
          if ($.isEmptyObject(res["errors"])) {
            window.location.href = redirect_to;
          } else {
            let errors = res["errors"];
            for (let key in errors) {
              $errors.append(`<p class="error">${errors[key]}</p>`);
            }
            isSended = false;
          }
        },
        error: function (res) {
          alert('Ошибка! Попробуйте позже!');
          $fieldset.prop('disabled', '');
          isSended = false;
        }
      });
    }
    return false;
  });
  $reset.length && $reset.click(function (e) {
    let $this = $(this);
    let url = $this.attr('href');
    $.ajax({
      url,
      method: 'GET',
      dataType: 'json',
      headers: {
        'X-CSRFToken': csrfmiddlewaretoken
      },
      success: function (res) {
        let json = JSON.parse(res.html);
        Object(_utils__WEBPACK_IMPORTED_MODULE_0__["openFancybox"])(json.html);
        resetPasswordAjax();
      },
      error: function (res) {
        alert('Ошибка! Попробуйте позже!');
      }
    });
    return false;
  });
  $signupButton.length && $signupButton.click(function (e) {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getAjaxByUrl"])('/all/accounts/signup_ajax/', success);
    function success(html) {
      Object(_utils__WEBPACK_IMPORTED_MODULE_0__["openFancybox"])(html);
      signup();
    }
  });
  Object(_utils__WEBPACK_IMPORTED_MODULE_0__["showPassword"])();
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
  $form.length && $form.submit(function (e) {
    if (!isSended) {
      $.each($inputs, function () {
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
        success: function (res) {
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
              success: function (res) {
                $form.parent().parent().html(res);
              },
              error: function (res) {
                alert('Ошибка! Попробуйте позже!');
              }
            });
            if ($.fancybox) {
              // $.fancybox.destroy();
            }
          } else {
            let errors = res["errors"];
            for (let key in errors) {
              $errors.append(`<p class="error">${errors[key]}</p>`);
            }
          }
          isSended = false;
          $fieldset.prop('disabled', '');
        },
        error: function (res) {
          alert('Ошибка! Попробуйте позже!');
          $fieldset.prop('disabled', '');
          isSended = false;
        }
      });
    }
    return false;
  });
  Object(_utils__WEBPACK_IMPORTED_MODULE_0__["showPassword"])();
}
function index() {}
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
  $form.length && $form.submit(function (e) {
    if (!isSended) {
      let email;
      $.each($inputs, function () {
        let $this = $(this);
        data[$this.attr('name')] = $this.val();
        if ($this.attr('name') == 'email') email = $this.val();
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
        success: function (res) {
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
              success: function (res) {
                $form.parent().parent().html(res);
              },
              error: function (res) {
                alert('Ошибка! Попробуйте позже!');
              }
            });
          } else {
            let errors = res["errors"];
            for (let key in errors) {
              $errors.append(`<p class="error">${errors[key]}</p>`);
            }
            isSended = false;
          }
        },
        error: function (res) {
          alert('Ошибка! Попробуйте позже!');
          $fieldset.prop('disabled', '');
          isSended = false;
        }
      });
    }
    return false;
  });
  $loginButton.length && $loginButton.click(function (e) {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getAjaxByUrl"])('/all/accounts/login_ajax/', success);
    function success(html) {
      Object(_utils__WEBPACK_IMPORTED_MODULE_0__["openFancybox"])(html);
      login();
    }
  });
  Object(_utils__WEBPACK_IMPORTED_MODULE_0__["showPassword"])();
}
function stepDocx() {
  let $form = $('.js-form');
  Object(_utils__WEBPACK_IMPORTED_MODULE_0__["sendMailForm"])('js-form');
}
function stepShort() {
  let $form = $('.js-form-send-promo');
  let $fieldset = $form.find('.js-fieldset');
  if ($form.length) {
    let $letters = $fieldset.find('input');
    $letters.on('paste', function (e) {
      let text = e.originalEvent.clipboardData.getData('text/plain');
      for (let i = 0; i < text.length; i++) {
        $letters[i] && $($letters[i]).val(text[i]);
      }
      return false;
    });
    $letters.on('keyup', function (e) {
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
    $form.submit(function (e) {
      if (!isSended) {
        let promo = '';
        $.each($fieldset.find('input'), function (i, item) {
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
            success: function (res) {
              if (res == 'OK') {
                // window.location.href = next_step;
              } else {
                isSended = false;
                $fieldset.prop('disabled', '');
              }
            },
            error: function (res) {
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
function stepFull() {}
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
  if (STORAGE['group_name_' + group_number] && STORAGE['group_count_' + group_number] && STORAGE['group_data_' + group_number]) {
    isShowGroup = true;
  }
  if (STORAGE['group_name_' + group_number]) $groupName.val(STORAGE['group_name_' + group_number]);
  if (STORAGE['group_count_' + group_number]) $groupCount.val(STORAGE['group_count_' + group_number]);
  $form.length && $form.submit(function (e) {
    let $this = $(this);
    let isValidForm = true;
    $('.' + classError).removeClass(classError);
    if (!$groupName.val()) {
      $groupName.addClass(classError);
      $groupName.prev().addClass(classError);
      isValidForm = false;
    }
    if (!$groupCount.val() || !parseInt($groupCount.val())) {
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
        success: function (res) {
          $groupData.html(res);
          $hideOnClick.hide();
          $groupData.on('paste', 'input', pasteFromBufferToTable);
          isSended = false;
          getGroupInputs();
          addTableHScroll();
        },
        error: function (res) {
          if (res.responseText == 'count') {
            let anotherGroupName = group_number == 1 ? STORAGE['group_name_2'] : STORAGE['group_name_1'];
            let anotherGroupCount = group_number == 1 ? STORAGE['group_count_2'] : STORAGE['group_count_1'];
            alert('В группе ' + anotherGroupName + ' ' + anotherGroupCount + ' человек, ' + 'поэтому в текущей группе должно быть тоже ' + anotherGroupCount + ' человек. ' + 'Группы должны быть равны по количеству участников.');
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
  if (isShowGroup) $form.trigger('submit');
  function pasteFromBufferToTable(e) {
    var $this = $(this);
    $.each(e.originalEvent.clipboardData.items, function (i, v) {
      if (v.type === 'text/plain') {
        v.getAsString(function (text) {
          var newLine = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getNewLineType"])(Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getOSName"])());
          var spaces = new RegExp('[(\s*)]');
          var corr = 0;
          var x = $this.closest('td').index() - 1,
            // - th
            y = $this.closest('tr').index();
          text = text.trim(newLine);
          $.each(text.split(new RegExp('[' + newLine + ']')), function (i2, v2) {
            if (v2 == '') {
              corr++;
              return true;
            }
            $.each(v2.split('\t'), function (i3, v3) {
              v3 = v3.trim(' ');
              var row = y + i2,
                col = x + i3;
              var $targetInput = $this.closest('tbody').find('tr:eq(' + (row - corr) + ') td:eq(' + col + ') input');
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
    $.each($change, function (i, elem) {
      let $this = $(this);
      let $name = $this.find('.js-group-name');
      let $count = $this.find('.js-group-count');
      if (STORAGE['group_name_' + (i + 1)]) $name.text(STORAGE['group_name_' + (i + 1)]);
      if (STORAGE['group_count_' + (i + 1)]) $count.text(STORAGE['group_count_' + (i + 1)]);
      $this.attr('href', `/all/${calc_name}/steps/${i + 2}/`);
    });
    function addBody(count, group_data, group_name, group_number) {
      let template = '';
      for (let i = 0; i < count; i++) {
        template += `<tr class="table__tbody-tr table__group-row--${group_number}">`;
        template += `<th class="table__tbody-th" scope="row">Группа "${group_name}" / Испытуемый ${i + 1}</th>`;
        for (let scale in group_data) {
          template += `<td class="table__tbody-td">${group_data[scale][i + 1]}</span></td>`;
        }
        template += '</tr>';
      }
      $($table.find('tbody')).append(template);
    }
  }
  $form.length && $form.submit(function () {
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
        success: function (res) {
          if (res == 'OK') {
            Object(_utils__WEBPACK_IMPORTED_MODULE_0__["preloader"])();
            window.location.href = next_step;
          } else {
            isSended = false;
            $fieldset.prop('disabled', '');
          }
        },
        error: function (res) {
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
      Object(_utils__WEBPACK_IMPORTED_MODULE_0__["addInputWithValue"])(scales[input], newInputPlace);
    }
  }
  $newScaleInput.click(function () {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["addInputWithValue"])(false, newInputPlace);
  });
  $formScales.length && $formScales.submit(function (e) {
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
      $.each($inputs, function (i) {
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
        success: function (res) {
          if (res == 'OK') {
            STORAGE['scales'] = newScales;
            sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
            window.location.href = next_step;
          }
        },
        error: function (res) {
          if (res.responseText == 'ERROR') {
            $error.addClass(classError);
          } else if (res.responseText == 'QUANTITY') {
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
  $inputPlace.on('paste', 'input', function (e) {
    let $this = $(this);
    let scaleInput = '.js-scale-input';
    $.each(e.originalEvent.clipboardData.items, function (i, val) {
      if (val.type === 'text/plain') {
        val.getAsString(function (text) {
          let newLine = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getNewLineType"])(Object(_utils__WEBPACK_IMPORTED_MODULE_0__["getOSName"])());
          let y = $this.closest(scaleInput).index();
          let corr = 0;
          text = text.trim(newLine);
          let values = text.split(new RegExp('[' + newLine + '|\t]'));
          $.each(values, function (i_row, val_row) {
            if (val_row == '') {
              corr++;
              return true;
            }
            val_row = val_row.trim(' ');
            let index = y + i_row - corr;
            let $targetInput = $inputPlace.find(`${scaleInput}:eq(${index}) input`);
            if (!$targetInput.length) {
              Object(_utils__WEBPACK_IMPORTED_MODULE_0__["addInputWithValue"])(val_row, newInputPlace);
            } else {
              $targetInput.val(val_row);
            }
          });
        });
      }
    });
    return false;
  });
  $formUpload.length && $formUpload.submit(function (e) {
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
        success: function (res) {
          STORAGE['scales'] = res;
          sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
          window.location.href = '';
        },
        error: function (res) {
          isSended = false;
          alert('Ошибка! Попробуйте позже!');
          $fieldset.prop('disabled', '');
        }
      });
    }
    return false;
  });
  $clearSotarage && $clearSotarage.click(function () {
    Object(_utils__WEBPACK_IMPORTED_MODULE_0__["clearStorage"])();
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
    $.each($inputs, function () {
      let $this = $(this);
      if (typeof group_data[$this.data('scale')] !== 'undefined' && typeof group_data[$this.data('scale')][$this.data('person')] !== 'undefined') $this.val(group_data[$this.data('scale')][$this.data('person')]);
    });
  }
  $form.length && $form.submit(function (e) {
    let isConfirm = Object(_utils__WEBPACK_IMPORTED_MODULE_0__["confirmEmptySubmit"])('js-form-values');
    if (isConfirm && !isSended) {
      let $this = $(this);
      let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();
      let values = {};
      let $fieldset = $this.find('.js-fieldset');
      let url = $this.attr('action');
      $.each($inputs, function () {
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
        success: function (res) {
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
        error: function (res) {
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
  $formUpload.length && $formUpload.submit(function (e) {
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
        success: function (res) {
          STORAGE['group_data_' + group_number] = res;
          sessionStorage[CALC_NAME] = JSON.stringify(STORAGE);
          window.location.href = '';
        },
        error: function (res) {
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
  if (typeof ym !== 'undefined') {
    let ym_params = {};
    $(document).on('submit', '.js-ym-registration', function (e) {
      ym(YM_ID, 'reachGoal', 'registration', ym_params);
    });
    $(document).on('submit', '.js-ym-autorization', function (e) {
      ym(YM_ID, 'reachGoal', 'autorization', ym_params);
    });
    $(document).on('submit', '.js-ym-pay', function (e) {
      if ($('input[name="OutSum"]').length) {
        ym_params['order_price'] = $('input[name="OutSum"]').val();
      }
      ym(YM_ID, 'reachGoal', 'pay', ym_params);
    });
  }
  if (typeof ga !== 'undefined') {
    $(document).on('submit', '.js-ym-registration', function (e) {
      ga('send', 'event', 'account', 'registration');
    });
    $(document).on('submit', '.js-ym-autorization', function (e) {
      ga('send', 'event', 'account', 'autorization');
    });
    $(document).on('submit', '.js-ym-pay', function (e) {
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
  $form.length && $form.submit(function (e) {
    if (!isSended) {
      let $this = $(this);
      let $fieldset = $this.find('.js-fieldset');
      let $error = $this.find('.js-promo-error');
      let csrftoken = $this.find('[name="csrfmiddlewaretoken"]').val();
      let url = $this.attr('action');
      let $promoLetters = $('.js-promo-letters');
      let promo = '';
      $.each($promoLetters.find('input'), function (i, item) {
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
        success: function (res) {
          console.log(res);
          window.location.href = '';
          // if (res == 'OK') {
          // } else {
          //     isSended = false;
          //     $fieldset.prop('disabled', '');
          // }
        },
        error: function (res) {
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
    $letters.on('keyup', function (e) {
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
    $form.submit(function (e) {
      return false;
    });
  }
  $promoDelete.length && $promoDelete.click(function (e) {
    if (confirm('Вы действительно хотите удалить промокод?')) {
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
        success: function (res) {
          if ($this.closest('tr').remove()) alert('Промокод удалён');
        },
        error: function (res) {
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
  $addEmailShow.length && $addEmailForm.length && $addEmailShow.click(function (e) {
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
  $form.length && $form.submit(function (e) {
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
        success: function (res) {
          $this_form.html('<p>Пароль успешно изменён!</p>');
          // if (res.location) {
          //   window.location.href = res.location;
          // } else {
          //   window.location.href = '/all/';
          // }
        },
        error: function (res) {
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
  Object(_utils__WEBPACK_IMPORTED_MODULE_0__["showPassword"])();
}
function addTableHScroll() {
  let $table = $('.js-table');
  let $tableWrapper = $table.parent();
  let $tableCopy = $('.js-table-copy');
  let classActive = 'active';
  $('.js-thead-copy').innerHeight($table.find('.table__thead-th').innerHeight());
  $('.js-tcell-copy').innerHeight($table.find('.table__tbody-th').innerHeight() - 2); // border

  $tableWrapper.scroll(function (e) {
    if ($tableWrapper.scrollLeft() > 10) {
      $tableCopy.addClass(classActive);
    } else {
      $tableCopy.removeClass(classActive);
    }
  });
}
window.YM_ID = '57165547';
window.ya = ya;
window.removeScale = _utils__WEBPACK_IMPORTED_MODULE_0__["removeScale"];
window.submitForm = _utils__WEBPACK_IMPORTED_MODULE_0__["submitForm"];
window.promoApply = _utils__WEBPACK_IMPORTED_MODULE_0__["promoApply"];
window.getPaymentMethodsAjax = _utils__WEBPACK_IMPORTED_MODULE_0__["getPaymentMethodsAjax"];
window.changePaymentMethodsAjax = _utils__WEBPACK_IMPORTED_MODULE_0__["changePaymentMethodsAjax"];
window.click_ya_payment_from_form = _utils__WEBPACK_IMPORTED_MODULE_0__["click_ya_payment_from_form"];
window.click_ga_payment = _utils__WEBPACK_IMPORTED_MODULE_0__["click_ga_payment"];
window.paymentFilter = _utils__WEBPACK_IMPORTED_MODULE_0__["paymentFilter"];
window.selectPaymentMethod = _utils__WEBPACK_IMPORTED_MODULE_0__["selectPaymentMethod"];
window.showPassword = _utils__WEBPACK_IMPORTED_MODULE_0__["showPassword"];
window.preloader = _utils__WEBPACK_IMPORTED_MODULE_0__["preloader"];

/***/ }),

/***/ "./src/js/utils.js":
/*!*************************!*\
  !*** ./src/js/utils.js ***!
  \*************************/
/*! exports provided: getOSName, getNewLineType, confirmEmptySubmit, sendMailForm, addInputWithValue, removeScale, getCookie, getCaptcha, clearStorage, getAjaxByUrl, getPaymentFormAjax, getPaymentMethodsAjax, changePaymentMethodsAjax, submitForm, smoothAnchorSlide, openFancybox, promoApply, click_ya_payment_from_form, click_ga_payment, paymentFilter, selectPaymentMethod, showPassword, preloader */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getOSName", function() { return getOSName; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getNewLineType", function() { return getNewLineType; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "confirmEmptySubmit", function() { return confirmEmptySubmit; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sendMailForm", function() { return sendMailForm; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "addInputWithValue", function() { return addInputWithValue; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "removeScale", function() { return removeScale; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCookie", function() { return getCookie; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCaptcha", function() { return getCaptcha; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clearStorage", function() { return clearStorage; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getAjaxByUrl", function() { return getAjaxByUrl; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getPaymentFormAjax", function() { return getPaymentFormAjax; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getPaymentMethodsAjax", function() { return getPaymentMethodsAjax; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "changePaymentMethodsAjax", function() { return changePaymentMethodsAjax; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "submitForm", function() { return submitForm; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "smoothAnchorSlide", function() { return smoothAnchorSlide; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "openFancybox", function() { return openFancybox; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "promoApply", function() { return promoApply; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "click_ya_payment_from_form", function() { return click_ya_payment_from_form; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "click_ga_payment", function() { return click_ga_payment; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "paymentFilter", function() { return paymentFilter; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "selectPaymentMethod", function() { return selectPaymentMethod; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "showPassword", function() { return showPassword; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "preloader", function() { return preloader; });


var inputCount = 2;
var sitekey = '6LfDtY4UAAAAANEBfbIswo6tCV7SjUyrSfci02aQ';
function getOSName() {
  var OSName = "Unknown";
  if (navigator.appVersion.indexOf("Win") != -1) OSName = "Windows";else if (navigator.appVersion.indexOf("Mac") != -1) OSName = "MacOS";else if (navigator.appVersion.indexOf("X11") != -1) OSName = "UNIX";else if (navigator.appVersion.indexOf("Linux") != -1) OSName = "Linux";
  return OSName;
}
function getNewLineType(OSName) {
  var newLine = '\n';
  if (OSName == "Windows") newLine = '\r\n';else if (OSName == "MacOS") newLine = '\n';else if (OSName == "UNIX") newLine = '\n';else if (OSName == "Linux") newLine = '\n';
  return newLine;
}
function confirmEmptySubmit(classForm) {
  let $form = $('.' + classForm);
  let $zeroed = $form.find('.js-zeroed');
  // let $close = $form.find('.js-fancybox-close');
  let isConfirm = true;
  let $inputs = $form.find('input');
  let $modal = $('#confirm');
  $zeroed.click(function () {
    $.each($inputs, function () {
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

  $.each($inputs, function () {
    let $this = $(this);
    if ($this.val() == '') {
      $.fancybox.open({
        src: $modal,
        type: 'html',
        opts: {
          buttons: [],
          padding: 0,
          smallBtn: false,
          helpers: {
            overlay: {
              css: {
                'background-color': 'rgba(0,0,0,.3)'
              }
            }
          }
        }
      });
      isConfirm = false;
      return false;
    }
  });
  return isConfirm;
}
function sendMailForm(classForm) {
  var $form = $('.' + classForm);
  let $formCover = $form.find('.js-form-cover');
  let $fieldset = $form.find('.js-fieldset');
  let isSended = false;
  let next_step = $form.find('[name="next_step"]').val();
  let calc_name = $form.find('[name="calc_name"]').val();
  let action = $form.find('[name="action"]').val();
  let url = $form.attr('action');
  let csrfmiddlewaretoken = $form.find('[name="csrfmiddlewaretoken"]').val();
  $form.length && $form.on('submit', function (e) {
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
        success: function (res) {
          if (res == 'OK') {
            $form.html('<b>Сообщение успешно отправлено на почту ' + email + '!</b>');
            if (next_step) window.location.href = next_step;
          }
        },
        error: function (res) {
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
}
;
function addInputWithValue(value, place) {
  let $place = $(place);
  value = value || '';
  let html = `<div class="step-page__scale">
                    <input type="text" class="step-page__scale-input input" name="scale-${inputCount}" placeholder="Введите название" value="${value}">
                    <button onclick="removeScale(this)" type="button" class="step-page__scale-remove">Удалить шкалу</button>
                </div>`;
  $place.append(html);
  inputCount++;
}
function removeScale(button) {
  $(button).parent().remove();
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = $.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function getCaptcha(csrfmiddlewaretoken) {
  typeof grecaptcha !== 'undefined' && grecaptcha.ready(function () {
    grecaptcha.execute(sitekey, {
      action: 'statpsy'
    }).then(function (token) {
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
function clearStorage() {
  let csrftoken = $('[name="csrfmiddlewaretoken"]').val();
  delete sessionStorage[CALC_NAME];
  $.ajax({
    url: '/all/ajax/session_clear/',
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: function (res) {
      window.location.href = '';
    }
  });
}
function getAjaxByUrl(url, success) {
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

function getPaymentFormAjax(data) {
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
    success: function (res) {
      $.fancybox.open({
        src: res,
        type: 'html',
        opts: {
          buttons: [],
          padding: 0,
          smallBtn: false
          // btnTpl: {
          //   close:
          //     '<button data-fancybox-close class="popup-payment__close""></button>"'
          // }
        }
      });
      $fieldset.prop('disabled', '');
      isChanged = false;
    },
    error: function (res) {
      // console.log(res);
      alert('Ошибка! Попробуйте позже!');
      $fieldset.prop('disabled', '');
      isChanged = false;
    }
  });
  return;
}
;
function getPaymentMethodsAjax(e) {
  let $this = $(this);
  ;
  let calc_name;
  let IncCurrLabel;
  let price_type;
  if (e && typeof e.data !== 'undefined') {
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
      success: function (res) {
        $.fancybox.open({
          src: res,
          type: 'html',
          opts: {
            buttons: [],
            padding: 0,
            smallBtn: false
            // btnTpl: {
            //   close:
            //     '<button data-fancybox-close class="popup-payment__close""></button>"'
            // }
          }
        });
        $fieldset.prop('disabled', '');
        isChanged = false;
      },
      error: function (res) {
        // console.log(res);
        alert('Ошибка! Попробуйте позже!');
        $fieldset.prop('disabled', '');
        isChanged = false;
      }
    });
  }
  return;
}
;
function changePaymentMethodsAjax(select) {
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
      success: function (res) {
        $.fancybox.destroy();
        $.fancybox.open(res);
        $fieldset.prop('disabled', '');
        isChanged = false;
      },
      error: function (res) {
        // console.log(res);
        alert('Ошибка! Попробуйте позже!');
        $fieldset.prop('disabled', '');
        isChanged = false;
      }
    });
  }
  return;
}
function submitForm() {
  let formWrapperClass = '.js-robokassa-form';
  let $form = $(formWrapperClass).find('form');
  click_ya_payment_from_form($form);
  click_ga_payment();

  // console.log($form);
  $form.submit();
}
function smoothAnchorSlide() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      let href = this.getAttribute('href');
      if (href !== '' && href !== '#') document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
      return true;
    });
  });
}
;
function openFancybox(html) {
  $.fancybox.destroy();
  $.fancybox.open({
    src: html,
    type: 'html',
    opts: {
      buttons: [],
      padding: 0,
      smallBtn: false
    }
  });
}
function promoApply(button) {
  let $this = $(button);
  let $form = $this.closest('.js-robokassa-form');
  let isApply = true;
  $wrapper = $this.closest('.js-payment-place');
  let $fieldset = $wrapper.find('.js-fieldset');
  let csrftoken = $form.find('[name="csrfmiddlewaretoken"]').val();
  $fieldset.prop('disabled', 'disabled');
  if (isApply) {
    let promo = $wrapper.find('[name="shppromo"]').val();
    let calc_name = $wrapper.find('[name="shpcalc_name"]').val();
    let url = '/all/accounts/apply_promo/';
    $.ajax({
      url,
      data: {
        promo,
        calc_name
      },
      method: 'POST',
      dataType: 'html',
      headers: {
        'X-CSRFToken': csrftoken
      },
      cache: false,
      success: function (res) {
        $wrapper.html(res);
        isApply = false;
      },
      error: function (res) {
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
function click_ya_payment_from_form($form) {
  if (typeof ym !== 'undefined') {
    let ym_params = {};
    if ($form && $form.find('input[name="shpfull_price"]').length) {
      ym_params['order_price'] = $form.find('input[name="shpfull_price"]').val();
    }
    ym(YM_ID, 'reachGoal', 'pay', ym_params);
  }
}
function click_ga_payment() {
  if (typeof ga !== 'undefined') {
    ga('send', 'event', 'robokassa_form', 'pay');
  }
}
function paymentFilter(el) {
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
function selectPaymentMethod(el) {
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
    success: function (res) {
      $hiddenFormPlace.html(res);
    },
    error: function (res) {
      alert('Ошибка! Попробуйте позже!');
    }
  });
}
function showPassword() {
  let $showPassword = $('.js-show-password');
  $showPassword.length && $showPassword.click(function () {
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
function preloader() {
  let preloader = document.getElementById("preloader");
  if (preloader) {
    setTimeout(() => {
      preloader.style.display = "block";
    }, 400);
  } else {
    console.log('No preloader');
  }
}
;

/***/ }),

/***/ 0:
/*!****************************************************!*\
  !*** multi ./src/css/style.scss ./src/js/index.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! ./src/css/style.scss */"./src/css/style.scss");
module.exports = __webpack_require__(/*! ./src/js/index.js */"./src/js/index.js");


/***/ })

/******/ });
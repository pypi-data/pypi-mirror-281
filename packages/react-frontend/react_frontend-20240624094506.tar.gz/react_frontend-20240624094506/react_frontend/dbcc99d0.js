/*! For license information please see dbcc99d0.js.LICENSE.txt */
"use strict";(self.webpackChunkreact_frontend=self.webpackChunkreact_frontend||[]).push([[4874],{4874:function(t,e,r){r.r(e),r.d(e,{HuiPictureCard:function(){return A}});var n,i,o=r(7599),a=r(46323),c=r(228),s=r(48399),l=r(38513),u=(r(68336),r(63383)),f=r(16494),h=r(26876);function d(t){return d="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},d(t)}function p(t,e){return e||(e=t.slice(0)),Object.freeze(Object.defineProperties(t,{raw:{value:Object.freeze(e)}}))}function y(){y=function(){return t};var t={},e=Object.prototype,r=e.hasOwnProperty,n=Object.defineProperty||function(t,e,r){t[e]=r.value},i="function"==typeof Symbol?Symbol:{},o=i.iterator||"@@iterator",a=i.asyncIterator||"@@asyncIterator",c=i.toStringTag||"@@toStringTag";function s(t,e,r){return Object.defineProperty(t,e,{value:r,enumerable:!0,configurable:!0,writable:!0}),t[e]}try{s({},"")}catch(C){s=function(t,e,r){return t[e]=r}}function l(t,e,r,i){var o=e&&e.prototype instanceof h?e:h,a=Object.create(o.prototype),c=new j(i||[]);return n(a,"_invoke",{value:_(t,r,c)}),a}function u(t,e,r){try{return{type:"normal",arg:t.call(e,r)}}catch(C){return{type:"throw",arg:C}}}t.wrap=l;var f={};function h(){}function p(){}function m(){}var v={};s(v,o,(function(){return this}));var g=Object.getPrototypeOf,b=g&&g(g(S([])));b&&b!==e&&r.call(b,o)&&(v=b);var w=m.prototype=h.prototype=Object.create(v);function k(t){["next","throw","return"].forEach((function(e){s(t,e,(function(t){return this._invoke(e,t)}))}))}function E(t,e){function i(n,o,a,c){var s=u(t[n],t,o);if("throw"!==s.type){var l=s.arg,f=l.value;return f&&"object"==d(f)&&r.call(f,"__await")?e.resolve(f.__await).then((function(t){i("next",t,a,c)}),(function(t){i("throw",t,a,c)})):e.resolve(f).then((function(t){l.value=t,a(l)}),(function(t){return i("throw",t,a,c)}))}c(s.arg)}var o;n(this,"_invoke",{value:function(t,r){function n(){return new e((function(e,n){i(t,r,e,n)}))}return o=o?o.then(n,n):n()}})}function _(t,e,r){var n="suspendedStart";return function(i,o){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===i)throw o;return L()}for(r.method=i,r.arg=o;;){var a=r.delegate;if(a){var c=x(a,r);if(c){if(c===f)continue;return c}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var s=u(t,e,r);if("normal"===s.type){if(n=r.done?"completed":"suspendedYield",s.arg===f)continue;return{value:s.arg,done:r.done}}"throw"===s.type&&(n="completed",r.method="throw",r.arg=s.arg)}}}function x(t,e){var r=e.method,n=t.iterator[r];if(void 0===n)return e.delegate=null,"throw"===r&&t.iterator.return&&(e.method="return",e.arg=void 0,x(t,e),"throw"===e.method)||"return"!==r&&(e.method="throw",e.arg=new TypeError("The iterator does not provide a '"+r+"' method")),f;var i=u(n,t.iterator,e.arg);if("throw"===i.type)return e.method="throw",e.arg=i.arg,e.delegate=null,f;var o=i.arg;return o?o.done?(e[t.resultName]=o.value,e.next=t.nextLoc,"return"!==e.method&&(e.method="next",e.arg=void 0),e.delegate=null,f):o:(e.method="throw",e.arg=new TypeError("iterator result is not an object"),e.delegate=null,f)}function O(t){var e={tryLoc:t[0]};1 in t&&(e.catchLoc=t[1]),2 in t&&(e.finallyLoc=t[2],e.afterLoc=t[3]),this.tryEntries.push(e)}function P(t){var e=t.completion||{};e.type="normal",delete e.arg,t.completion=e}function j(t){this.tryEntries=[{tryLoc:"root"}],t.forEach(O,this),this.reset(!0)}function S(t){if(t){var e=t[o];if(e)return e.call(t);if("function"==typeof t.next)return t;if(!isNaN(t.length)){var n=-1,i=function e(){for(;++n<t.length;)if(r.call(t,n))return e.value=t[n],e.done=!1,e;return e.value=void 0,e.done=!0,e};return i.next=i}}return{next:L}}function L(){return{value:void 0,done:!0}}return p.prototype=m,n(w,"constructor",{value:m,configurable:!0}),n(m,"constructor",{value:p,configurable:!0}),p.displayName=s(m,c,"GeneratorFunction"),t.isGeneratorFunction=function(t){var e="function"==typeof t&&t.constructor;return!!e&&(e===p||"GeneratorFunction"===(e.displayName||e.name))},t.mark=function(t){return Object.setPrototypeOf?Object.setPrototypeOf(t,m):(t.__proto__=m,s(t,c,"GeneratorFunction")),t.prototype=Object.create(w),t},t.awrap=function(t){return{__await:t}},k(E.prototype),s(E.prototype,a,(function(){return this})),t.AsyncIterator=E,t.async=function(e,r,n,i,o){void 0===o&&(o=Promise);var a=new E(l(e,r,n,i),o);return t.isGeneratorFunction(r)?a:a.next().then((function(t){return t.done?t.value:a.next()}))},k(w),s(w,c,"Generator"),s(w,o,(function(){return this})),s(w,"toString",(function(){return"[object Generator]"})),t.keys=function(t){var e=Object(t),r=[];for(var n in e)r.push(n);return r.reverse(),function t(){for(;r.length;){var n=r.pop();if(n in e)return t.value=n,t.done=!1,t}return t.done=!0,t}},t.values=S,j.prototype={constructor:j,reset:function(t){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(P),!t)for(var e in this)"t"===e.charAt(0)&&r.call(this,e)&&!isNaN(+e.slice(1))&&(this[e]=void 0)},stop:function(){this.done=!0;var t=this.tryEntries[0].completion;if("throw"===t.type)throw t.arg;return this.rval},dispatchException:function(t){if(this.done)throw t;var e=this;function n(r,n){return a.type="throw",a.arg=t,e.next=r,n&&(e.method="next",e.arg=void 0),!!n}for(var i=this.tryEntries.length-1;i>=0;--i){var o=this.tryEntries[i],a=o.completion;if("root"===o.tryLoc)return n("end");if(o.tryLoc<=this.prev){var c=r.call(o,"catchLoc"),s=r.call(o,"finallyLoc");if(c&&s){if(this.prev<o.catchLoc)return n(o.catchLoc,!0);if(this.prev<o.finallyLoc)return n(o.finallyLoc)}else if(c){if(this.prev<o.catchLoc)return n(o.catchLoc,!0)}else{if(!s)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return n(o.finallyLoc)}}}},abrupt:function(t,e){for(var n=this.tryEntries.length-1;n>=0;--n){var i=this.tryEntries[n];if(i.tryLoc<=this.prev&&r.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var o=i;break}}o&&("break"===t||"continue"===t)&&o.tryLoc<=e&&e<=o.finallyLoc&&(o=null);var a=o?o.completion:{};return a.type=t,a.arg=e,o?(this.method="next",this.next=o.finallyLoc,f):this.complete(a)},complete:function(t,e){if("throw"===t.type)throw t.arg;return"break"===t.type||"continue"===t.type?this.next=t.arg:"return"===t.type?(this.rval=this.arg=t.arg,this.method="return",this.next="end"):"normal"===t.type&&e&&(this.next=e),f},finish:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.finallyLoc===t)return this.complete(r.completion,r.afterLoc),P(r),f}},catch:function(t){for(var e=this.tryEntries.length-1;e>=0;--e){var r=this.tryEntries[e];if(r.tryLoc===t){var n=r.completion;if("throw"===n.type){var i=n.arg;P(r)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(t,e,r){return this.delegate={iterator:S(t),resultName:e,nextLoc:r},"next"===this.method&&(this.arg=void 0),f}},t}function m(t,e,r,n,i,o,a){try{var c=t[o](a),s=c.value}catch(l){return void r(l)}c.done?e(s):Promise.resolve(s).then(n,i)}function v(t,e){for(var r=0;r<e.length;r++){var n=e[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(t,j(n.key),n)}}function g(t,e){return g=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(t,e){return t.__proto__=e,t},g(t,e)}function b(t){var e=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(t){return!1}}();return function(){var r,n=C(t);if(e){var i=C(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return function(t,e){if(e&&("object"===d(e)||"function"==typeof e))return e;if(void 0!==e)throw new TypeError("Derived constructors may only return object or undefined");return w(t)}(this,r)}}function w(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function k(){k=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(r){e.forEach((function(e){e.kind===r&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var r=t.prototype;["method","field"].forEach((function(n){e.forEach((function(e){var i=e.placement;if(e.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?t:r;this.defineClassElement(o,e)}}),this)}),this)},defineClassElement:function(t,e){var r=e.descriptor;if("field"===e.kind){var n=e.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(t)}}Object.defineProperty(t,e.key,r)},decorateClass:function(t,e){var r=[],n=[],i={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,i)}),this),t.forEach((function(t){if(!x(t))return r.push(t);var e=this.decorateElement(t,i);r.push(e.element),r.push.apply(r,e.extras),n.push.apply(n,e.finishers)}),this),!e)return{elements:r,finishers:n};var o=this.decorateConstructor(r,e);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(t,e,r){var n=e[t.placement];if(!r&&-1!==n.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");n.push(t.key)},decorateElement:function(t,e){for(var r=[],n=[],i=t.decorators,o=i.length-1;o>=0;o--){var a=e[t.placement];a.splice(a.indexOf(t.key),1);var c=this.fromElementDescriptor(t),s=this.toElementFinisherExtras((0,i[o])(c)||c);t=s.element,this.addElementPlacement(t,e),s.finisher&&n.push(s.finisher);var l=s.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],e);r.push.apply(r,l)}}return{element:t,finishers:n,extras:r}},decorateConstructor:function(t,e){for(var r=[],n=e.length-1;n>=0;n--){var i=this.fromClassDescriptor(t),o=this.toClassDescriptor((0,e[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){t=o.elements;for(var a=0;a<t.length-1;a++)for(var c=a+1;c<t.length;c++)if(t[a].key===t[c].key&&t[a].placement===t[c].placement)throw new TypeError("Duplicated element ("+t[a].key+")")}}return{elements:t,finishers:r}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(e)||function(t,e){if(t){if("string"==typeof t)return S(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?S(t,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var r=j(t.key),n=String(t.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var o={kind:e,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=t.initializer),o},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:P(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var r=P(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:r}},runClassFinishers:function(t,e){for(var r=0;r<e.length;r++){var n=(0,e[r])(t);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");t=n}}return t},disallowProperty:function(t,e,r){if(void 0!==t[e])throw new TypeError(r+" can't have a ."+e+" property.")}};return t}function E(t){var e,r=j(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===t.kind?"field":"method",key:r,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(n.decorators=t.decorators),"field"===t.kind&&(n.initializer=t.value),n}function _(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function x(t){return t.decorators&&t.decorators.length}function O(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function P(t,e){var r=t[e];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+e+"' to be a function");return r}function j(t){var e=function(t,e){if("object"!==d(t)||null===t)return t;var r=t[Symbol.toPrimitive];if(void 0!==r){var n=r.call(t,e||"default");if("object"!==d(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"===d(e)?e:String(e)}function S(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,n=new Array(e);r<e;r++)n[r]=t[r];return n}function L(){return L="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(t,e,r){var n=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=C(t)););return t}(t,e);if(n){var i=Object.getOwnPropertyDescriptor(n,e);return i.get?i.get.call(arguments.length<3?t:r):i.value}},L.apply(this,arguments)}function C(t){return C=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(t){return t.__proto__||Object.getPrototypeOf(t)},C(t)}var A=function(t,e,r,n){var i=k();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=e((function(t){i.initializeInstanceElements(t,c.elements)}),r),c=i.decorateClass(function(t){for(var e=[],r=function(t){return"method"===t.kind&&t.key===o.key&&t.placement===o.placement},n=0;n<t.length;n++){var i,o=t[n];if("method"===o.kind&&(i=e.find(r)))if(O(o.descriptor)||O(i.descriptor)){if(x(o)||x(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(x(o)){if(x(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}_(o,i)}else e.push(o)}return e}(a.d.map(E)),t);return i.initializeClassElements(a.F,c.elements),i.runClassFinishers(a.F,c.finishers)}([(0,a.Mo)("hui-picture-card")],(function(t,e){var d,k,E=function(e){!function(t,e){if("function"!=typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),Object.defineProperty(t,"prototype",{writable:!1}),e&&g(t,e)}(a,e);var r,n,i,o=b(a);function a(){var e;!function(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}(this,a);for(var r=arguments.length,n=new Array(r),i=0;i<r;i++)n[i]=arguments[i];return e=o.call.apply(o,[this].concat(n)),t(w(e)),e}return r=a,n&&v(r.prototype,n),i&&v(r,i),Object.defineProperty(r,"prototype",{writable:!1}),r}(e);return{F:E,d:[{kind:"method",static:!0,key:"getConfigElement",value:(d=y().mark((function t(){return y().wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,Promise.all([r.e(6826),r.e(7426),r.e(3976),r.e(8348),r.e(392),r.e(4871),r.e(1691),r.e(5482),r.e(859)]).then(r.bind(r,859));case 2:return t.abrupt("return",document.createElement("hui-picture-card-editor"));case 3:case"end":return t.stop()}}),t)})),k=function(){var t=this,e=arguments;return new Promise((function(r,n){var i=d.apply(t,e);function o(t){m(i,r,n,o,a,"next",t)}function a(t){m(i,r,n,o,a,"throw",t)}o(void 0)}))},function(){return k.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"picture",image:"https://demo.home-assistant.io/stub_config/t-shirt-promo.png",tap_action:{action:"none"},hold_action:{action:"none"}}}},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"_config",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 5}},{kind:"method",key:"setConfig",value:function(t){if(!t||!t.image)throw new Error("Image required");this._config=t}},{kind:"method",key:"shouldUpdate",value:function(t){return 1!==t.size||!t.has("hass")||!t.get("hass")}},{kind:"method",key:"updated",value:function(t){if(L(C(E.prototype),"updated",this).call(this,t),this._config&&this.hass){var e=t.get("hass"),r=t.get("_config");e&&r&&e.themes===this.hass.themes&&r.theme===this._config.theme||(0,l.R)(this,this.hass.themes,this._config.theme)}}},{kind:"method",key:"render",value:function(){return this._config&&this.hass?(0,o.dy)(n||(n=p(["\n      <ha-card\n        @action=","\n        .actionHandler=","\n        tabindex=","\n        class=","\n      >\n        <img\n          alt=","\n          src=","\n        />\n      </ha-card>\n    "])),this._handleAction,(0,u.K)({hasHold:(0,h._)(this._config.hold_action),hasDoubleClick:(0,h._)(this._config.double_tap_action)}),(0,s.o)((0,h._)(this._config.tap_action)?"0":void 0),(0,c.$)({clickable:Boolean(this._config.tap_action||this._config.hold_action||this._config.double_tap_action)}),this._config.alt_text,this.hass.hassUrl(this._config.image)):o.Ld}},{kind:"get",static:!0,key:"styles",value:function(){return(0,o.iv)(i||(i=p(["\n      ha-card {\n        overflow: hidden;\n        height: 100%;\n      }\n\n      ha-card.clickable {\n        cursor: pointer;\n      }\n\n      img {\n        display: block;\n        width: 100%;\n      }\n    "])))}},{kind:"method",key:"_handleAction",value:function(t){(0,f.G)(this,this.hass,this._config,t.detail.action)}}]}}),o.oi)}}]);
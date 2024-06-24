/*! For license information please see 17479e2b.js.LICENSE.txt */
"use strict";(self.webpackChunkreact_frontend=self.webpackChunkreact_frontend||[]).push([[2662],{74376:function(e,t,r){var n,i=r(99307),o=r(39274),a=r(7599);function s(e){return s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},s(e)}function c(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,b(n.key),n)}}function l(e,t){return l=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},l(e,t)}function u(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=f(e);if(t){var i=f(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return function(e,t){if(t&&("object"===s(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return d(e)}(this,r)}}function d(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function f(e){return f=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},f(e)}function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!y(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=b(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function p(e){var t,r=b(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function m(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function y(e){return e.decorators&&e.decorators.length}function v(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function b(e){var t=function(e,t){if("object"!==s(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==s(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===s(t)?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}!function(e,t,r,n){var i=h();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(v(o.descriptor)||v(i.descriptor)){if(y(o)||y(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(y(o)){if(y(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}m(o,i)}else t.push(o)}return t}(a.d.map(p)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,r(46323).Mo)("ha-checkbox")],(function(e,t){var r=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&l(e,t)}(a,t);var r,n,i,o=u(a);function a(){var t;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,a);for(var r=arguments.length,n=new Array(r),i=0;i<r;i++)n[i]=arguments[i];return t=o.call.apply(o,[this].concat(n)),e(d(t)),t}return r=a,n&&c(r.prototype,n),i&&c(r,i),Object.defineProperty(r,"prototype",{writable:!1}),r}(t);return{F:r,d:[{kind:"field",static:!0,key:"styles",value:function(){return[o.W,(0,a.iv)(n||(e=["\n      :host {\n        --mdc-theme-secondary: var(--primary-color);\n      }\n    "],t||(t=e.slice(0)),n=Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))))];var e,t}}]}}),i.A)},92662:function(e,t,r){r.r(t);var n,i,o,a,s,c,l,u,d=r(7599),f=r(46323),h=r(228),p=r(1460),m=r(51183),y=r(38513),v=(r(68336),r(74376),r(37662),r(51520),function(e,t,r){return e.callWS(Object.assign({type:"shopping_list/items/update",item_id:t},r))}),g=r(49389),b=r(88423);function w(e){return w="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},w(e)}function k(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function E(){E=function(){return e};var e={},t=Object.prototype,r=t.hasOwnProperty,n=Object.defineProperty||function(e,t,r){e[t]=r.value},i="function"==typeof Symbol?Symbol:{},o=i.iterator||"@@iterator",a=i.asyncIterator||"@@asyncIterator",s=i.toStringTag||"@@toStringTag";function c(e,t,r){return Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}),e[t]}try{c({},"")}catch(D){c=function(e,t,r){return e[t]=r}}function l(e,t,r,i){var o=t&&t.prototype instanceof f?t:f,a=Object.create(o.prototype),s=new S(i||[]);return n(a,"_invoke",{value:_(e,r,s)}),a}function u(e,t,r){try{return{type:"normal",arg:e.call(t,r)}}catch(D){return{type:"throw",arg:D}}}e.wrap=l;var d={};function f(){}function h(){}function p(){}var m={};c(m,o,(function(){return this}));var y=Object.getPrototypeOf,v=y&&y(y(j([])));v&&v!==t&&r.call(v,o)&&(m=v);var g=p.prototype=f.prototype=Object.create(m);function b(e){["next","throw","return"].forEach((function(t){c(e,t,(function(e){return this._invoke(t,e)}))}))}function k(e,t){function i(n,o,a,s){var c=u(e[n],e,o);if("throw"!==c.type){var l=c.arg,d=l.value;return d&&"object"==w(d)&&r.call(d,"__await")?t.resolve(d.__await).then((function(e){i("next",e,a,s)}),(function(e){i("throw",e,a,s)})):t.resolve(d).then((function(e){l.value=e,a(l)}),(function(e){return i("throw",e,a,s)}))}s(c.arg)}var o;n(this,"_invoke",{value:function(e,r){function n(){return new t((function(t,n){i(e,r,t,n)}))}return o=o?o.then(n,n):n()}})}function _(e,t,r){var n="suspendedStart";return function(i,o){if("executing"===n)throw new Error("Generator is already running");if("completed"===n){if("throw"===i)throw o;return I()}for(r.method=i,r.arg=o;;){var a=r.delegate;if(a){var s=x(a,r);if(s){if(s===d)continue;return s}}if("next"===r.method)r.sent=r._sent=r.arg;else if("throw"===r.method){if("suspendedStart"===n)throw n="completed",r.arg;r.dispatchException(r.arg)}else"return"===r.method&&r.abrupt("return",r.arg);n="executing";var c=u(e,t,r);if("normal"===c.type){if(n=r.done?"completed":"suspendedYield",c.arg===d)continue;return{value:c.arg,done:r.done}}"throw"===c.type&&(n="completed",r.method="throw",r.arg=c.arg)}}}function x(e,t){var r=t.method,n=e.iterator[r];if(void 0===n)return t.delegate=null,"throw"===r&&e.iterator.return&&(t.method="return",t.arg=void 0,x(e,t),"throw"===t.method)||"return"!==r&&(t.method="throw",t.arg=new TypeError("The iterator does not provide a '"+r+"' method")),d;var i=u(n,e.iterator,t.arg);if("throw"===i.type)return t.method="throw",t.arg=i.arg,t.delegate=null,d;var o=i.arg;return o?o.done?(t[e.resultName]=o.value,t.next=e.nextLoc,"return"!==t.method&&(t.method="next",t.arg=void 0),t.delegate=null,d):o:(t.method="throw",t.arg=new TypeError("iterator result is not an object"),t.delegate=null,d)}function P(e){var t={tryLoc:e[0]};1 in e&&(t.catchLoc=e[1]),2 in e&&(t.finallyLoc=e[2],t.afterLoc=e[3]),this.tryEntries.push(t)}function O(e){var t=e.completion||{};t.type="normal",delete t.arg,e.completion=t}function S(e){this.tryEntries=[{tryLoc:"root"}],e.forEach(P,this),this.reset(!0)}function j(e){if(e){var t=e[o];if(t)return t.call(e);if("function"==typeof e.next)return e;if(!isNaN(e.length)){var n=-1,i=function t(){for(;++n<e.length;)if(r.call(e,n))return t.value=e[n],t.done=!1,t;return t.value=void 0,t.done=!0,t};return i.next=i}}return{next:I}}function I(){return{value:void 0,done:!0}}return h.prototype=p,n(g,"constructor",{value:p,configurable:!0}),n(p,"constructor",{value:h,configurable:!0}),h.displayName=c(p,s,"GeneratorFunction"),e.isGeneratorFunction=function(e){var t="function"==typeof e&&e.constructor;return!!t&&(t===h||"GeneratorFunction"===(t.displayName||t.name))},e.mark=function(e){return Object.setPrototypeOf?Object.setPrototypeOf(e,p):(e.__proto__=p,c(e,s,"GeneratorFunction")),e.prototype=Object.create(g),e},e.awrap=function(e){return{__await:e}},b(k.prototype),c(k.prototype,a,(function(){return this})),e.AsyncIterator=k,e.async=function(t,r,n,i,o){void 0===o&&(o=Promise);var a=new k(l(t,r,n,i),o);return e.isGeneratorFunction(r)?a:a.next().then((function(e){return e.done?e.value:a.next()}))},b(g),c(g,s,"Generator"),c(g,o,(function(){return this})),c(g,"toString",(function(){return"[object Generator]"})),e.keys=function(e){var t=Object(e),r=[];for(var n in t)r.push(n);return r.reverse(),function e(){for(;r.length;){var n=r.pop();if(n in t)return e.value=n,e.done=!1,e}return e.done=!0,e}},e.values=j,S.prototype={constructor:S,reset:function(e){if(this.prev=0,this.next=0,this.sent=this._sent=void 0,this.done=!1,this.delegate=null,this.method="next",this.arg=void 0,this.tryEntries.forEach(O),!e)for(var t in this)"t"===t.charAt(0)&&r.call(this,t)&&!isNaN(+t.slice(1))&&(this[t]=void 0)},stop:function(){this.done=!0;var e=this.tryEntries[0].completion;if("throw"===e.type)throw e.arg;return this.rval},dispatchException:function(e){if(this.done)throw e;var t=this;function n(r,n){return a.type="throw",a.arg=e,t.next=r,n&&(t.method="next",t.arg=void 0),!!n}for(var i=this.tryEntries.length-1;i>=0;--i){var o=this.tryEntries[i],a=o.completion;if("root"===o.tryLoc)return n("end");if(o.tryLoc<=this.prev){var s=r.call(o,"catchLoc"),c=r.call(o,"finallyLoc");if(s&&c){if(this.prev<o.catchLoc)return n(o.catchLoc,!0);if(this.prev<o.finallyLoc)return n(o.finallyLoc)}else if(s){if(this.prev<o.catchLoc)return n(o.catchLoc,!0)}else{if(!c)throw new Error("try statement without catch or finally");if(this.prev<o.finallyLoc)return n(o.finallyLoc)}}}},abrupt:function(e,t){for(var n=this.tryEntries.length-1;n>=0;--n){var i=this.tryEntries[n];if(i.tryLoc<=this.prev&&r.call(i,"finallyLoc")&&this.prev<i.finallyLoc){var o=i;break}}o&&("break"===e||"continue"===e)&&o.tryLoc<=t&&t<=o.finallyLoc&&(o=null);var a=o?o.completion:{};return a.type=e,a.arg=t,o?(this.method="next",this.next=o.finallyLoc,d):this.complete(a)},complete:function(e,t){if("throw"===e.type)throw e.arg;return"break"===e.type||"continue"===e.type?this.next=e.arg:"return"===e.type?(this.rval=this.arg=e.arg,this.method="return",this.next="end"):"normal"===e.type&&t&&(this.next=t),d},finish:function(e){for(var t=this.tryEntries.length-1;t>=0;--t){var r=this.tryEntries[t];if(r.finallyLoc===e)return this.complete(r.completion,r.afterLoc),O(r),d}},catch:function(e){for(var t=this.tryEntries.length-1;t>=0;--t){var r=this.tryEntries[t];if(r.tryLoc===e){var n=r.completion;if("throw"===n.type){var i=n.arg;O(r)}return i}}throw new Error("illegal catch attempt")},delegateYield:function(e,t,r){return this.delegate={iterator:j(e),resultName:t,nextLoc:r},"next"===this.method&&(this.arg=void 0),d}},e}function _(e,t,r,n,i,o,a){try{var s=e[o](a),c=s.value}catch(l){return void r(l)}s.done?t(c):Promise.resolve(c).then(n,i)}function x(e){return function(){var t=this,r=arguments;return new Promise((function(n,i){var o=e.apply(t,r);function a(e){_(o,n,i,a,s,"next",e)}function s(e){_(o,n,i,a,s,"throw",e)}a(void 0)}))}}function P(e,t){for(var r=0;r<t.length;r++){var n=t[r];n.enumerable=n.enumerable||!1,n.configurable=!0,"value"in n&&(n.writable=!0),Object.defineProperty(e,T(n.key),n)}}function O(e,t){return O=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},O(e,t)}function S(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var r,n=R(e);if(t){var i=R(this).constructor;r=Reflect.construct(n,arguments,i)}else r=n.apply(this,arguments);return function(e,t){if(t&&("object"===w(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return j(e)}(this,r)}}function j(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function I(){I=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(n){t.forEach((function(t){var i=t.placement;if(t.kind===n&&("static"===i||"prototype"===i)){var o="static"===i?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var n=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===n?void 0:n.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],n=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!A(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),n.push.apply(n,t.finishers)}),this),!t)return{elements:r,finishers:n};var o=this.decorateConstructor(r,t);return n.push.apply(n,o.finishers),o.finishers=n,o},addElementPlacement:function(e,t,r){var n=t[e.placement];if(!r&&-1!==n.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");n.push(e.key)},decorateElement:function(e,t){for(var r=[],n=[],i=e.decorators,o=i.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&n.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);r.push.apply(r,l)}}return{element:e,finishers:n,extras:r}},decorateConstructor:function(e,t){for(var r=[],n=t.length-1;n>=0;n--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[n])(i)||i);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=T(e.key),n=String(e.placement);if("static"!==n&&"prototype"!==n&&"own"!==n)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+n+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:n,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:V(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=V(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var n=(0,t[r])(e);if(void 0!==n){if("function"!=typeof n)throw new TypeError("Finishers must return a constructor.");e=n}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function D(e){var t,r=T(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var n={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(n.decorators=e.decorators),"field"===e.kind&&(n.initializer=e.value),n}function C(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function A(e){return e.decorators&&e.decorators.length}function H(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function V(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function T(e){var t=function(e,t){if("object"!==w(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==w(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===w(t)?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function L(){return L="undefined"!=typeof Reflect&&Reflect.get?Reflect.get.bind():function(e,t,r){var n=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=R(e)););return e}(e,t);if(n){var i=Object.getOwnPropertyDescriptor(n,t);return i.get?i.get.call(arguments.length<3?e:r):i.value}},L.apply(this,arguments)}function R(e){return R=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},R(e)}!function(e,t,r,n){var i=I();if(n)for(var o=0;o<n.length;o++)i=n[o](i);var a=t((function(e){i.initializeInstanceElements(e,s.elements)}),r),s=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},n=0;n<e.length;n++){var i,o=e[n];if("method"===o.kind&&(i=t.find(r)))if(H(o.descriptor)||H(i.descriptor)){if(A(o)||A(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(A(o)){if(A(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}C(o,i)}else t.push(o)}return t}(a.d.map(D)),e);i.initializeClassElements(a.F,s.elements),i.runClassFinishers(a.F,s.finishers)}([(0,f.Mo)("hui-shopping-list-card")],(function(e,t){var g,w,_,I,D=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&O(e,t)}(a,t);var r,n,i,o=S(a);function a(){var t;!function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,a);for(var r=arguments.length,n=new Array(r),i=0;i<r;i++)n[i]=arguments[i];return t=o.call.apply(o,[this].concat(n)),e(j(t)),t}return r=a,n&&P(r.prototype,n),i&&P(r,i),Object.defineProperty(r,"prototype",{writable:!1}),r}(t);return{F:D,d:[{kind:"method",static:!0,key:"getConfigElement",value:(I=x(E().mark((function e(){return E().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,r.e(7467).then(r.bind(r,97467));case 2:return e.abrupt("return",document.createElement("hui-shopping-list-card-editor"));case 3:case"end":return e.stop()}}),e)}))),function(){return I.apply(this,arguments)})},{kind:"method",static:!0,key:"getStubConfig",value:function(){return{type:"shopping-list"}}},{kind:"field",decorators:[(0,f.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,f.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,f.SB)()],key:"_uncheckedItems",value:void 0},{kind:"field",decorators:[(0,f.SB)()],key:"_checkedItems",value:void 0},{kind:"field",decorators:[(0,f.SB)()],key:"_reordering",value:function(){return!1}},{kind:"field",decorators:[(0,f.SB)()],key:"_renderEmptySortable",value:function(){return!1}},{kind:"field",key:"_sortable",value:void 0},{kind:"field",decorators:[(0,f.IO)("#sortable")],key:"_sortableEl",value:void 0},{kind:"method",key:"getCardSize",value:function(){return 3+(this._config&&this._config.title?2:0)}},{kind:"method",key:"setConfig",value:function(e){this._config=e,this._uncheckedItems=[],this._checkedItems=[]}},{kind:"method",key:"hassSubscribe",value:function(){var e=this;return this._fetchData(),[this.hass.connection.subscribeEvents((function(){return e._fetchData()}),"shopping_list_updated")]}},{kind:"method",key:"updated",value:function(e){if(L(R(D.prototype),"updated",this).call(this,e),this._config&&this.hass){var t=e.get("hass"),r=e.get("_config");(e.has("hass")&&(null==t?void 0:t.themes)!==this.hass.themes||e.has("_config")&&(null==r?void 0:r.theme)!==this._config.theme)&&(0,y.R)(this,this.hass.themes,this._config.theme)}}},{kind:"method",key:"render",value:function(){var e=this;return this._config&&this.hass?(0,d.dy)(n||(n=k(["\n      <ha-card\n        .header=","\n        class=",'\n      >\n        <div class="addRow">\n          <ha-svg-icon\n            class="addButton"\n            .path=',"\n            .title=","\n            @click=",'\n          >\n          </ha-svg-icon>\n          <ha-textfield\n            class="addBox"\n            .placeholder=',"\n            @keydown=",'\n          ></ha-textfield>\n          <ha-svg-icon\n            class="reorderButton"\n            .path=',"\n            .title=","\n            @click=","\n          >\n          </ha-svg-icon>\n        </div>\n        ","\n        ","\n      </ha-card>\n    "])),this._config.title,(0,h.$)({"has-header":"title"in this._config}),"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",this.hass.localize("ui.panel.lovelace.cards.shopping-list.add_item"),this._addItem,this.hass.localize("ui.panel.lovelace.cards.shopping-list.add_item"),this._addKeyPress,"M18 21L14 17H17V7H14L18 3L22 7H19V17H22M2 19V17H12V19M2 13V11H9V13M2 7V5H6V7H2Z",this.hass.localize("ui.panel.lovelace.cards.shopping-list.reorder_items"),this._toggleReorder,this._reordering?(0,d.dy)(i||(i=k(['\n              <div id="sortable">\n                ',"\n              </div>\n            "])),(0,p.l)([this._uncheckedItems,this._renderEmptySortable],(function(){return e._renderEmptySortable?"":e._renderItems(e._uncheckedItems)}))):this._renderItems(this._uncheckedItems),this._checkedItems.length>0?(0,d.dy)(o||(o=k(['\n              <div class="divider"></div>\n              <div class="checked">\n                <span>\n                  ','\n                </span>\n                <ha-svg-icon\n                  class="clearall"\n                  tabindex="0"\n                  .path=',"\n                  .title=","\n                  @click=","\n                >\n                </ha-svg-icon>\n              </div>\n              ","\n            "])),this.hass.localize("ui.panel.lovelace.cards.shopping-list.checked_items"),"M5,13H19V11H5M3,17H17V15H3M7,7V9H21V7",this.hass.localize("ui.panel.lovelace.cards.shopping-list.clear_items"),this._clearItems,(0,m.r)(this._checkedItems,(function(e){return e.id}),(function(t){return(0,d.dy)(a||(a=k(['\n                    <div class="editRow">\n                      <ha-checkbox\n                        tabindex="0"\n                        .checked=',"\n                        .itemId=","\n                        @change=",'\n                      ></ha-checkbox>\n                      <ha-textfield\n                        class="item"\n                        .value=',"\n                        .itemId=","\n                        @change=","\n                      ></ha-textfield>\n                    </div>\n                  "])),t.complete,t.id,e._completeItem,t.name,t.id,e._saveEdit)}))):""):d.Ld}},{kind:"method",key:"_renderItems",value:function(e){var t=this;return(0,d.dy)(s||(s=k(["\n      ","\n    "])),(0,m.r)(e,(function(e){return e.id}),(function(e){return(0,d.dy)(c||(c=k(['\n            <div class="editRow" item-id=','>\n              <ha-checkbox\n                tabindex="0"\n                .checked=',"\n                .itemId=","\n                @change=",'\n              ></ha-checkbox>\n              <ha-textfield\n                class="item"\n                .value=',"\n                .itemId=","\n                @change=","\n              ></ha-textfield>\n              ","\n            </div>\n          "])),e.id,e.complete,e.id,t._completeItem,e.name,e.id,t._saveEdit,t._reordering?(0,d.dy)(l||(l=k(["\n                    <ha-svg-icon\n                      .title=",'\n                      class="reorderButton"\n                      .path=',"\n                    >\n                    </ha-svg-icon>\n                  "])),t.hass.localize("ui.panel.lovelace.cards.shopping-list.drag_and_drop"),"M7,19V17H9V19H7M11,19V17H13V19H11M15,19V17H17V19H15M7,15V13H9V15H7M11,15V13H13V15H11M15,15V13H17V15H15M7,11V9H9V11H7M11,11V9H13V11H11M15,11V9H17V11H15M7,7V5H9V7H7M11,7V5H13V7H11M15,7V5H17V7H15Z"):"")})))}},{kind:"method",key:"_fetchData",value:(_=x(E().mark((function e(){var t,r,n,i;return E().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(this.hass){e.next=2;break}return e.abrupt("return");case 2:return t=[],r=[],e.next=6,this.hass.callWS({type:"shopping_list/items"});case 6:for(i in n=e.sent)n[i].complete?t.push(n[i]):r.push(n[i]);this._checkedItems=t,this._uncheckedItems=r;case 10:case"end":return e.stop()}}),e,this)}))),function(){return _.apply(this,arguments)})},{kind:"method",key:"_completeItem",value:function(e){var t=this;v(this.hass,e.target.itemId,{complete:e.target.checked}).catch((function(){return t._fetchData()}))}},{kind:"method",key:"_saveEdit",value:function(e){var t,r,n=this;e.target.value?v(this.hass,e.target.itemId,{name:e.target.value}).catch((function(){return n._fetchData()})):(t=this.hass,r=e.target.itemId,t.callWS({type:"shopping_list/items/remove",item_id:r})).catch((function(){return n._fetchData()})),e.target.blur()}},{kind:"method",key:"_clearItems",value:function(){var e,t=this;this.hass&&(e=this.hass,e.callWS({type:"shopping_list/items/clear"})).catch((function(){return t._fetchData()}))}},{kind:"get",key:"_newItem",value:function(){return this.shadowRoot.querySelector(".addBox")}},{kind:"method",key:"_addItem",value:function(e){var t,r,n=this,i=this._newItem;i.value.length>0&&(t=this.hass,r=i.value,t.callWS({type:"shopping_list/items/add",name:r})).catch((function(){return n._fetchData()})),i.value="",e&&i.focus()}},{kind:"method",key:"_addKeyPress",value:function(e){13===e.keyCode&&this._addItem(null)}},{kind:"method",key:"_toggleReorder",value:(w=x(E().mark((function e(){var t;return E().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return this._reordering=!this._reordering,e.next=3,this.updateComplete;case 3:this._reordering?this._createSortable():(null===(t=this._sortable)||void 0===t||t.destroy(),this._sortable=void 0);case 4:case"end":return e.stop()}}),e,this)}))),function(){return w.apply(this,arguments)})},{kind:"method",key:"_createSortable",value:(g=x(E().mark((function e(){var t,r,n=this;return E().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,b.F)();case 2:t=e.sent,r=this._sortableEl,this._sortable=new t(r,{animation:150,fallbackClass:"sortable-fallback",dataIdAttr:"item-id",handle:"ha-svg-icon",onEnd:function(){var e=x(E().mark((function e(t){return E().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(void 0!==t.newIndex&&void 0!==t.oldIndex){e.next=2;break}return e.abrupt("return");case 2:return t.oldIndex!==t.newIndex&&((i=n.hass,o=n._sortable.toArray(),i.callWS({type:"shopping_list/items/reorder",item_ids:o})).catch((function(){return n._fetchData()})),n._uncheckedItems.splice(t.newIndex,0,n._uncheckedItems.splice(t.oldIndex,1)[0])),n._renderEmptySortable=!0,e.next=6,n.updateComplete;case 6:for(;null!=r&&r.lastElementChild;)r.removeChild(r.lastElementChild);n._renderEmptySortable=!1;case 8:case"end":return e.stop()}var i,o}),e)})));return function(t){return e.apply(this,arguments)}}()});case 5:case"end":return e.stop()}}),e,this)}))),function(){return g.apply(this,arguments)})},{kind:"get",static:!0,key:"styles",value:function(){return(0,d.iv)(u||(u=k(["\n      ha-card {\n        padding: 16px;\n        height: 100%;\n        box-sizing: border-box;\n      }\n\n      .has-header {\n        padding-top: 0;\n      }\n\n      .editRow,\n      .addRow,\n      .checked {\n        display: flex;\n        flex-direction: row;\n        align-items: center;\n      }\n\n      .item {\n        margin-top: 8px;\n      }\n\n      .addButton {\n        padding-right: 16px;\n        padding-inline-end: 16px;\n        cursor: pointer;\n        direction: var(--direction);\n      }\n\n      .reorderButton {\n        padding-left: 16px;\n        padding-inline-start: 16px;\n        cursor: pointer;\n        direction: var(--direction);\n      }\n\n      ha-checkbox {\n        margin-left: -12px;\n        margin-inline-start: -12px;\n        direction: var(--direction);\n      }\n\n      ha-textfield {\n        flex-grow: 1;\n      }\n\n      .checked {\n        margin: 12px 0;\n        justify-content: space-between;\n      }\n\n      .checked span {\n        color: var(--primary-text-color);\n        font-weight: 500;\n      }\n\n      .divider {\n        height: 1px;\n        background-color: var(--divider-color);\n        margin: 10px 0;\n      }\n\n      .clearall {\n        cursor: pointer;\n      }\n    "])))}}]}}),(0,g.f)(d.oi))}}]);
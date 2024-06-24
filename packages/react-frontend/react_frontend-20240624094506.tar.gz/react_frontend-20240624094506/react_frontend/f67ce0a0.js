"use strict";(self.webpackChunkreact_frontend=self.webpackChunkreact_frontend||[]).push([[1480],{81480:function(e,t,n){function r(e,t,n){return(t=d(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function i(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&o(e,t)}function o(e,t){return o=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},o(e,t)}function c(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=a(e);if(t){var i=a(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return function(e,t){if(t&&("object"===v(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e)}(this,n)}}function a(e){return a=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},a(e)}function s(e){return function(e){if(Array.isArray(e))return u(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||function(e,t){if(!e)return;if("string"==typeof e)return u(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return u(e,t)}(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function u(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function h(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function l(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,d(r.key),r)}}function f(e,t,n){return t&&l(e.prototype,t),n&&l(e,n),Object.defineProperty(e,"prototype",{writable:!1}),e}function d(e){var t=function(e,t){if("object"!==v(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==v(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===v(t)?t:String(t)}function v(e){return v="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},v(e)}function g(e){return Array.isArray?Array.isArray(e):"[object Array]"===L(e)}n.d(t,{Z:function(){return ve}});var y=1/0;function p(e){return null==e?"":function(e){if("string"==typeof e)return e;var t=e+"";return"0"==t&&1/e==-y?"-0":t}(e)}function m(e){return"string"==typeof e}function k(e){return"number"==typeof e}function M(e){return!0===e||!1===e||function(e){return b(e)&&null!==e}(e)&&"[object Boolean]"==L(e)}function b(e){return"object"===v(e)}function x(e){return null!=e}function w(e){return!e.trim().length}function L(e){return null==e?void 0===e?"[object Undefined]":"[object Null]":Object.prototype.toString.call(e)}var _=function(e){return"Missing ".concat(e," property in key")},S=function(e){return"Property 'weight' in key '".concat(e,"' must be a positive integer")},C=Object.prototype.hasOwnProperty,A=function(){function e(t){var n=this;h(this,e),this._keys=[],this._keyMap={};var r=0;t.forEach((function(e){var t=I(e);r+=t.weight,n._keys.push(t),n._keyMap[t.id]=t,r+=t.weight})),this._keys.forEach((function(e){e.weight/=r}))}return f(e,[{key:"get",value:function(e){return this._keyMap[e]}},{key:"keys",value:function(){return this._keys}},{key:"toJSON",value:function(){return JSON.stringify(this._keys)}}]),e}();function I(e){var t=null,n=null,r=null,i=1,o=null;if(m(e)||g(e))r=e,t=O(e),n=E(e);else{if(!C.call(e,"name"))throw new Error(_("name"));var c=e.name;if(r=c,C.call(e,"weight")&&(i=e.weight)<=0)throw new Error(S(c));t=O(c),n=E(c),o=e.getFn}return{path:t,id:n,weight:i,src:r,getFn:o}}function O(e){return g(e)?e:e.split(".")}function E(e){return g(e)?e.join("."):e}var j={useExtendedSearch:!1,getFn:function(e,t){var n=[],r=!1;return function e(t,i,o){if(x(t))if(i[o]){var c=t[i[o]];if(!x(c))return;if(o===i.length-1&&(m(c)||k(c)||M(c)))n.push(p(c));else if(g(c)){r=!0;for(var a=0,s=c.length;a<s;a+=1)e(c[a],i,o+1)}else i.length&&e(c,i,o+1)}else n.push(t)}(e,m(t)?t.split("."):t,0),r?n:n[0]},ignoreLocation:!1,ignoreFieldNorm:!1,fieldNormWeight:1},$=Object.assign({},{isCaseSensitive:!1,includeScore:!1,keys:[],shouldSort:!0,sortFn:function(e,t){return e.score===t.score?e.idx<t.idx?-1:1:e.score<t.score?-1:1}},{includeMatches:!1,findAllMatches:!1,minMatchCharLength:1},{location:0,threshold:.6,distance:100},j),F=/[^ ]+/g;var R=function(){function e(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},n=t.getFn,r=void 0===n?$.getFn:n,i=t.fieldNormWeight,o=void 0===i?$.fieldNormWeight:i;h(this,e),this.norm=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:1,t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:3,n=new Map,r=Math.pow(10,t);return{get:function(t){var i=t.match(F).length;if(n.has(i))return n.get(i);var o=1/Math.pow(i,.5*e),c=parseFloat(Math.round(o*r)/r);return n.set(i,c),c},clear:function(){n.clear()}}}(o,3),this.getFn=r,this.isCreated=!1,this.setIndexRecords()}return f(e,[{key:"setSources",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.docs=e}},{key:"setIndexRecords",value:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.records=e}},{key:"setKeys",value:function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];this.keys=t,this._keysMap={},t.forEach((function(t,n){e._keysMap[t.id]=n}))}},{key:"create",value:function(){var e=this;!this.isCreated&&this.docs.length&&(this.isCreated=!0,m(this.docs[0])?this.docs.forEach((function(t,n){e._addString(t,n)})):this.docs.forEach((function(t,n){e._addObject(t,n)})),this.norm.clear())}},{key:"add",value:function(e){var t=this.size();m(e)?this._addString(e,t):this._addObject(e,t)}},{key:"removeAt",value:function(e){this.records.splice(e,1);for(var t=e,n=this.size();t<n;t+=1)this.records[t].i-=1}},{key:"getValueForItemAtKeyId",value:function(e,t){return e[this._keysMap[t]]}},{key:"size",value:function(){return this.records.length}},{key:"_addString",value:function(e,t){if(x(e)&&!w(e)){var n={v:e,i:t,n:this.norm.get(e)};this.records.push(n)}}},{key:"_addObject",value:function(e,t){var n=this,r={i:t,$:{}};this.keys.forEach((function(t,i){var o=t.getFn?t.getFn(e):n.getFn(e,t.path);if(x(o))if(g(o)){for(var c=[],a=[{nestedArrIndex:-1,value:o}];a.length;){var s=a.pop(),u=s.nestedArrIndex,h=s.value;if(x(h))if(m(h)&&!w(h)){var l={v:h,i:u,n:n.norm.get(h)};c.push(l)}else g(h)&&h.forEach((function(e,t){a.push({nestedArrIndex:t,value:e})}))}r.$[i]=c}else if(m(o)&&!w(o)){var f={v:o,n:n.norm.get(o)};r.$[i]=f}})),this.records.push(r)}},{key:"toJSON",value:function(){return{keys:this.keys,records:this.records}}}]),e}();function N(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=n.getFn,i=void 0===r?$.getFn:r,o=n.fieldNormWeight,c=void 0===o?$.fieldNormWeight:o,a=new R({getFn:i,fieldNormWeight:c});return a.setKeys(e.map(I)),a.setSources(t),a.create(),a}function P(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=t.errors,r=void 0===n?0:n,i=t.currentLocation,o=void 0===i?0:i,c=t.expectedLocation,a=void 0===c?0:c,s=t.distance,u=void 0===s?$.distance:s,h=t.ignoreLocation,l=void 0===h?$.ignoreLocation:h,f=r/e.length;if(l)return f;var d=Math.abs(a-o);return u?f+d/u:d?1:f}var W=32;function z(e,t,n){var r=arguments.length>3&&void 0!==arguments[3]?arguments[3]:{},i=r.location,o=void 0===i?$.location:i,c=r.distance,a=void 0===c?$.distance:c,s=r.threshold,u=void 0===s?$.threshold:s,h=r.findAllMatches,l=void 0===h?$.findAllMatches:h,f=r.minMatchCharLength,d=void 0===f?$.minMatchCharLength:f,v=r.includeMatches,g=void 0===v?$.includeMatches:v,y=r.ignoreLocation,p=void 0===y?$.ignoreLocation:y;if(t.length>W)throw new Error("Pattern length exceeds max of ".concat(W,"."));for(var m,k=t.length,M=e.length,b=Math.max(0,Math.min(o,M)),x=u,w=b,L=d>1||g,_=L?Array(M):[];(m=e.indexOf(t,w))>-1;){var S=P(t,{currentLocation:m,expectedLocation:b,distance:a,ignoreLocation:p});if(x=Math.min(S,x),w=m+k,L)for(var C=0;C<k;)_[m+C]=1,C+=1}w=-1;for(var A=[],I=1,O=k+M,E=1<<k-1,j=0;j<k;j+=1){for(var F=0,R=O;F<R;){P(t,{errors:j,currentLocation:b+R,expectedLocation:b,distance:a,ignoreLocation:p})<=x?F=R:O=R,R=Math.floor((O-F)/2+F)}O=R;var N=Math.max(1,b-R+1),z=l?M:Math.min(b+R,M)+k,K=Array(z+2);K[z+1]=(1<<j)-1;for(var T=z;T>=N;T-=1){var q=T-1,B=n[e.charAt(q)];if(L&&(_[q]=+!!B),K[T]=(K[T+1]<<1|1)&B,j&&(K[T]|=(A[T+1]|A[T])<<1|1|A[T+1]),K[T]&E&&(I=P(t,{errors:j,currentLocation:q,expectedLocation:b,distance:a,ignoreLocation:p}))<=x){if(x=I,(w=q)<=b)break;N=Math.max(1,2*b-w)}}if(P(t,{errors:j+1,currentLocation:b,expectedLocation:b,distance:a,ignoreLocation:p})>x)break;A=K}var J={isMatch:w>=0,score:Math.max(.001,I)};if(L){var U=function(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[],t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:$.minMatchCharLength,n=[],r=-1,i=-1,o=0,c=e.length;o<c;o+=1){var a=e[o];a&&-1===r?r=o:a||-1===r||((i=o-1)-r+1>=t&&n.push([r,i]),r=-1)}return e[o-1]&&o-r>=t&&n.push([r,o-1]),n}(_,d);U.length?g&&(J.indices=U):J.isMatch=!1}return J}function K(e){for(var t={},n=0,r=e.length;n<r;n+=1){var i=e.charAt(n);t[i]=(t[i]||0)|1<<r-n-1}return t}var T=function(){function e(t){var n=this,r=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},i=r.location,o=void 0===i?$.location:i,c=r.threshold,a=void 0===c?$.threshold:c,s=r.distance,u=void 0===s?$.distance:s,l=r.includeMatches,f=void 0===l?$.includeMatches:l,d=r.findAllMatches,v=void 0===d?$.findAllMatches:d,g=r.minMatchCharLength,y=void 0===g?$.minMatchCharLength:g,p=r.isCaseSensitive,m=void 0===p?$.isCaseSensitive:p,k=r.ignoreLocation,M=void 0===k?$.ignoreLocation:k;if(h(this,e),this.options={location:o,threshold:a,distance:u,includeMatches:f,findAllMatches:v,minMatchCharLength:y,isCaseSensitive:m,ignoreLocation:M},this.pattern=m?t:t.toLowerCase(),this.chunks=[],this.pattern.length){var b=function(e,t){n.chunks.push({pattern:e,alphabet:K(e),startIndex:t})},x=this.pattern.length;if(x>W){for(var w=0,L=x%W,_=x-L;w<_;)b(this.pattern.substr(w,W),w),w+=W;if(L){var S=x-W;b(this.pattern.substr(S),S)}}else b(this.pattern,0)}}return f(e,[{key:"searchIn",value:function(e){var t=this.options,n=t.isCaseSensitive,r=t.includeMatches;if(n||(e=e.toLowerCase()),this.pattern===e){var i={isMatch:!0,score:0};return r&&(i.indices=[[0,e.length-1]]),i}var o=this.options,c=o.location,a=o.distance,u=o.threshold,h=o.findAllMatches,l=o.minMatchCharLength,f=o.ignoreLocation,d=[],v=0,g=!1;this.chunks.forEach((function(t){var n=t.pattern,i=t.alphabet,o=t.startIndex,y=z(e,n,i,{location:c+o,distance:a,threshold:u,findAllMatches:h,minMatchCharLength:l,includeMatches:r,ignoreLocation:f}),p=y.isMatch,m=y.score,k=y.indices;p&&(g=!0),v+=m,p&&k&&(d=[].concat(s(d),s(k)))}));var y={isMatch:g,score:g?v/this.chunks.length:1};return g&&r&&(y.indices=d),y}}]),e}(),q=function(){function e(t){h(this,e),this.pattern=t}return f(e,[{key:"search",value:function(){}}],[{key:"isMultiMatch",value:function(e){return B(e,this.multiRegex)}},{key:"isSingleMatch",value:function(e){return B(e,this.singleRegex)}}]),e}();function B(e,t){var n=e.match(t);return n?n[1]:null}var J=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=e===this.pattern;return{isMatch:t,score:t?0:1,indices:[0,this.pattern.length-1]}}}],[{key:"type",get:function(){return"exact"}},{key:"multiRegex",get:function(){return/^="(.*)"$/}},{key:"singleRegex",get:function(){return/^=(.*)$/}}]),n}(q),U=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=-1===e.indexOf(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-exact"}},{key:"multiRegex",get:function(){return/^!"(.*)"$/}},{key:"singleRegex",get:function(){return/^!(.*)$/}}]),n}(q),V=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=e.startsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,this.pattern.length-1]}}}],[{key:"type",get:function(){return"prefix-exact"}},{key:"multiRegex",get:function(){return/^\^"(.*)"$/}},{key:"singleRegex",get:function(){return/^\^(.*)$/}}]),n}(q),D=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=!e.startsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-prefix-exact"}},{key:"multiRegex",get:function(){return/^!\^"(.*)"$/}},{key:"singleRegex",get:function(){return/^!\^(.*)$/}}]),n}(q),Q=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=e.endsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[e.length-this.pattern.length,e.length-1]}}}],[{key:"type",get:function(){return"suffix-exact"}},{key:"multiRegex",get:function(){return/^"(.*)"\$$/}},{key:"singleRegex",get:function(){return/^(.*)\$$/}}]),n}(q),Z=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){var t=!e.endsWith(this.pattern);return{isMatch:t,score:t?0:1,indices:[0,e.length-1]}}}],[{key:"type",get:function(){return"inverse-suffix-exact"}},{key:"multiRegex",get:function(){return/^!"(.*)"\$$/}},{key:"singleRegex",get:function(){return/^!(.*)\$$/}}]),n}(q),G=function(e){i(n,e);var t=c(n);function n(e){var r,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},o=i.location,c=void 0===o?$.location:o,a=i.threshold,s=void 0===a?$.threshold:a,u=i.distance,l=void 0===u?$.distance:u,f=i.includeMatches,d=void 0===f?$.includeMatches:f,v=i.findAllMatches,g=void 0===v?$.findAllMatches:v,y=i.minMatchCharLength,p=void 0===y?$.minMatchCharLength:y,m=i.isCaseSensitive,k=void 0===m?$.isCaseSensitive:m,M=i.ignoreLocation,b=void 0===M?$.ignoreLocation:M;return h(this,n),(r=t.call(this,e))._bitapSearch=new T(e,{location:c,threshold:s,distance:l,includeMatches:d,findAllMatches:g,minMatchCharLength:p,isCaseSensitive:k,ignoreLocation:b}),r}return f(n,[{key:"search",value:function(e){return this._bitapSearch.searchIn(e)}}],[{key:"type",get:function(){return"fuzzy"}},{key:"multiRegex",get:function(){return/^"(.*)"$/}},{key:"singleRegex",get:function(){return/^(.*)$/}}]),n}(q),H=function(e){i(n,e);var t=c(n);function n(e){return h(this,n),t.call(this,e)}return f(n,[{key:"search",value:function(e){for(var t,n=0,r=[],i=this.pattern.length;(t=e.indexOf(this.pattern,n))>-1;)n=t+i,r.push([t,n-1]);var o=!!r.length;return{isMatch:o,score:o?0:1,indices:r}}}],[{key:"type",get:function(){return"include"}},{key:"multiRegex",get:function(){return/^'"(.*)"$/}},{key:"singleRegex",get:function(){return/^'(.*)$/}}]),n}(q),X=[J,H,V,D,Z,Q,U,G],Y=X.length,ee=/ +(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/;var te=new Set([G.type,H.type]),ne=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},r=n.isCaseSensitive,i=void 0===r?$.isCaseSensitive:r,o=n.includeMatches,c=void 0===o?$.includeMatches:o,a=n.minMatchCharLength,s=void 0===a?$.minMatchCharLength:a,u=n.ignoreLocation,l=void 0===u?$.ignoreLocation:u,f=n.findAllMatches,d=void 0===f?$.findAllMatches:f,v=n.location,g=void 0===v?$.location:v,y=n.threshold,p=void 0===y?$.threshold:y,m=n.distance,k=void 0===m?$.distance:m;h(this,e),this.query=null,this.options={isCaseSensitive:i,includeMatches:c,minMatchCharLength:s,findAllMatches:d,ignoreLocation:l,location:g,threshold:p,distance:k},this.pattern=i?t:t.toLowerCase(),this.query=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{};return e.split("|").map((function(e){for(var n=e.trim().split(ee).filter((function(e){return e&&!!e.trim()})),r=[],i=0,o=n.length;i<o;i+=1){for(var c=n[i],a=!1,s=-1;!a&&++s<Y;){var u=X[s],h=u.isMultiMatch(c);h&&(r.push(new u(h,t)),a=!0)}if(!a)for(s=-1;++s<Y;){var l=X[s],f=l.isSingleMatch(c);if(f){r.push(new l(f,t));break}}}return r}))}(this.pattern,this.options)}return f(e,[{key:"searchIn",value:function(e){var t=this.query;if(!t)return{isMatch:!1,score:1};var n=this.options,r=n.includeMatches;e=n.isCaseSensitive?e:e.toLowerCase();for(var i=0,o=[],c=0,a=0,u=t.length;a<u;a+=1){var h=t[a];o.length=0,i=0;for(var l=0,f=h.length;l<f;l+=1){var d=h[l],v=d.search(e),g=v.isMatch,y=v.indices,p=v.score;if(!g){c=0,i=0,o.length=0;break}if(i+=1,c+=p,r){var m=d.constructor.type;te.has(m)?o=[].concat(s(o),s(y)):o.push(y)}}if(i){var k={isMatch:!0,score:c/i};return r&&(k.indices=o),k}}return{isMatch:!1,score:1}}}],[{key:"condition",value:function(e,t){return t.useExtendedSearch}}]),e}(),re=[];function ie(e,t){for(var n=0,r=re.length;n<r;n+=1){var i=re[n];if(i.condition(e,t))return new i(e,t)}return new T(e,t)}var oe="$and",ce="$or",ae="$path",se="$val",ue=function(e){return!(!e[oe]&&!e[ce])},he=function(e){return r({},oe,Object.keys(e).map((function(t){return r({},t,e[t])})))};function le(e,t){var n=(arguments.length>2&&void 0!==arguments[2]?arguments[2]:{}).auto,r=void 0===n||n;return ue(e)||(e=he(e)),function e(n){var i=Object.keys(n),o=function(e){return!!e[ae]}(n);if(!o&&i.length>1&&!ue(n))return e(he(n));if(function(e){return!g(e)&&b(e)&&!ue(e)}(n)){var c=o?n[ae]:i[0],a=o?n[se]:n[c];if(!m(a))throw new Error(function(e){return"Invalid value for key ".concat(e)}(c));var s={keyId:E(c),pattern:a};return r&&(s.searcher=ie(a,t)),s}var u={children:[],operator:i[0]};return i.forEach((function(t){var r=n[t];g(r)&&r.forEach((function(t){u.children.push(e(t))}))})),u}(e)}function fe(e,t){var n=e.matches;t.matches=[],x(n)&&n.forEach((function(e){if(x(e.indices)&&e.indices.length){var n={indices:e.indices,value:e.value};e.key&&(n.key=e.key.src),e.idx>-1&&(n.refIndex=e.idx),t.matches.push(n)}}))}function de(e,t){t.score=e.score}var ve=function(){function e(t){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},r=arguments.length>2?arguments[2]:void 0;h(this,e),this.options=Object.assign({},$,n),this.options.useExtendedSearch,this._keyStore=new A(this.options.keys),this.setCollection(t,r)}return f(e,[{key:"setCollection",value:function(e,t){if(this._docs=e,t&&!(t instanceof R))throw new Error("Incorrect 'index' type");this._myIndex=t||N(this.options.keys,this._docs,{getFn:this.options.getFn,fieldNormWeight:this.options.fieldNormWeight})}},{key:"add",value:function(e){x(e)&&(this._docs.push(e),this._myIndex.add(e))}},{key:"remove",value:function(){for(var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:function(){return!1},t=[],n=0,r=this._docs.length;n<r;n+=1){var i=this._docs[n];e(i,n)&&(this.removeAt(n),n-=1,r-=1,t.push(i))}return t}},{key:"removeAt",value:function(e){this._docs.splice(e,1),this._myIndex.removeAt(e)}},{key:"getIndex",value:function(){return this._myIndex}},{key:"search",value:function(e){var t=(arguments.length>1&&void 0!==arguments[1]?arguments[1]:{}).limit,n=void 0===t?-1:t,r=this.options,i=r.includeMatches,o=r.includeScore,c=r.shouldSort,a=r.sortFn,s=r.ignoreFieldNorm,u=m(e)?m(this._docs[0])?this._searchStringList(e):this._searchObjectList(e):this._searchLogical(e);return function(e,t){var n=t.ignoreFieldNorm,r=void 0===n?$.ignoreFieldNorm:n;e.forEach((function(e){var t=1;e.matches.forEach((function(e){var n=e.key,i=e.norm,o=e.score,c=n?n.weight:null;t*=Math.pow(0===o&&c?Number.EPSILON:o,(c||1)*(r?1:i))})),e.score=t}))}(u,{ignoreFieldNorm:s}),c&&u.sort(a),k(n)&&n>-1&&(u=u.slice(0,n)),function(e,t){var n=arguments.length>2&&void 0!==arguments[2]?arguments[2]:{},r=n.includeMatches,i=void 0===r?$.includeMatches:r,o=n.includeScore,c=void 0===o?$.includeScore:o,a=[];return i&&a.push(fe),c&&a.push(de),e.map((function(e){var n=e.idx,r={item:t[n],refIndex:n};return a.length&&a.forEach((function(t){t(e,r)})),r}))}(u,this._docs,{includeMatches:i,includeScore:o})}},{key:"_searchStringList",value:function(e){var t=ie(e,this.options),n=this._myIndex.records,r=[];return n.forEach((function(e){var n=e.v,i=e.i,o=e.n;if(x(n)){var c=t.searchIn(n),a=c.isMatch,s=c.score,u=c.indices;a&&r.push({item:n,idx:i,matches:[{score:s,value:n,norm:o,indices:u}]})}})),r}},{key:"_searchLogical",value:function(e){var t=this,n=le(e,this.options),r=function e(n,r,i){if(!n.children){var o=n.keyId,c=n.searcher,a=t._findMatches({key:t._keyStore.get(o),value:t._myIndex.getValueForItemAtKeyId(r,o),searcher:c});return a&&a.length?[{idx:i,item:r,matches:a}]:[]}for(var u=[],h=0,l=n.children.length;h<l;h+=1){var f=e(n.children[h],r,i);if(f.length)u.push.apply(u,s(f));else if(n.operator===oe)return[]}return u},i=this._myIndex.records,o={},c=[];return i.forEach((function(e){var t=e.$,i=e.i;if(x(t)){var a=r(n,t,i);a.length&&(o[i]||(o[i]={idx:i,item:t,matches:[]},c.push(o[i])),a.forEach((function(e){var t,n=e.matches;(t=o[i].matches).push.apply(t,s(n))})))}})),c}},{key:"_searchObjectList",value:function(e){var t=this,n=ie(e,this.options),r=this._myIndex,i=r.keys,o=r.records,c=[];return o.forEach((function(e){var r=e.$,o=e.i;if(x(r)){var a=[];i.forEach((function(e,i){a.push.apply(a,s(t._findMatches({key:e,value:r[i],searcher:n})))})),a.length&&c.push({idx:o,item:r,matches:a})}})),c}},{key:"_findMatches",value:function(e){var t=e.key,n=e.value,r=e.searcher;if(!x(n))return[];var i=[];if(g(n))n.forEach((function(e){var n=e.v,o=e.i,c=e.n;if(x(n)){var a=r.searchIn(n),s=a.isMatch,u=a.score,h=a.indices;s&&i.push({score:u,key:t,value:n,idx:o,norm:c,indices:h})}}));else{var o=n.v,c=n.n,a=r.searchIn(o),s=a.isMatch,u=a.score,h=a.indices;s&&i.push({score:u,key:t,value:o,norm:c,indices:h})}return i}}]),e}();ve.version="6.6.2",ve.createIndex=N,ve.parseIndex=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{},n=t.getFn,r=void 0===n?$.getFn:n,i=t.fieldNormWeight,o=void 0===i?$.fieldNormWeight:i,c=e.keys,a=e.records,s=new R({getFn:r,fieldNormWeight:o});return s.setKeys(c),s.setIndexRecords(a),s},ve.config=$,ve.parseQuery=le,function(){re.push.apply(re,arguments)}(ne)}}]);
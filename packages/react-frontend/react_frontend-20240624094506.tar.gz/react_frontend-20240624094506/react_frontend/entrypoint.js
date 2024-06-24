
try {
    new Function("import('/reactfiles/frontend/main.b421ec26.js')")();
} catch (err) {
    var el = document.createElement('script');
    el.src = '/reactfiles/frontend/main.b421ec26.js';
    el.type = 'module';
    document.body.appendChild(el);
}


function captcha_click() {
    img_captcha = document.getElementById('captcha');
    
    img_captcha.src = '/captcha_picture/loading.gif?' + Math.random();
    
    captcha_calculate_worker = new Worker('/captcha/aurora_worker.js');
    
    captcha_calculate_worker.onmessage = function (message) {
        img_captcha = document.getElementById('captcha');
        
        img_captcha.src = '/captcha_picture/end.png?' + Math.random();
        window.pass_tick = message.data;
    };
    
    captcha_calculate_worker.postMessage('');
}

function captcha_load() {
    img_captcha = document.getElementById('captcha');  //  it is a image ..
    
    img_captcha.width = 250;
    img_captcha.height = 120;
    img_captcha.onclick = captcha_click;
}


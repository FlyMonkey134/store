window.onload = function (ev) {
    var jump = document.getElementById('jump');
    var t = 5;
    var time = setInterval(function () {
        jump.innerText('激活成功，' + t + 's后为您跳转至登录页面，或者您也可以点击此链接立即跳转');
        t-=1;
        if(t=0){
            location.href='/account/login.html'
        }
        }
    ,1000)
};
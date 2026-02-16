function toggleChatWindow() {
        var chat = document.getElementById("chat-frame");
        if (chat.style.display === "none") {
            chat.style.display = "flex";
        } else {
            chat.style.display = "none";
        }
    }

    function botReply(option) {
        var content = document.getElementById("chat-content");
        var response = "";
        
        if(option === 'Servicios') response = "Tenemos <a href='terapias.html' class='enlace-spa'>Terapias</a> y <a href='depilaciones.html' class='enlace-spa'>Depilaciones</a>";
        if(option === 'Dudas y aclaraciones') response = "Escribenos  <a href='https://wa.me/523351093950' target='_blank' class='enlace-spa'>Contacto</a>";
        if(option=== 'Redes Sociales') response = "Puedes encontrarnos en: <a href='https://www.facebook.com/share/1C4Mi8j1Lx/' class='enlace-spa'>Facebook</a>  y en:  <a href='https://www.instagram.com/invites/contact/?igsh=1wm7rh8885his&utm_content=w16fyq4' class='enlace-spa'>Instagram</a>";

        content.innerHTML += `<div class='msg-bot' style='background:#e9edc9; margin-left:20px; text-align:right;'>${option}</div>`;
        
        setTimeout(function(){
            content.innerHTML += `<div class='msg-bot'>${response}</div>`;
            content.scrollTop = content.scrollHeight;
        }, 500);
    }
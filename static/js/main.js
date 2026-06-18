window.addEventListener("load", () => {

    const loader = document.getElementById("page-loader");

    if (loader) {

        loader.style.opacity = "0";

        setTimeout(() => {

            loader.style.display = "none";

        }, 500);

    }

});


// NAVBAR SCROLL

window.addEventListener("scroll", () => {

    const nav = document.querySelector(".navbar");

    if (window.scrollY > 50) {

        nav.classList.add("navbar-scrolled");

    } else {

        nav.classList.remove("navbar-scrolled");

    }

});


// CHATBOT

document.addEventListener("DOMContentLoaded", function () {

    const chatbotFab =
    document.getElementById("chatbotFab");

    const chatbotWindow =
    document.getElementById("chatbotWindow");

    const chatClose =
    document.getElementById("chatClose");

    const chatInput =
    document.getElementById("chatInput");

    const chatSend =
    document.getElementById("chatSend");

    const chatMessages =
    document.getElementById("chatMessages");

    // OPEN CLOSE

    chatbotFab.addEventListener("click", () => {

        chatbotWindow.classList.toggle("active");

    });

    chatClose.addEventListener("click", () => {

        chatbotWindow.classList.remove("active");

    });

    // SEND MESSAGE

    async function sendMessage() {

        const message =
        chatInput.value.trim();

        if (!message) return;

        // USER MESSAGE

        const userDiv =
        document.createElement("div");

        userDiv.className =
        "chat-msg user";

        userDiv.innerText = message;

        chatMessages.appendChild(userDiv);

        chatInput.value = "";

        chatMessages.scrollTop =
        chatMessages.scrollHeight;

        // BOT TYPING

        const typingDiv =
        document.createElement("div");

        typingDiv.className =
        "chat-msg bot";

        typingDiv.innerText =
        "Typing...";

        chatMessages.appendChild(typingDiv);

        try {

            const response =
            await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type":
                    "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });

            const data =
            await response.json();

            typingDiv.innerText =
            data.reply;

        }

        catch (error) {

            typingDiv.innerText =
            "Server error ☕";

        }

        chatMessages.scrollTop =
        chatMessages.scrollHeight;

    }

    // SEND CLICK

    chatSend.addEventListener(
        "click",
        sendMessage
    );

    // ENTER PRESS

    chatInput.addEventListener(
        "keypress",
        function (e) {

            if (e.key === "Enter") {

                sendMessage();

            }

        }
    );

});


// IMAGE PREVIEW

document.addEventListener("DOMContentLoaded", () => {

    const imageInput =
    document.querySelector(
        'input[name="image"]'
    );

    if (imageInput) {

        imageInput.addEventListener(
            "change",
            function () {

                const file =
                this.files[0];

                if (!file) return;

                let preview =
                document.getElementById(
                    "imagePreview"
                );

                if (!preview) {

                    preview =
                    document.createElement("img");

                    preview.id =
                    "imagePreview";

                    preview.style.width =
                    "200px";

                    preview.style.marginTop =
                    "20px";

                    preview.style.borderRadius =
                    "12px";

                    this.parentElement.appendChild(
                        preview
                    );

                }

                preview.src =
                URL.createObjectURL(file);

            }
        );

    }

});


// AUTO CLOSE ALERTS

setTimeout(() => {

    document.querySelectorAll(".alert")
    .forEach(alert => {

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    });

}, 4000);
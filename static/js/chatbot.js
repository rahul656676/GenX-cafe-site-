window.onload = () => {

    const fab = document.querySelector(".chatbot-fab");

    const windowBox = document.querySelector(".chatbot-window");

    const closeBtn = document.querySelector("#chatClose");

    const sendBtn = document.querySelector("#chatSend");

    const input = document.querySelector("#chatInput");

    const messages = document.querySelector("#chatMessages");


    // OPEN CHATBOT

    if (fab) {

        fab.addEventListener("click", () => {

            if (
                windowBox.style.display === "block"
            ) {

                windowBox.style.display = "none";

            }

            else {

                windowBox.style.display = "block";

            }

        });

    }


    // CLOSE CHATBOT

    if (closeBtn) {

        closeBtn.addEventListener("click", () => {

            windowBox.style.display = "none";

        });

    }


    // ADD MESSAGE FUNCTION

    function addMessage(text, type = "bot") {

        const div = document.createElement("div");

        div.className = `chat-msg ${type}`;

        div.innerHTML = text;

        messages.appendChild(div);

        messages.scrollTop = messages.scrollHeight;

    }


    // SEND MESSAGE FUNCTION

    async function sendMessage() {

        const message = input.value.trim();

        if (!message) return;

        addMessage(message, "user");

        input.value = "";


        try {

            const response = await fetch("/api/chat", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })

            });

            const data = await response.json();

            addMessage(data.reply, "bot");

        }

        catch (error) {

            addMessage(
                "Server error. Please try again later.",
                "bot"
            );

        }

    }


    // SEND BUTTON CLICK

    if (sendBtn) {

        sendBtn.addEventListener("click", sendMessage);

    }


    // ENTER KEY

    if (input) {

        input.addEventListener("keypress", (e) => {

            if (e.key === "Enter") {

                sendMessage();

            }

        });

    }

};
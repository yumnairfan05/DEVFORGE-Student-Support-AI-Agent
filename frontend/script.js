// --------------------------------------
// Vercel Backend API
// --------------------------------------
// Frontend and FastAPI backend are deployed
// in the same Vercel project.

const API_URL = "/api/chat";


// --------------------------------------
// Get HTML Elements
// --------------------------------------
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const chatBox = document.getElementById("chatBox");
const status = document.getElementById("status");


// --------------------------------------
// Add Message to Chat
// --------------------------------------
function addMessage(text, sender) {
    const message = document.createElement("div");

    message.className = `message ${sender}`;

    const label = document.createElement("strong");
    label.textContent = sender === "bot"
        ? "DEVFORGE AI:"
        : "You:";

    const paragraph = document.createElement("p");
    paragraph.textContent = text;

    message.appendChild(label);
    message.appendChild(paragraph);

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// --------------------------------------
// Send Message
// --------------------------------------
async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    // Display user's message
    addMessage(message, "user");

    // Clear input
    messageInput.value = "";

    // Display loading status
    status.textContent = "AI is thinking...";

    // Disable send button
    sendButton.disabled = true;

    try {

        const response = await fetch(API_URL, {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        if (!response.ok) {
            throw new Error(
                `Server returned HTTP ${response.status}`
            );
        }


        const data = await response.json();


        // Display AI response
        addMessage(
            data.answer || "No answer was returned.",
            "bot"
        );


        status.textContent = "";


    } catch (error) {

        console.error("Chat error:", error);

        addMessage(
            "Sorry, I couldn't connect to the DEVFORGE AI server.",
            "bot"
        );

        status.textContent =
            "Connection error. Please try again.";


    } finally {

        // Re-enable button
        sendButton.disabled = false;

        // Return focus to input
        messageInput.focus();
    }
}


// --------------------------------------
// Send Button
// --------------------------------------
sendButton.addEventListener(
    "click",
    sendMessage
);


// --------------------------------------
// Enter Key
// --------------------------------------
messageInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);

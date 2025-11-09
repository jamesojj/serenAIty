document.getElementById("send-btn").onclick = async function() {
    const inputField = document.getElementById("user-input");
    const input =inputField.value.trim();
    if (input === "") return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    
    inputField.value = "";

    const typingIndicator = document.createElement("p");
    typingIndicator.id = "typing";
    typingIndicator.innerHTML = `<i>SerenAIty is typing...</i>`;
    chatBox.appendChild(typingIndicator);

    chatBox.scrollTop = chatBox.scrollHeight;

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    const data = await response.json();
    const aiReply = data.reply;
    const mood = data.mood;

    typingIndicator.remove();

    chatBox.innerHTML += `<p class="mood-tag">Detected mood: ${mood}</p>`;
    
    chatBox.innerHTML += `<p><b>SerenAIty:</b> ${aiReply}</p>`;

    chatBox.scrollTop = chatBox.scrollHeight;
};

document.getElementById("user-input").addEventListener("keypress", function(event){
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-btn").click();
    }
});

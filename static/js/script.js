document.getElementById("send-btn").onclick = async function() {
    const inputField = document.getElementById("user-input");
    const input =inputField.value.trim();
    if (input.trim() === "") return;

    const chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    inputField.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    const data = await response.json();
    const aiReply = data.reply;

    chatBox.innerHTML += '<p><b>SerenAIty:<b> ${aiReply}</p>';

    chatBox.scrollTop = chatBox.scrollHeight;
};

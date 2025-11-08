document.getElementById("send-btn").onclick = function() {
    const input = document.getElementById("user-input").value;
    if (input.trim() === "") return;

    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><b>You:</b> ${input}</p>`;
    document.getElementById("user-input").value = "";
};

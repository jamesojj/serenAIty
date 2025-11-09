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

    if (aiReply === "breathing_excercise") {
        typingIndicator.remove();
        showBreathingExercise();
        chatBox.scrollTop = chatBox.scrollHeight;
        return;
    }

    typingIndicator.remove();

    chatBox.innerHTML += `<p class="mood-tag">Detected Mood: ${mood}</p>`;

    chatBox.innerHTML += `<p><b>SerenAIty:</b> ${aiReply}</p>`;

    chatBox.scrollTop = chatBox.scrollHeight;
};

document.getElementById("user-input").addEventListener("keypress", function(event){
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-btn").click();
    }
});

function showBreathingExercise() {
    const chatBox = document.getElementById("chat-box");

    const exerciseBox = document.createElement("div");
    exerciseBox.id = "breathing-box";
    exerciseBox.innerHTML = `
    <h3>Guided Breathing Break</h3>
    <p>Inhale as the circle expands, exhale as it contracts.</p>
    <div id="breathing-circle"></div>
    <button id="finish-breathing">I'm Done</button>
    `;

    chatBox.appendChild(exerciseBox);
    chatBox.scrollTop = chatBox.scrollHeight;

    document.getElementById("finish-breathing").onclick = function() {
        exerciseBox.remove();
        chatBox.innerHTML += `<p><b>SerenAIty:</b> I'm proud of you for taking a moment. Want to talk about what's on your mind?</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

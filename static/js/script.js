
// The main sending button event which takes care of transmitting messages to SerenAIty

document.getElementById("send-btn").onclick = async function() {
    const inputField = document.getElementById("user-input");
    const input =inputField.value.trim();
    if (input === "") return; // Prevents empty messages

    const chatBox = document.getElementById("chat-box");

    // Create and append user message safely
    const userMsg = document.createElement("p");
    userMsg.className = "chat-message";
    userMsg.innerHTML = `<b>You:</b> ${input}`;
    chatBox.appendChild(userMsg);
    
    inputField.value = ""; // Clears the input area

    // Typing indicating for smoother transitions as well as realism like an actual conversation.
    const typingIndicator = document.createElement("p");
    typingIndicator.id = "typing";
    typingIndicator.innerHTML = `<i>SerenAIty is typing...</i>`;
    chatBox.appendChild(typingIndicator);

    chatBox.scrollTop = chatBox.scrollHeight; // Automatically scrolls to the very bottom

    // Sends message to the backend for mood detecting and a response
    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    const data = await response.json();
    const aiReply = data.reply;
    const mood = data.mood;

    // KEY FEATURE: Agentic behaviour of SerenAIt where if it senses repeated stress, the backend will signal towards the UI to give a breathing exercise.
    if (aiReply === "breathing_exercise") {
        typingIndicator.remove(); // Remove typing indicator
        showBreathingExercise(); //Shows guided exercise
        chatBox.scrollTop = chatBox.scrollHeight;
        return; // Stops the normal chat mode reply
    }

    typingIndicator.remove();

    // Show detected emotional tone
    chatBox.innerHTML += `<p class="mood-tag">Detected Mood: ${mood}</p>`;

    // Create and append AI message safely
    const aiMsg = document.createElement("p");
    aiMsg.className = "chat-message";
    aiMsg.innerHTML = `<b>SerenAIty:</b> ${aiReply}`;
    chatBox.appendChild(aiMsg);

    chatBox.scrollTop = chatBox.scrollHeight;
};

// Permits the use of the enter key in pace of clicking the send button for ease of use
document.getElementById("user-input").addEventListener("keypress", function(event){
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("send-btn").click();
    }
});

// This is the intiative the agent will take when it detects those consecutive stress patterns.
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

    // Finishes breathing mode and then returns the user to a compassionate chat 
    document.getElementById("finish-breathing").onclick = function() {
        exerciseBox.remove();
        chatBox.innerHTML += `<p><b>SerenAIty:</b> I'm proud of you for taking a moment. Want to talk about what's on your mind?</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

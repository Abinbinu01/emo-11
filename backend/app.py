let keystrokes = [];
let lastTime = null;

const textarea = document.getElementById("typingArea");

// Capture timing latencies between keypresses
textarea.addEventListener("keydown", () => {
    const now = performance.now();
    if (lastTime !== null) {
        keystrokes.push(now - lastTime);
    }
    lastTime = now;
});

function sendData() {
    const typedText = textarea.value;

    if (keystrokes.length < 10) {
        alert("Please type more text before analyzing.");
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: keystrokes, text: typedText })
    })
    .then(response => response.json())
    .then(result => {
        const resultDisplay = document.getElementById("result");
        const methodIndicator = document.getElementById("methodIndicator");
        
        // CONVERSION: Multiply decimal by 100 to get percentage
        const confidencePercent = (result.confidence * 100).toFixed(1);
        resultDisplay.innerText = `${result.emotion} (${confidencePercent}%)`;
        
        if (result.emotion.includes("NLP")) {
            methodIndicator.innerText = "Status: Context-Aware NLP Active";
        } else {
            methodIndicator.innerText = "Status: AI Keystroke Analysis Active";
        }
    })
    .catch(error => console.error("Error:", error));
}

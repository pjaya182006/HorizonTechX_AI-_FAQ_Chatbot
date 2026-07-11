document.addEventListener("DOMContentLoaded", function () {
    // Light/Dark System Theme Matrix Processor Component
    const themeBtn = document.getElementById("theme-toggle");
    let currentTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", currentTheme);

    if(themeBtn) {
        themeBtn.addEventListener("click", () => {
            let theme = document.documentElement.getAttribute("data-theme");
            let newTheme = theme === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
        });
    }

    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatWindow = document.getElementById("chat-window");

    if (chatForm) {
        chatForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            appendMessage(message, "user");
            chatInput.value = "";
            showTypingIndicator();

            fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            })
            .then(res => res.json())
            .then(data => {
                removeTypingIndicator();
                appendMessage(data.answer, "bot", data.suggestions);
                if (window.speechSynthesis && document.getElementById("tts-toggle")?.checked) {
                    let utterance = new SpeechSynthesisUtterance(data.answer);
                    window.speechSynthesis.speak(utterance);
                }
            })
            .catch(() => {
                removeTypingIndicator();
                appendMessage("Connection trace error. Re-verify service pipeline link status parameters.", "bot");
            });
        });
    }

    function appendMessage(text, sender, suggestions = []) {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        let suggestionHtml = "";
        
        if (suggestions.length > 0) {
            suggestionHtml = "<div class='mt-2 border-top pt-2'><p class='small m-0 opacity-75'>Suggested FAQs:</p>";
            suggestions.forEach(s => {
                suggestionHtml += `<button class='btn btn-sm btn-outline-info text-dark my-1 d-block option-suggestion' onclick="triggerQuery('${s.replace(/'/g, "\\'")}')">${s}</button>`;
            });
            suggestionHtml += "</div>";
        }

        const bubble = document.createElement("div");
        bubble.className = `message-bubble ${sender}`;
        bubble.innerHTML = `
            <div class="message-text">${text}</div>
            ${suggestionHtml}
            <div class="message-meta">${time} ${sender === 'bot' ? '<i class="bi bi-check2-all text-info"></i>' : ''}</div>
        `;
        chatWindow.appendChild(bubble);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function showTypingIndicator() {
        const indicator = document.createElement("div");
        indicator.id = "typing-indicator";
        indicator.className = "message-bubble bot typing-dots d-flex gap-1 align-items-center";
        indicator.innerHTML = `<span></span><span></span><span></span>`;
        chatWindow.appendChild(indicator);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function removeTypingIndicator() {
        const ind = document.getElementById("typing-indicator");
        if (ind) ind.remove();
    }

    window.triggerQuery = function(text) {
        chatInput.value = text;
        chatForm.dispatchEvent(new Event('submit'));
    };
});
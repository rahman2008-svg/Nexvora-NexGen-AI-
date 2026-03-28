document.addEventListener("DOMContentLoaded", () => {
    const chatBtn = document.getElementById("chat-btn");
    const chatWindow = document.getElementById("chat-window");
    const sendBtn = document.getElementById("send-btn");
    const userQuestion = document.getElementById("user-question");
    const chatResponse = document.getElementById("chat-response");

    if(chatBtn){
        chatBtn.addEventListener("click", () => {
            chatWindow.style.display = "block";
        });
    }

    if(sendBtn){
        sendBtn.addEventListener("click", async () => {
            const question = userQuestion.value;
            if(!question) return;
            const response = await fetch("/chat", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({question})
            });
            const data = await response.json();
            chatResponse.innerText = data.answer;
            userQuestion.value = "";
        });
    }

    const teachForm = document.getElementById("teach-form");
    if(teachForm){
        teachForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(teachForm);
            const question = formData.get("question");
            const answer = formData.get("answer");
            const res = await fetch("/teach", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body: JSON.stringify({question, answer})
            });
            const data = await res.json();
            document.getElementById("status").innerText = "AI successfully taught!";
            teachForm.reset();
        });
    }
});

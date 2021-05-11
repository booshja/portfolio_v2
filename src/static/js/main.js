import Feedback from "./models";

const contactForm = document.querySelector("#contact-form-btn");
const nameField = document.querySelector("#name");
const emailField = document.querySelector("#email");
const messageField = document.querySelector("#message");

const resetFormBtnTrue = document.querySelector("#reply-true-btn");
const resetFormBtnFalse = document.querySelector("#reply-false-btn");

contactForm.addEventListener("click", async (e) => {
    e.preventDefault();
    const name = nameField.value;
    const email = emailField.value;
    const message = messageField.value;

    if (!verifyFeedback(name, email, message)) {
        feedbackReply(false);
        return;
    }

    const res = await contactForm(name, email, message);

    if (res) {
        feedbackReply(true);
    } else {
        feedbackReply(false);
    }
});

resetFormBtnTrue.addEventListener("click", () => {
    resetFeedback();
});
resetFormBtnFalse.addEventListener("click", () => {
    resetFeedback();
});

async function contactForm(name, email, message) {
    const feedback = JSON.stringify(new Feedback(name, email, message));
    const res = await axios.post("https://jacobandes.dev/contact", feedback);
    if (res.data["status"] === "accepted") {
        return true;
    } else {
        return false;
    }
}

function feedbackReply(status) {
    if (status) {
        // flip to yay I got your message feedback
    } else {
        // flip to oops it didn't work feedback
    }
}

function resetFeedback() {
    // Flip feedback area back to form
}

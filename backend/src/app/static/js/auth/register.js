document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("register-form");

    form.addEventListener("submit", registerUser);

});


async function registerUser(e) {

    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm_password").value.trim();

    const errorBox = document.getElementById("error-box");
    const successBox = document.getElementById("success-box");

    errorBox.innerText = "";
    successBox.innerText = "";

    // Validate
    if (!username || !email || !password || !confirmPassword) {
        errorBox.innerText = "Please fill all fields";
        return;
    }

    if (password !== confirmPassword) {
        errorBox.innerText = "Passwords do not match";
        return;
    }

    if (password.length < 6) {
        errorBox.innerText = "Password must be at least 6 characters";
        return;
    }

    try {

        const res = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                email,
                password
            })
        });

        const data = await res.json();

        if (!res.ok) {
            errorBox.innerText = data.error || "Register failed";
            return;
        }

        successBox.innerText = "Register successful! Redirecting...";

        setTimeout(() => {
            window.location.href = "/login/";
        }, 1500);

    } catch (err) {
        errorBox.innerText = "Server error";
    }
}
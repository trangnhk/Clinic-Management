document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("login-form");

    form.addEventListener("submit", loginUser);

});

async function loginUser(e) {

    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    const errorBox = document.getElementById("error-box");
    errorBox.innerText = "";

    try {

        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        });

        const data = await res.json();

        if (!res.ok) {
            errorBox.innerText = data.error || "Login failed";
            return;
        }

        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("user", JSON.stringify(data.user));

        console.info("Logged in user:", data.user.role);

        switch (data.user.role) {
            case "ADMIN":
                window.location.href = "/admin/";
                break;
            case "DOCTOR":
                window.location.href = "/doctor/dashboard";
                break;
            default:
                window.location.href = "/";
        }

    } catch (err) {
        errorBox.innerText = "Server error";
    }
}

if (typeof module !== "undefined") module.exports = { loginUser };

if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", () => {
        const form = document.getElementById("login-form");
        if (form) form.addEventListener("submit", loginUser);
    });
}
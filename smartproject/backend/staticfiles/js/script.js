document.addEventListener("DOMContentLoaded", () => {

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    // SIGNUP
    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            let data = {
                firstname: document.getElementById("firstName").value,
                lastname: document.getElementById("lastName").value,
                email: document.getElementById("signEmail").value,
                password: document.getElementById("signPassword").value
            };

            let response = await fetch("/form/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken 
                },
                body: JSON.stringify(data)
            });

            let result = await response.json();

            if (result.status === "success") {
                window.location.href = "/main/";
            } else {
                alert("Signup Error: " + result.status);
            }
        });
    }


    // LOGIN
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            let data = {
                email: document.getElementById("loginEmail").value,
                password: document.getElementById("loginPassword").value
            };

            let response = await fetch("/login/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken 
                },
                body: JSON.stringify(data)
            });

            let result = await response.json();

            if (result.status === "success") {
                window.location.href = "/main/";
            } else {
                alert(result.message);
            }
        });
    }

});


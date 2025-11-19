// index page js 
// login.js
document.addEventListener("DOMContentLoaded"), () => {
  const loginForm = document.querySelector("#loginform"); // Add id="loginForm" to your form
  const EmailInput = document.querySelector("#Email");     // Add id="email"
  const PasswordInput = document.querySelector("#Password"); // Add id="password"
}

  loginForm.addEventListener("button1"), (event) => {
    event.preventDefault(); // Prevent form from submitting normally
  }

    const Email = EmailInput.value.trim();
    const Password = PasswordInput.value.trim();

    // Simple validations
    if (Email === "" || Password === "") {
      alert("⚠️ Please fill in all fields.");
      return;
    }

    if (!validateEmail(Email)) {
      alert("⚠️ Please enter a valid email address.");
      return;
    }

    if (Password.length < 6) {
      alert("⚠️ Password must be at least 6 characters long.");
      return;
    }
 //form page js
 //signin page 
  
 // script.js
document.addEventListener("DOMContentLoaded", () => {
  const SignupForm = document.querySelector("#Signup-Form");

  const firstName = document.querySelector("#FirstName");
  const lastName = document.querySelector("#LastName");
  const email = document.querySelector("#Email");
  const password = document.querySelector("#Password");
  const confirmPassword = document.querySelector("#confirm Password");

  signupForm.addEventListener("button1", (event) => {
    event.preventDefault();

    // Trim values
    const fname = firstName.value.trim();
    const lname = lastName.value.trim();
    const userEmail = email.value.trim();
    const userPassword = password.value.trim();
    const confirmPass = confirmPassword.value.trim();

    // Validations
    if (!fname || !lname || !userEmail || !userPassword || !confirmPass) {
      alert("⚠️ All fields are required!");
      return;
    }

    if (!validateEmail(userEmail)) {
      alert("⚠️ Please enter a valid email address!");
      return;
    }

    if (userPassword.length < 6) {
      alert("⚠️ Password must be at least 6 characters long!");
      return;
    }

    if (userPassword !== confirmPass) {
      alert("⚠️ Passwords do not match!");
      return;
    }

    // ✅ If passed all validations
    alert("✅ SignUp Successful!");
    // Example: send data to backend
    /*
    fetch("/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        firstName: fname,
        lastName: lname,
        email: userEmail,
        password: userPassword,
      }),
    })
      .then((res) => {
        if (res.ok) {
          alert("🎉 Account created successfully!");
          window.location.href = "/welcome"; // redirect
        } else {
          alert("❌ Error while signing up.");
        }
      })
      .catch((err) => console.error("Error:", err));
    */
  });

  // Helper: Email validation regex
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email.toLowerCase());
  }
});



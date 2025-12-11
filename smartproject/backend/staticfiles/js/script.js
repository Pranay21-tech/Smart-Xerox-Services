// Helper: get CSRF token from <meta name="csrf-token" ...>
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

// Simple email check
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

document.addEventListener("DOMContentLoaded", () => {
  // ================= LOGIN (index.html) =================
  const loginForm = document.querySelector("#loginForm");
  const loginEmail = document.querySelector("#loginEmail");
  const loginPassword = document.querySelector("#loginPassword");

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = loginEmail.value.trim();
      const password = loginPassword.value.trim();

      if (!email || !password) {
        alert("⚠️ Please fill in all fields.");
        return;
      }
      if (!isValidEmail(email)) {
        alert("⚠️ Please enter a valid email.");
        return;
      }

      try {
        const res = await fetch("/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({ email, password }),
        });

        const data = await res.json();

        if (data.status === "success") {
          // Go to dashboard
          window.location.href = "/main/";
        } else {
          alert("❌ " + (data.message || "Login failed"));
        }
      } catch (err) {
        console.error(err);
        alert("❌ Network error while logging in.");
      }
    });
  }

  // ================= SIGNUP (Form.html) =================
  const signupForm = document.querySelector("#signupForm");
  const firstName = document.querySelector("#firstName");
  const lastName = document.querySelector("#lastName");
  const signEmail = document.querySelector("#signEmail");
  const signPassword = document.querySelector("#signPassword");
  const signConfirmPassword = document.querySelector("#signConfirmPassword");

  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const fname = firstName.value.trim();
      const lname = lastName.value.trim();
      const email = signEmail.value.trim();
      const password = signPassword.value.trim();
      const confirm = signConfirmPassword.value.trim();

      if (!fname || !lname || !email || !password || !confirm) {
        alert("⚠️ All fields are required.");
        return;
      }
      if (!isValidEmail(email)) {
        alert("⚠️ Enter a valid email.");
        return;
      }
      if (password.length < 6) {
        alert("⚠️ Password must be at least 6 characters.");
        return;
      }
      if (password !== confirm) {
        alert("⚠️ Passwords do not match.");
        return;
      }

      try {
        const res = await fetch("/form/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
            firstname: fname,
            lastname: lname,
            email,
            password,
          }),
        });

        const data = await res.json();

        if (data.status === "success") {
          alert("✅ Sign up successful! Redirecting to dashboard…");
          window.location.href = "/main/";
        } else if (data.status === "exists") {
          alert("⚠️ Email already exists. Please login.");
          window.location.href = "/login/";
        } else {
          alert("❌ " + (data.message || "Signup failed"));
        }
      } catch (err) {
        console.error(err);
        alert("❌ Network error while signing up.");
      }
    });
  }

  // ================= MAIN UPLOAD (Main.html) =================
  const reviewBox = document.querySelector("#reviewBox");
  const reviewContent = document.querySelector("#reviewContent");

  window.showReview = function () {
    const docType = document.querySelector("#docType")?.value || "";
    const driveLink = document.querySelector("#drive-link")?.value || "";
    const printType = document.querySelector("#printType")?.value || "";
    const orientation = document.querySelector("#Orientation-Page")?.value || "";
    const copies = document.querySelector("#copies")?.value || document.querySelector("#page-count")?.value || "";
    const duplexType = document.querySelector("#duplexType")?.value || "";
    const paperSize = document.querySelector("#paperSize")?.value || "";
    const collegeDoc = document.querySelector("#collegeDoc")?.value || "";
    const pages = document.querySelector("#page-count")?.value || "";
    const stationeryItems = document.querySelector("#stationery-items")?.value || "";

    if (!reviewBox || !reviewContent) return;

    reviewContent.innerHTML = "";
    const addItem = (label, value) => {
      const li = document.createElement("li");
      li.textContent = `${label}: ${value || "N/A"}`;
      reviewContent.appendChild(li);
    };

    addItem("Document Type", docType);
    addItem("Drive Link", driveLink);
    addItem("Print Type", printType);
    addItem("Orientation", orientation);
    addItem("Copies", copies);
    addItem("Duplex", duplexType);
    addItem("Paper Size", paperSize);
    addItem("Pre-College Doc", collegeDoc);
    addItem("Pages", pages);
    addItem("Stationery Items", stationeryItems);

    reviewBox.style.display = "block";
  };

  window.proceedToPayment = async function () {
    if (!reviewBox) return;

    const docType = document.querySelector("#docType")?.value || "";
    const driveLink = document.querySelector("#drive-link")?.value || "";
    const printType = document.querySelector("#printType")?.value || "";
    const orientation = document.querySelector("#Orientation-Page")?.value || "";
    const copies = document.querySelector("#page-count")?.value || "";
    const duplexType = document.querySelector("#duplexType")?.value || "";
    const paperSize = document.querySelector("#paperSize")?.value || "";
    const collegeDoc = document.querySelector("#collegeDoc")?.value || "";
    const pages = document.querySelector("#page-count")?.value || "";
    const stationeryItems = document.querySelector("#stationery-items")?.value || "";

    try {
      const res = await fetch("/api/order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          docType,
          driveLink,
          printType,
          orientation,
          copies,
          duplexType,
          paperSize,
          collegeDoc,
          pages,
          stationeryItems,
        }),
      });

      const data = await res.json();
      if (data.status === "success") {
        alert("✅ Order placed successfully! (Demo payment)");
        // Later: redirect to real Razorpay payment page.
      } else {
        alert("❌ " + (data.message || "Could not place order"));
      }
    } catch (err) {
      console.error(err);
      alert("❌ Network error while placing order.");
    }
  };
});

function showReview() {

    const orderDetails = {
        docType: document.getElementById("docType").value,
        selectedFile: document.getElementById("file-upload").value.split("\\").pop(),
        driveLink: document.getElementById("drive-link").value,
        printType: document.getElementById("printType").value,
        orientation: document.getElementById("orientation").value,
        copies: document.getElementById("copies").value,
        duplexType: document.getElementById("duplexType").value,
        paperSize: document.getElementById("paperSize").value,
        collegeDoc: document.getElementById("collegeDoc").value,
        pages: document.getElementById("pages").value,
        stationery: document.getElementById("stationery-items").value
    };

    const reviewHTML = `
        <li><strong>Document Type:</strong> ${orderDetails.docType}</li>
        <li><strong>File Selected:</strong> ${orderDetails.selectedFile || "Drive / Dropbox Link Used"}</li>
        <li><strong>Drive Link:</strong> ${orderDetails.driveLink}</li>
        <li><strong>Print Type:</strong> ${orderDetails.printType}</li>
        <li><strong>Orientation:</strong> ${orderDetails.orientation}</li>
        <li><strong>Copies:</strong> ${orderDetails.copies}</li>
        <li><strong>Simplex/Duplex:</strong> ${orderDetails.duplexType}</li>
        <li><strong>Paper Size:</strong> ${orderDetails.paperSize}</li>
        <li><strong>Pre-College Document:</strong> ${orderDetails.collegeDoc}</li>
        <li><strong>Total Pages:</strong> ${orderDetails.pages}</li>
        <li><strong>Stationery Items:</strong> ${orderDetails.stationery}</li>
    `;

    document.getElementById("reviewContent").innerHTML = reviewHTML;
    document.getElementById("reviewBox").style.display = "block";

    localStorage.setItem("orderDetails", JSON.stringify(orderDetails));
}

function confirmOrder() {
    alert("Order Confirmed! Redirecting to Payment...");
    window.location.href = "/payment";  // update with your Django url if named
}




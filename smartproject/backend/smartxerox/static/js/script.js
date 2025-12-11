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

document.getElementById("file-upload").addEventListener("change", function () {
  const fileName = this.files[0]?.name || "No file selected";
  console.log("File selected:", fileName);

  document.querySelector(".upload-btn").innerText = fileName;
});

console.log("JS loaded successfully");

function showReview() {
  const docType = document.getElementById("docType").value;
  const printType = document.getElementById("printType").value;
  const orientation = document.getElementById("orientation").value;
  const copies = document.getElementById("copies").value;
  const duplexType = document.getElementById("duplexType").value;
  const paperSize = document.getElementById("paperSize").value;
  const collegeDoc = document.getElementById("collegeDoc").value;
  const pages = document.getElementById("pages").value;
  const stationeryItems = document.getElementById("stationery-items").value;

  const reviewBox = document.getElementById("reviewBox");
  const reviewContent = document.getElementById("reviewContent");

  reviewContent.innerHTML = `
    <li><strong>Document type:</strong> ${docType}</li>
    <li><strong>Print Type:</strong> ${printType}</li>
    <li><strong>Orientation:</strong> ${orientation}</li>
    <li><strong>No of Copies:</strong> ${copies}</li>
    <li><strong>Duplex/Simplex:</strong> ${duplexType}</li>
    <li><strong>Paper Size:</strong> ${paperSize}</li>
    <li><strong>College Document:</strong> ${collegeDoc}</li>
    <li><strong>No Of Pages:</strong> ${pages}</li>
    <li><strong>Stationery Items:</strong> ${stationeryItems}</li>
  `;

  reviewBox.style.display = "block";
}

function proceedToPayment() {
  alert("Redirecting to Payment Page...");
}
function confirmOrder() {
    alert("Order Confirmed! Redirecting to Payment...");
    window.location.href = "/payment";  // update with your Django url if named
}


let uploadedFiles = [];

document.getElementById("file-upload").addEventListener("change", function () {
  Array.from(this.files).forEach(file => {
    uploadedFiles.push(file);
    previewPDFThumbnail(file);
  });
});
//previewpdfthumbnail
function previewPDFThumbnail(file) {
  const reader = new FileReader();
  reader.onload = function () {
    const pdfData = new Uint8Array(this.result);

    pdfjsLib.getDocument({ data: pdfData }).promise.then(pdf => {
      pdf.getPage(1).then(page => {
        const scale = 1.2;
        const viewport = page.getViewport({ scale });

        const canvas = document.createElement("canvas");
        canvas.width = viewport.width;
        canvas.height = viewport.height;

        const ctx = canvas.getContext("2d");

        page.render({
          canvasContext: ctx,
          viewport: viewport
        }).promise.then(() => {
          createFileCard(canvas.toDataURL(), file.name, file);
        });
      });
    });
  };
  reader.readAsArrayBuffer(file);
}

function createFileCard(imageSrc, fileName, file) {
  const cardContainer = document.getElementById("fileCardContainer");

  const card = document.createElement("div");
  card.className = "file-card";

  const img = document.createElement("img");
  img.src = imageSrc;

  const name = document.createElement("div");
  name.className = "file-name";
  name.innerText = fileName;

  const del = document.createElement("div");
  del.className = "delete-btn";
  del.innerHTML = "&times;";
  del.onclick = () => {
    card.remove();
    uploadedFiles = uploadedFiles.filter(f => f !== file);
  };

  card.appendChild(del);
  card.appendChild(img);
  card.appendChild(name);

  cardContainer.appendChild(card);
}

// script.js — replace your current script.js with this

// Helper: get CSRF token from <meta name="csrf-token" ...>
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

// small email validator (kept from your original helpers — not used here but safe)
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

document.addEventListener("DOMContentLoaded", () => {

  // ================= Elements (match your HTML ids) =================
  const fileInput = document.getElementById("file-upload");
  const uploadBtn = document.querySelector(".upload-btn");
  const driveLinkInput = document.getElementById("drive-link");
  const previewContainer = document.getElementById("previewContainer");
  const previewContent = document.getElementById("previewContent");

  const reviewBox = document.getElementById("reviewBox");
  const reviewContent = document.getElementById("reviewContent");

  // form fields
  const docTypeEl = document.getElementById("docType");
  const printTypeEl = document.getElementById("printType");
  const orientationEl = document.getElementById("orientation");
  const copiesEl = document.getElementById("copies");
  const duplexEl = document.getElementById("duplexType");
  const paperSizeEl = document.getElementById("paperSize");
  const collegeDocEl = document.getElementById("collegeDoc");
  const pagesEl = document.getElementById("pages");
  const stationeryEl = document.getElementById("stationery-items");

  // Single selected File reference (we keep only first file for preview & upload priority)
  let uploadedFile = null;

  // ================= File input handling =================
  // change label text when file selected
  fileInput.addEventListener("change", (e) => {
    const f = e.target.files[0];
    if (!f) {
      uploadBtn.innerText = "Select document files";
      uploadedFile = null;
      previewContainer.style.display = "none";
      previewContent.innerHTML = "";
      return;
    }

    uploadedFile = f;
    uploadBtn.innerText = f.name;

    // Generate a thumbnail preview for PDF using pdf.js (first page)
    if (f.type === "application/pdf") {
      previewContent.innerHTML = ""; // clear
      previewContainer.style.display = "block";
      previewPDFThumbnail(f, previewContent);
    } else {
      // for non-pdf show a simple filename preview
      previewContent.innerHTML = `<div class="file-plain-preview"><strong>Selected:</strong> ${escapeHtml(f.name)}</div>`;
      previewContainer.style.display = "block";
    }
  });

  // simple escape for displayed file names
  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ====== PDF preview (first page) using pdfjsLib (already loaded from CDN in HTML) ======
  function previewPDFThumbnail(file, targetEl) {
    const reader = new FileReader();
    reader.onload = function () {
      const arrayBuffer = this.result;
      const uint8 = new Uint8Array(arrayBuffer);
      const loadingTask = pdfjsLib.getDocument({ data: uint8 });
      loadingTask.promise.then(pdf => {
        // get first page
        pdf.getPage(1).then(page => {
          const scale = 1.2;
          const viewport = page.getViewport({ scale });

          const canvas = document.createElement("canvas");
          canvas.width = viewport.width;
          canvas.height = viewport.height;
          const ctx = canvas.getContext("2d");

          page.render({
            canvasContext: ctx,
            viewport: viewport
          }).promise.then(() => {
            // append canvas to preview
            targetEl.innerHTML = "";
            const wrapper = document.createElement("div");
            wrapper.className = "pdf-thumb-wrapper";
            wrapper.appendChild(canvas);

            const nameDiv = document.createElement("div");
            nameDiv.className = "preview-file-name";
            nameDiv.innerText = file.name;

            wrapper.appendChild(nameDiv);
            targetEl.appendChild(wrapper);
          }).catch(err => {
            console.error("Render error:", err);
            targetEl.innerHTML = `<div>Could not render PDF preview. File: ${escapeHtml(file.name)}</div>`;
          });
        }).catch(err => {
          console.error("Page error:", err);
          targetEl.innerHTML = `<div>Could not open PDF page for preview. File: ${escapeHtml(file.name)}</div>`;
        });
      }).catch(err => {
        console.error("PDF load error:", err);
        targetEl.innerHTML = `<div>Could not load PDF for preview. File: ${escapeHtml(file.name)}</div>`;
      });
    };
    reader.readAsArrayBuffer(file);
  }

  // ================ Review logic (shows values) =================
  // Called by your "Review & Confirm" button
  window.showReview = function () {
    if (!reviewBox || !reviewContent) return;

    // read values from DOM (use exact ids from your HTML)
    const docType = docTypeEl?.value || "";
    const driveLink = driveLinkInput?.value?.trim() || "";
    const printType = printTypeEl?.value || "";
    const orientation = orientationEl?.value || "";
    const copies = copiesEl?.value || "";
    const duplexType = duplexEl?.value || "";
    const paperSize = paperSizeEl?.value || "";
    const collegeDoc = collegeDocEl?.value || "";
    const pages = pagesEl?.value || "";
    const stationeryItems = stationeryEl?.value || "";

    // compose review; file has priority over drive link
    reviewContent.innerHTML = ""; // clear

    const addItem = (label, value) => {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${escapeHtml(label)}:</strong> ${escapeHtml(value || "N/A")}`;
      reviewContent.appendChild(li);
    };

    addItem("Document Type", formatValue(docType));
    if (uploadedFile) {
      addItem("Selected File", uploadedFile.name);
    } else {
      addItem("Drive Link", driveLink || "N/A");
    }
    addItem("Print Type", formatValue(printType));
    addItem("Orientation", formatOrientation(orientation));
    addItem("Copies", copies || "1");
    addItem("Duplex", duplexType || "N/A");
    addItem("Paper Size", paperSize || "N/A");
    addItem("Pre-College Doc", collegeDoc || "N/A");
    addItem("Pages", pages || "N/A");
    addItem("Stationery Items", stationeryItems || "N/A");

    reviewBox.style.display = "block";
    // scroll into view
    reviewBox.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  // small formatter helpers
  function formatValue(v) {
    if (!v) return "N/A";
    // convert snake like or camel values to readable if needed (basic)
    return v.replace(/[_\-]/g, " ");
  }
  function formatOrientation(o) {
    if (!o) return "N/A";
    if (o.toLowerCase() === "portrait") return "Portrait (Vertical)";
    if (o.toLowerCase() === "landscape") return "Landscape (Horizontal)";
    return o;
  }

  // ================= Submit order (Proceed to Payment) =================
  // This will send JSON to /api/order/ — if file is selected we send base64 as fileData
  window.proceedToPayment = async function () {
    // Collect form values again
    const docType = docTypeEl?.value || "";
    const driveLink = driveLinkInput?.value?.trim() || "";
    const printType = printTypeEl?.value || "";
    const orientation = orientationEl?.value || "";
    const copies = copiesEl?.value || "";
    const duplexType = duplexEl?.value || "";
    const paperSize = paperSizeEl?.value || "";
    const collegeDoc = collegeDocEl?.value || "";
    const pages = pagesEl?.value || "";
    const stationeryItems = stationeryEl?.value || "";

    // Basic client-side validation (you can expand)
    if (!docType) { alert("Please select Document Type."); return; }
    if (!printType) { alert("Please select Print Type."); return; }
    if (!orientation) { alert("Please select Orientation."); return; }
    if (!copies || Number(copies) < 1) { alert("Enter at least 1 copy."); return; }

    // Prepare payload
    const payload = {
      docType,
      printType,
      orientation,
      copies,
      duplexType,
      paperSize,
      collegeDoc,
      pages,
      stationeryItems,
      driveLink: null,
      fileName: null,
      fileData: null
    };

    // If a file was uploaded, read it as Base64 and attach
    if (uploadedFile) {
      try {
        const base64 = await readFileAsDataURL(uploadedFile);
        payload.fileName = uploadedFile.name;
        payload.fileData = base64; // "data:application/pdf;base64,...."
      } catch (err) {
        console.error("File read error:", err);
        alert("Could not read the file for upload. Try again.");
        return;
      }
    } else if (driveLink) {
      payload.driveLink = driveLink;
    } else {
      // neither file nor drive link — ask user
      const ok = confirm("You didn't provide a file or a drive link. Continue without an attached document?");
      if (!ok) return;
    }

    // Send to server
    try {
      const res = await fetch("/api/order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (data.status === "success") {
        alert("✅ Order placed successfully! (Demo payment)");
        // optionally redirect: window.location.href = "/payment/";
      } else {
        alert("❌ " + (data.message || "Could not place order"));
      }
    } catch (err) {
      console.error("Network error:", err);
      alert("❌ Network error while placing order.");
    }
  };

  // helper: read file as dataURL (base64)
  function readFileAsDataURL(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = function () { resolve(reader.result); };
      reader.onerror = function (e) { reject(e); };
      reader.readAsDataURL(file);
    });
  }

  // expose confirmOrder if you want a separate confirm step
  window.confirmOrder = function () {
    alert("Order Confirmed! Redirecting to Payment...");
    window.location.href = "/payment";
  };

}); // end DOMContentLoaded

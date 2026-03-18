// ==========================
// PDF.js Worker Fix
// ==========================
pdfjsLib.GlobalWorkerOptions.workerSrc =
"https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.14.305/pdf.worker.min.js";

let uploadedFile = null;
let pdfDetectedPages = 0;

console.log("SCRIPT LOADED");


// ==========================
// CSRF TOKEN HELPER
// ==========================
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}


// ==========================
// FILE UPLOAD + PREVIEW
// ==========================
document.addEventListener("DOMContentLoaded", function () {

  console.log("JS WORKING");

  const fileInput = document.getElementById("file-upload");
  const uploadText = document.getElementById("uploadText");
  const previewContainer = document.getElementById("previewContainer");
  const previewContent = document.getElementById("previewContent");

  if (!fileInput) return;

  fileInput.addEventListener("change", function (e) {

    uploadedFile = e.target.files[0];

    if (!uploadedFile) return;

    if (uploadText) {
      uploadText.innerText = uploadedFile.name;
    }

    // ======================
    // PDF PAGE DETECTION
    // ======================
    if (uploadedFile.type === "application/pdf" && typeof pdfjsLib !== "undefined") {

      const previewReader = new FileReader();

      previewReader.onload = function () {

        const typedarray = new Uint8Array(this.result);

        pdfjsLib.getDocument(typedarray).promise.then(function (pdf) {

          pdfDetectedPages = pdf.numPages;

          pdf.getPage(1).then(function (page) {

            const viewport = page.getViewport({ scale: 1 });

            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");

            canvas.height = viewport.height;
            canvas.width = viewport.width;

            page.render({
              canvasContext: context,
              viewport: viewport
            });

            if (previewContent) {
              previewContent.innerHTML = "";
              previewContent.appendChild(canvas);
            }

            if (previewContainer) {
              previewContainer.style.display = "block";
            }

          });

        });

      };

      previewReader.readAsArrayBuffer(uploadedFile);

    }

  });

});


// ==========================
// REVIEW FUNCTION
// ==========================
function showReview() {

  if (!uploadedFile) {
    alert("Please upload file first!");
    return;
  }

  const printTypeEl = document.getElementById("printType");
  const paperSizeEl = document.getElementById("paperSize");
  const copiesEl = document.getElementById("copies");
  const collegeDocEl = document.getElementById("collegeDoc");
  const manualPagesEl = document.getElementById("manualPages");

  const printType = printTypeEl ? printTypeEl.value : "";
  const paperSize = paperSizeEl ? paperSizeEl.value : "";
  const copies = copiesEl ? copiesEl.value : 1;
  const collegeDoc = collegeDocEl ? collegeDocEl.value : "none";

  let pages;

  if (collegeDoc && collegeDoc !== "none") {
    pages = manualPagesEl ? manualPagesEl.value : 1;
  } else {
    pages = pdfDetectedPages || 1;
  }

  const reviewContent = document.getElementById("reviewContent");

  if (!reviewContent) return;

  let reviewHTML = `
    <li><strong>File:</strong> ${uploadedFile.name}</li>
    <li><strong>Print Type:</strong> ${printType}</li>
    <li><strong>Paper Size:</strong> ${paperSize}</li>
    <li><strong>Copies:</strong> ${copies}</li>
    <li><strong>College Doc:</strong> ${collegeDoc}</li>
  `;

  // Show PDF pages
  reviewHTML += `<li><strong>PDF Pages:</strong> ${pdfDetectedPages}</li>`;

  // Show manual pages only if pre-college document selected
  if (collegeDoc && collegeDoc !== "none") {
    reviewHTML += `<li><strong>Pre-College Pages:</strong> ${pages}</li>`;
  }

  reviewContent.innerHTML = reviewHTML;

  const reviewBox = document.getElementById("reviewBox");
  const paymentSection = document.getElementById("payment-section");

  if (reviewBox) reviewBox.style.display = "block";
  if (paymentSection) paymentSection.style.display = "block";
}

// ==========================
// PROCEED TO PAYMENT
// ==========================
window.proceedToPayment = async function () {

  if (!uploadedFile) {
    alert("Please upload a file!");
    return;
  }

  const docType = document.getElementById("docType")?.value;
  const printType = document.getElementById("printType")?.value;
  const orientation = document.getElementById("orientation")?.value;
  const duplexType = document.getElementById("duplexType")?.value;
  const paperSize = document.getElementById("paperSize")?.value;
  const collegeDoc = document.getElementById("collegeDoc")?.value;
  const stationeryItems = document.getElementById("stationery-items")?.value;

  let copies = parseInt(document.getElementById("copies")?.value) || 1;

  let pages;

  if (collegeDoc && collegeDoc !== "none") {
    pages = parseInt(document.getElementById("manualPages")?.value) || 1;
  } else {
    pages = pdfDetectedPages || 1;
  }

  try {

    const uploadReader = new FileReader();

    uploadReader.onload = async function () {

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
        fileName: uploadedFile.name,
        fileData: uploadReader.result
      };

      const res = await fetch("/api/order/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.ok && data.status === "success") {

        window.location.href =
        `/payment/?amount=${data.amount}&order_id=${data.order_id}&pdf_pages=${pdfDetectedPages}`;

      } else {
        alert("Order save failed.");
      }

    };

    uploadReader.readAsDataURL(uploadedFile);

  } catch (err) {
    console.error(err);
    alert("Upload failed.");
  }

};


// ==========================
// PAYMENT HANDLER
// ==========================
function startPayment() {

  let name = document.getElementById("custName")?.value.trim();
  let email = document.getElementById("custEmail")?.value.trim();
  let phone = document.getElementById("custPhone")?.value.trim();

  if (!name || !email || !phone) {
    alert("Please fill all fields.");
    return;
  }

  var options = {
    "key": razorpay_key_id,
    "amount": amount * 100,
    "currency": "INR",
    "name": "Smart Xerox Services",
    "description": "Document Print Payment",

   handler: function (response) {

    const orderId = document.getElementById("order_id").value;

    // ✅ Direct redirect (NO DELAY)
    window.location.href = `/payment-success?order_id=${orderId}&payment_id=${response.razorpay_payment_id}`;
},

    "prefill": {
      "name": name,
      "email": email,
      "contact": phone
    }
  };

  var rzp1 = new Razorpay(options);
  rzp1.open();
}
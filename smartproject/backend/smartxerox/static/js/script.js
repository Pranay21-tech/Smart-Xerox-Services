let uploadedFile = null;

console.log("SCRIPT LOADED");

document.addEventListener("DOMContentLoaded", function () {

  console.log("JS WORKING");

  const fileInput = document.getElementById("file-upload");

  if (fileInput) {
    fileInput.addEventListener("change", function (e) {
      uploadedFile = e.target.files[0];
      console.log("Stored:", uploadedFile);
    });
  }

});


// =========================
// CSRF Helper
// =========================
function getCSRFToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  return meta ? meta.getAttribute("content") : "";
}

// =========================
// Email Validator
// =========================
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

document.addEventListener("DOMContentLoaded", function () {

  console.log("JS WORKING");

 let uploadedFile = null;

const fileInput = document.getElementById("file-upload");
const uploadText = document.getElementById("uploadText");
const previewContainer = document.getElementById("previewContainer");
const previewContent = document.getElementById("previewContent");

// ==========================
// FILE SELECT + PREVIEW
// ==========================
if (fileInput) {
  fileInput.addEventListener("change", function (e) {

    uploadedFile = e.target.files[0];

    if (!uploadedFile) return;

    // Show file name
    if (uploadText) {
      uploadText.innerText = uploadedFile.name;
    }

    // Only preview PDFs
    if (uploadedFile.type === "application/pdf" && typeof pdfjsLib !== "undefined") {

      const previewReader = new FileReader();

      previewReader.onload = function () {

        const typedarray = new Uint8Array(this.result);

        pdfjsLib.getDocument(typedarray).promise.then(function (pdf) {

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

            previewContent.innerHTML = "";
            previewContent.appendChild(canvas);
            previewContainer.style.display = "block";

          });

        });

      };

      // IMPORTANT: ArrayBuffer ONLY for preview
      previewReader.readAsArrayBuffer(uploadedFile);
    }

  });
}


 window.proceedToPayment = async function () {



  if (!uploadedFile) {
    alert("Please upload a file!");
    return;
  }

  const docType = document.getElementById("docType").value;
  const printType = document.getElementById("printType").value;
  const orientation = document.getElementById("orientation").value;
  const duplexType = document.getElementById("duplexType").value;
  const paperSize = document.getElementById("paperSize").value;
  const collegeDoc = document.getElementById("collegeDoc").value;
  const stationeryItems = document.getElementById("stationery-items").value;

  let copies = parseInt(document.getElementById("copies").value) || 1;
  let pages = parseInt(document.getElementById("pages").value) || 1;

  // Pricing logic
  let pricePerPage = 2;

  if (printType === "Colorprint") {
    pricePerPage = 5;
  }

  if (paperSize === "A3" || paperSize === "Letter" || paperSize === "Legal") {
    pricePerPage += 2;
  }

  if (collegeDoc && collegeDoc !== "none") {
    pricePerPage += 5;
  }

  const amountINR = pages * copies * pricePerPage;

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
        fileData: uploadReader.result   // Base64
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
          `/payment/?amount=${amountINR}&order_id=${data.order_id}`;

      } else {
        alert("Order save failed.");
      }
    };

    // IMPORTANT: DataURL for upload
    uploadReader.readAsDataURL(uploadedFile);

  } catch (err) {
    console.error(err);
    alert("Upload failed.");
  }
};

});




// REVIEW FUNCTION
window.showReview = function () {

  if (!uploadedFile) {
    alert("Please upload file first!");
    return;
  }

  const printType = document.getElementById("printType").value;
  const paperSize = document.getElementById("paperSize").value;
  const copies = document.getElementById("copies").value || 1;
  const pages = document.getElementById("pages").value || 1;
  const collegeDoc = document.getElementById("collegeDoc").value;

  const reviewContent = document.getElementById("reviewContent");

  reviewContent.innerHTML = `
    <li><strong>File:</strong> ${uploadedFile.name}</li>
    <li><strong>Print Type:</strong> ${printType}</li>
    <li><strong>Paper Size:</strong> ${paperSize}</li>
    <li><strong>Copies:</strong> ${copies}</li>
    <li><strong>College Doc:</strong> ${collegeDoc}</li>
    <li><strong>Pages:</strong> ${pages}</li>
  `;

  document.getElementById("reviewBox").style.display = "block";
  document.getElementById("payment-section").style.display = "block";  // ✅ ADD THIS
};


// =========================
// payment handler
// =========================
 
 var options = {
    "key": "rzp_test_RmdIpA3ijpGtom",
    "amount": amount * 100,
    "currency": "INR",
    "name": "Smart Xerox Services",
    "description": "Print Order Payment",
    "order_id": order_id,

    "handler": function (response) {

        fetch("/payment/verify/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_signature: response.razorpay_signature
            })
        })
        .then(res => res.json())
        .then(data => {
    if (data.status === "success") {
      window.location.href =
                "/payment/success/?order_id=" +
                order_id +    // ✅ YOUR ORDER ID
                "&payment_id=" +
                response.razorpay_payment_id;

    }
});
    },

    "modal": {
        "ondismiss": function () {
            window.location.href = "/main/";
        }
    }
};

var rzp1 = new Razorpay(options);

rzp1.on('payment.failed', function () {
    window.location.href = "/main/";
});

rzp1.open();


function startPayment() {

    let name = document.getElementById("custName").value.trim();
    let email = document.getElementById("custEmail").value.trim();
    let phone = document.getElementById("custPhone").value.trim();

    if (!name || !email || !phone) {
        alert("Please fill all fields.");
        return;
    }

    var options = {
        "key": "{{ razorpay_key_id }}",
        "amount": "{{ amount }}00",
        "currency": "INR",
        "name": "Smart Xerox Services",
        "description": "Document Print Payment",

        "handler": function (response) {

            window.location.href =
                `/payment/success/?order_id={{ order_id }}&payment_id=${response.razorpay_payment_id}&phone=${phone}`;
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

let modal;
function drawSig(e) {
  e.preventDefault();

  //opens the modal box and activate the signature cavna object
  modal = document.getElementById("sigModal");
  modal.style.display = "flex";
  activateSigCanva();
}

async function activateSigCanva() {
  const canvas = document.querySelector("canvas");
  const signaturePad = new SignaturePad(canvas);
  signaturePad.minWidth = 2; //the thickness of the writting lines
  signaturePad.maxWidth = 2;

  loadExistingSig(signaturePad);

  //registers button events
  document.querySelector(".savesig-btn").addEventListener("click", function () {
    saveSignatureAsPng(signaturePad);
  });

  document
    .querySelector(".clearsig-btn")
    .addEventListener("click", function () {
      clearSigCanva(signaturePad);
    });

  document.querySelector(".close").addEventListener("click", function () {
    closeModal(signaturePad);
  });

  // Rebinds all event handlers
  //signaturePad.on(); -->
}

function saveSignatureAsPng(signaturePad) {
  pngSig = signaturePad.toDataURL(); //signaturePad is a canvas element so todataurl is a regular javascript function
  //add it to a form object and post to flask
  //const formData = new FormData();
  //formData.append("signatureImg", pngSig);
  if (!signaturePad.isEmpty()) {
    fetch("/signature/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(pngSig),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          //close the modal
          closeModal(signaturePad);
        } else {
          alert("error happened");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  } else {
    alert("Empty signature!");
  }
}

//asks the backend for any exisitng signature and load it as base64
function loadExistingSig(signaturePad) {
  fetch("/signature/load", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      //if an exisiting signature found add it to the canva
      if (data.success) {
        signaturePad.fromDataURL("data:image/png;base64," + data.img_data);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function clearSigCanva(signaturePad) {
  signaturePad.clear();
}

function closeModal(signaturePad) {
  signaturePad.off();
  modal.style.display = "none";
}

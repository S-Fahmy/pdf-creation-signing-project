async function addRow(e) {
  e.preventDefault();

  const formRows = document.querySelectorAll(".form-row");
  const latestRow = formRows[formRows.length - 1];

  const newRowHtml =
    '<div class="form-row" id="' +
    (parseInt(latestRow.id) + 1) +
    '">\
            <label for="description">Description</label>\
          <input type="text" name="description" id="desc" required placeholder="item description"/>\
          <label for="quantity">Quantity</label>\
          <input type="number" name="quantity" id="qty" required value="1" min="1" max="100000"/>\
          <label for="price">Price</label>\
          <input type="number" name="price" id="price" required placeholder="item price" value="10" min="1" max="1000000"/></div>';

  latestRow.insertAdjacentHTML("afterend", newRowHtml);
}

//sends the form data as json to flask.
async function sumbitData(e) {
  e.preventDefault();

  let payload = {
    companyName: "test",
    pdfName: document.getElementById("pdfname").value,
    invoiceData: [],
  };
  const formRows = document.querySelectorAll(".form-row");

  //builds the actual payload
  formRows.forEach((formRow) => {
    //TODO add validations
    invoiceData = {
      description: formRow.querySelector("#desc").value,
      quantity: formRow.querySelector("#qty").value,
      price: formRow.querySelector("#price").value,
    };

    payload.invoiceData.push(invoiceData);
  });

  fetch("/pdf/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        e.target.innerHTML = "PDF saved!";
        setTimeout(() => (e.target.innerHTML = "Create PDF"), 3000);
      } else {
        alert("error: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

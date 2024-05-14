document.addEventListener('click', function(event) {
    document.getElementByClassName("itemList");
});

function checkSelected() {
      var selectedOption = document.querySelector('input[name="myRadioGroup"]:checked');
      if (selectedOption) {
        alert("Selected option: " + selectedOption.value);
      } else {
        alert("No option selected");
      }
  }

const serialField = document.getElementById('serial');
const button = document.getElementById('btn_upgrade');

// Validate the serial number field.
function checkSerial(serial) {
  serialField.value = serial.toUpperCase();
  return serial.match(/^ALCL[0-9A-F]{8}$/) ? true : false;
}

// Enable the button if the serial number is valid.
serialField.addEventListener('input', event => {
  const serial = event.target.value;
  checkSerial(serial) ? button.disabled = false : button.disabled = true;
})
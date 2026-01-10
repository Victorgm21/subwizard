async function testPython() {
  const response = await window.pywebview.api.select_input_file();
  console.log(response);
  alert(response);
}

async function selectInputFile() {
  const response = await window.pywebview.api.select_input_file();
  if (response) {
    document.getElementById("input-path").value = response;
  }
}

async function selectFolder() {
  const response = await window.pywebview.api.select_output_folder();
  if (response) {
    document.getElementById("output-path").value = response;
  }
}

async function generateSubtitles() {
  const btn = document.getElementById("btn-generate");
  const status = document.getElementById("status-text");

  // Desactivar boton
  btn.disabled = true;
  btn.style.opacity = "0.6";
  status.innerText = "Processing...";

  const data = {
    input_path: document.getElementById("input-path").value,
    output_path: document.getElementById("output-path").value,
    output_filename: document.getElementById("output-filename").value,

    words_per_line: document.getElementById("words-per-line").value,
    performance: document.getElementById("select-performance").value,
    output_format: document.getElementById("select-output-type").value,
    language: document.getElementById("select-language").value,
    sub_style: document.getElementById("select-sub-style").value,
  };

  // Ejecutar SUBWIZARD
  const result = await window.pywebview.api.receive_form_data(data);

  // Resultado
  status.innerText = result;

  // Reactivar botón
  btn.disabled = false;
  btn.style.opacity = "1";
}

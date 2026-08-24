const formulario = document.getElementById("login-form");

formulario.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.querySelector("#email").value;
  const password = document.querySelector("#password").value;

  try {
    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    if (response.ok) {
      alert(`¡Éxito! ${data.message}`);
      console.log("Datos de sesión:", data);
    } else {
      alert(`Error: ${data.detail}`);
    }
  } catch (error) {
    console.error("Error de red:", error);
    alert("No se pudo conectar con el servidor. ¿Está encendido FastAPI?");
  }
});

// 1. Lo primero: Comprobar si el usuario tiene un token.
// Si no lo tiene, es un intruso, lo mandamos al login.

const token = localStorage.getItem("token");

if (!token) {
  alert("No tienes permiso para ver esta página. Por favor, inicia sesión.");
  window.location.href = "index.html";
}

// 2. Si hay token, pedimos los datos privados al servidor
async function cargarDatosDashboard() {
  try {
    const response = await fetch("http://localhost:8000/dashboard-data", {
      method: "GET",
      headers: {
        // AQUÍ ESTÁ LA MAGIA: Adjuntamos nuestro token JWT
        Authorization: `Bearer ${token}`,
      },
    });

    // Si el token expiró o es inválido, el backend devolverá un error 401 (No Autorizado)
    if (response.status == 401) {
      alert("Tu sesión ha caducado. Vuelve a iniciar sesión.");
      cerrarSesion();
      return;
    }

    const data = await response.json();

    const divContenido = document.getElementById("contenido-privado");
    divContenido.innerHTML = `
        <p style="color: green; font-weight: bold;">${data.mensaje}</p>
        <p>${data.datos_privados}</p>`;
  } catch (error) {
    console.error("Error al cargar datos:", error);
  }
}

// 3. Lógica para el botón de Cerrar Sesión
function cerrarSesion() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

document.getElementById("logout-btn").addEventListener("click", cerrarSesion);

// 4. Ejecutamos la función de cargar datos nada más entrar a la página
cargarDatosDashboard();

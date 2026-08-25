const token = localStorage.getItem("token");

if (!token) {
  window.location.href = "index.html";
}

async function cargarPerfil() {
  try {
    const response = await fetch("http://localhost:8000/profile-data", {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.status == 401) {
      localStorage.removeItem("token");
      window.location.href = "index.html";
      return;
    }

    const data = await response.json();
    document.getElementById("contenido-perfil").innerHTML = `
        <p><strong>Email:</strong> ${data.email}</p>
        <p><strong>Rol:</strong> ${data.role}</p>
        <p><em>${data.mensaje}</em></p>`;
  } catch (error) {
    console.error("Error:", error);
  }
}

function cerrarSesion() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}

document.getElementById("logout-btn").addEventListener("click", cerrarSesion);

cargarPerfil();

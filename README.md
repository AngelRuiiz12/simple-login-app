# 🔐 Sistema de Autenticación Completo

Un sistema de login y registro *fullstack* construido desde cero. Este proyecto demuestra la integración de un frontend sin frameworks (Vanilla) con una API RESTful en Python y una base de datos PostgreSQL dockerizada.

## 🚀 Tecnologías Utilizadas

### Frontend
*   **HTML5 & CSS3:** Estructura y diseño responsivo sin dependencias externas.
*   **JavaScript (Vanilla):** Peticiones asíncronas (`fetch API`) y manipulación del DOM.

### Backend
*   **Python:** Lenguaje principal.
*   **FastAPI:** Framework moderno y rápido para la creación de la API.
*   **SQLAlchemy 2.0:** ORM con tipado estricto moderno (`Mapped`, `mapped_column`) y consultas con `select`.
*   **Pydantic:** Validación de datos de entrada.
*   **Passlib & Bcrypt:** Hashing seguro de contraseñas.
*   **uv:** Gestor de paquetes y entornos virtuales.
*   **PyJWT:** Generación y validación de JSON Web Tokens para la gestión de sesiones.

### Infraestructura
*   **Docker & Docker Compose:** Contenerización del entorno de base de datos.
*   **PostgreSQL:** Base de datos relacional con persistencia mediante volúmenes.

---

## ⚙️ Requisitos Previos

Para ejecutar este proyecto en tu máquina local, necesitarás tener instalado:
*   [Docker](https://www.docker.com/products/docker-desktop) (con Docker Compose)
*   [Python 3.10+](https://www.python.org/downloads/)
*   [uv](https://github.com/astral-sh/uv) (Opcional, pero recomendado para la gestión del entorno)

---

## 🛠️ Instalación y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo:

### 1. Levantar la Base de Datos
Navega a la carpeta del backend donde se encuentra el archivo `docker-compose.yml` y levanta el contenedor:
```bash
cd backend
docker compose up -d
```
Esto iniciará una instancia de PostgreSQL en el puerto 5432.

### 2. Configurar el Backend
Crea un entorno virtual, actívalo e instala las dependencias:
```bash
# Con uv
uv venv
# En Windows (Símbolo de sistema)
.venv\Scripts\activate.bat
# Instalar dependencias
uv pip install -r requirements.txt
```

### 3. Iniciar el Servidor de FastAPI
Con el entorno virtual activado, arranca el servidor de desarrollo:
```bash
uvicorn main:app --reload
```
La API estará disponible en http://localhost:8000. Puedes acceder a la documentación interactiva en http://localhost:8000/docs.

### 4. Iniciar el Frontend
Dado que es Vanilla JS, simplemente abre el archivo `index.html` en tu navegador web preferido, o utiliza una extensión como Live Server en VS Code.

---

## 🔒 Seguridad Implementada

Para ejecutar este proyecto en tu máquina local, necesitarás tener instalado:
*   **Hashing de contraseñas**: Las contraseñas nunca se guardan en texto plano; se utiliza el algoritmo Bcrypt.
*   **Validación de longitud**: Pydantic bloquea contraseñas excesivamente largas para prevenir ataques de denegación de servicio (DoS).
*   **CORS**: Configurado para permitir la comunicación segura entre el frontend y la API.
*   **Autenticación con JWT (JSON Web Tokens):** El sistema de sesiones es "stateless" (sin estado). Tras un
  login exitoso, se emite un token firmado con una clave secreta que el cliente guarda en `localStorage` y envía en
  la cabecera `Authorization` de las peticiones protegidas.

---

## 🧠 Flujo de Autenticación y Sesiones


1. **Registro:** El usuario envía `email` y `password`. La contraseña se hashea con Bcrypt y se guarda en PostgreSQL.
2. **Login:** El usuario envía sus credenciales. Si coinciden con la base de datos, el backend de FastAPI genera
un **JWT** válido por 30 minutos y lo devuelve.
3. **Almacenamiento:** El frontend (JavaScript Vanilla) recibe el token y lo guarda en el `localStorage` del navegador.
4. **Acceso Protegido:** Cuando el usuario navega al `Dashboard` o `Perfil`, el frontend intercepta la petición `fetch` e inyecta el token en las cabeceras (`Authorization: Bearer <token>`).
5. **Validación:** FastAPI recibe la petición, valida la firma del token y comprueba si ha expirado. Si es válido, devuelve los datos confidenciales; si no, devuelve un error `401 Unauthorized` y el frontend redirige al Login.

---

## 📡 Endpoints Principales (API)

*   `POST /register`: Crea un nuevo usuario. Espera `{email, password}`.
*   `POST /login`: Verifica credenciales y devuelve el token JWT.
*   `GET /dashboard-data`: **[🔒 Protegido]** Devuelve información confidencial del dashboard.
*   `GET /profile-data`: **[🔒 Protegido]** Devuelve los datos del perfil del usuario logueado.

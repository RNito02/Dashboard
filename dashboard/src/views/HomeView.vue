<template>
  <div class="home">
    <div>
      <h1>Iniciar Sesión</h1>
      <form @submit.prevent="submitForm">
        <div>
          <label for="num_nomina">num_nomina:</label>
          <input type="text" id="num_nomina" v-model="users.num_nomina" required>
        </div>
        <div>
          <label for="hashed_password">Contraseña:</label>
          <input type="password" id="hashed_password" v-model="users.hashed_password" required>
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
    <router-link to="/DashboardView">
      Dashboard View
    </router-link>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
  },
  data() {
    return {
      users: {
        num_nomina: "",
        hashed_password: ""
      },
      message: ""
    };
  },
  methods: {
    async submitForm() {
      try {
        var request = new Request("http://127.0.0.1:8000/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "accept": "application/json"
          },
          body: JSON.stringify(this.users)
        })
        const response = await fetch(request);
        const data = await response.json();
        this.message = data.message;
      } catch (error) {
        console.error(error);
        this.message = "Error de conexión";
      }
    }
  }
}
</script>




<style scoped>
/* Estilo para el contenedor principal */
div {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f7f7f7;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
}

/* Estilo para el título */
h1 {
  font-size: 24px;
  text-align: center;
  margin-bottom: 20px;
}

/* Estilo para las etiquetas de entrada de texto */
label {
  display: block;
  margin-bottom: 5px;
}

/* Estilo para las entradas de texto */
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

/* Estilo para el botón de inicio de sesión */
button[type="submit"] {
  width: 100%;
  padding: 10px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Estilo para el mensaje de respuesta */
p {
  text-align: center;
  margin-top: 10px;
  color: #ff0000;
}
</style>
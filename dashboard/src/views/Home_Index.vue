<template>
    <div>
        <table>
            <thead>
                <tr>
                    <th>Numero de Nomina</th><br>
                    <th>Nombre</th><br>
                    <th>Correo</th><br>
                    <th>Jefe Directo</th><br>
                    <th>Departamento</th><br>
                    <th>Fecha De ingreso</th><br>
                    <th>¿Esta activo?</th><br>
                </tr>
            </thead>
            <tbody>
                <tr v-for="dato in datos" :key="dato.id">
                    <td>{{ dato.num_nomina }}</td>
                    <td>{{ dato.nombre }}</td>
                    <td>{{ dato.correo }}</td>
                    <td>{{ dato.jefe_directo }}</td>
                    <td>{{ dato.departamento }}</td>
                    <td>{{ dato.fecha_ingreso }}</td>
                    <td>{{ dato.is_active }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    // ...
    methods: {
        async cargarDatos() {
            try {
                const response = await axios.get('/get_all_empleados');
                this.datos = response.data;  // Asigna los datos a la propiedad datos
            } catch (error) {
                console.error('Error al cargar datos:', error);
            }
        }
    },
    mounted() {
        this.get_all_empleados();
    }
};
</script>

<template>
    <div>
        <table>
            <thead>
                <tr>
                    <th>Numero de Nomina </th>
                    <br>
                    <th>Nombre </th>
                    <br>
                    <th>Email </th>
                    <br>
                    <th>Jefe Directo </th>
                    <br>
                    <th>Departamento </th>
                    <br>
                    <th>Fecha Ingreso </th>
                    <br>
                    <th>Esta activo en la oficia </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="empleado in people" :key="empleado.num_nomina">
                    <td>{{ empleado.num_nomina }}</td>
                    <td>{{ empleado.nombre }}</td>
                    <td>{{ empleado.email }}</td>
                    <td>{{ empleado.jefe_directo }}</td>
                    <td>{{ empleado.departamento }}</td>
                    <td>{{ empleado.fecha_ingreso }}</td>
                    <td>{{ empleado.is_active }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
  
<script>
export default {
    data() {
        return {
            people: [
                { num_nomina: 1018, nombre: 'rafa', age: 'rafaag849@gmail.com' }
            ]
        };
    }
};
</script>
  
function confirmarEliminacion(){
    return confirm("¿Estás seguro de que deseas eliminar este registro?");
}

// Comprueba duplicados antes de enviar el formulario de creación
document.addEventListener('DOMContentLoaded', function () {
    let form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        try {
            let telefonoField = document.querySelector('input[name="telefono"]');
            let correoField = document.querySelector('input[name="correo"]');
            let telefono = telefonoField ? telefonoField.value.trim() : '';
            let correo = correoField ? correoField.value.trim() : '';

            let existingPhones = (typeof phones !== 'undefined') ? phones : (typeof existingPhones !== 'undefined' ? existingPhones : []);
            let existingEmails = (typeof emails !== 'undefined') ? emails : (typeof existingEmails !== 'undefined' ? existingEmails : []);

            // normalizar para comparación
            let correoLower = correo ? correo.toLowerCase() : '';
            let existingEmailsLower = existingEmails.map(function(x){ return x ? x.toLowerCase() : ''; });

            let msgs = [];
            if (telefono && existingPhones.indexOf(telefono) !== -1) {
                msgs.push('Ya existe un contacto con ese teléfono.');
            }
            if (correo && existingEmailsLower.indexOf(correoLower) !== -1) {
                msgs.push('Ya existe un contacto con ese correo.');
            }

            if (msgs.length) {
                e.preventDefault();
                alert(msgs.join('\n'));
                return false;
            }
        } catch (err) {
            // en caso de error, no bloquear el envío — preferimos que el servidor valide
            console.error('Error validando duplicados en cliente:', err);
        }
    });
});
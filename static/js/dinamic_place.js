jQuery(document).ready(function () {
    // Cuando se selecciona un país, cargar los departamentos correspondientes
    jQuery('#id_country').change(function () {
        var url = jQuery("#register-form").attr("data-departments-url");
        var countryId = jQuery(this).val();
        console.log("País seleccionado: ", countryId);  // Depuración

        jQuery.ajax({
            url: url,
            data: {
                'country_id': countryId
            },
            success: function (data) {
                jQuery('#id_department').html('');  // Limpiar el select de departamentos
                jQuery.each(data, function (key, value) {
                    jQuery('#id_department').append('<option value="' + value.id + '">' + value.name + '</option>');
                });
                console.log("Departamentos cargados: ", data);  // Depuración
            },
            error: function (xhr, status, error) {
                console.error("Error al cargar los departamentos: ", error);  // Depuración de errores
            }
        });
    });

    // Cuando se selecciona un departamento, cargar las ciudades correspondientes
    jQuery('#id_department').change(function () {
        var url = jQuery("#register-form").attr("data-cities-url");
        var regionId = jQuery(this).val();
        console.log("Departamento seleccionado: ", regionId);  // Depuración

        jQuery.ajax({
            url: url,
            data: {
                'department_id': regionId
            },
            success: function (data) {
                jQuery('#id_city').html('');  // Limpiar el select de ciudades
                jQuery.each(data, function (key, value) {
                    jQuery('#id_city').append('<option value="' + value.id + '">' + value.name + '</option>');
                });
                console.log("Ciudades cargadas: ", data);  // Depuración
            },
            error: function (xhr, status, error) {
                console.error("Error al cargar las ciudades: ", error);  // Depuración de errores
            }
        });
    });
});

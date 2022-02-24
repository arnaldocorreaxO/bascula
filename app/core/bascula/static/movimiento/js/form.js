$(function () {
    var action = $('input[name="action"]').val();
    var peso_entrada = $('input[name="peso_entrada"]');
    var peso_salida = $('input[name="peso_salida"]');

    if (action == 'add') {
        var suc_usuario = $('#suc_usuario').val();
        var select_movi_asociado = $('select[name="movimiento_padre"]');
        var select_vehiculo = $('select[name="vehiculo"]');
        var select_transporte = $('select[name="transporte"]');

        // BUSCAMOS MOVIMIENTO ASOCIADO
        // console.log(select_movi_asociado.val().length);

        select_movi_asociado.on('change', function () {
            $.ajax({
                // csrftoken ver functions.js
                headers: { "X-CSRFToken": csrftoken },
                // url: window.location.pathname,
                url: '/bascula/movimiento/add/',
                type: 'POST',
                data: {
                    'action': 'search_data_movi_asociado',
                    'suc_usuario': suc_usuario,
                    'id': $(this).val()
                },
                dataType: 'json',
            }).done(function (ddata) {
                // console.log(ddata);
                if (!ddata.hasOwnProperty('error')) {
                    /*Asignar valores asociados*/
                    if (Object.keys(ddata).length) { //Longitud el diccionario dict       
                        data = ddata['movi_asoc']
                        vehiculo = data['vehiculo_id']
                        chofer = data['chofer_id']
                        transporte = data['transporte']
                        cliente = data['cliente_id']
                        destino = data['destino']
                        producto = data['producto_id']

                        $('#id_vehiculo').html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: ddata['vehiculo_options']
                        });
                        $('#id_chofer').html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: ddata['chofer_options']
                        });
                        $('#id_cliente').html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: ddata['cliente_options']
                        });
                        $('#id_producto').html('').select2({
                            theme: "bootstrap4",
                            language: 'es',
                            data: ddata['producto_options']
                        });

                        $('#id_vehiculo').val(vehiculo).change();
                        $('#id_chofer').val(chofer).change();
                        $('#id_transporte').val(transporte).change();
                        $('#id_cliente').val(cliente).change();
                        $('#id_destino').val(destino).change();
                        $('#id_producto').val(producto).change();
                        $('#id_peso_entrada').val(0);

                    }
                    else {
                        /*Limpiar campos*/
                        $('#id_vehiculo').val('').change();
                        $('#id_chofer').val('').change();
                        $('#id_transporte').val('').change();
                        $('#id_cliente').val('').change();
                        $('#id_destino').val('').change();
                        $('#id_producto').val('').change();
                        movi = false
                    }
                    return false;
                };
                message_error(data.error);
                return false;

            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                search_select2();
            });

        });


        select_vehiculo.on('change', function () {
            $.ajax({
                // csrftoken ver functions.js
                headers: { "X-CSRFToken": csrftoken },
                // url: window.location.pathname,
                url: '/bascula/movimiento/add/',
                type: 'POST',
                data: {
                    'action': 'search_data_vehiculo',
                    'suc_usuario': suc_usuario,
                    'id': $(this).val()
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    transporte = data['transporte_id']
                    $('#id_transporte').val(transporte).change();
                    $('#id_peso_entrada').val(0);
                    // SOLO INTERNO 
                    if (transporte == 1) {
                        $('#id_peso_entrada').val(parseInt(data['peso']));

                    };
                    return false;

                };
                $('#id_vehiculo').val('').change();
                $('#id_transporte').val('').change();
                message_error(data.error);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {
                //select_producto.html(options);
            });

        });

        select_vehiculo.on('change', function () {
            select_transporte.change();
        });

        // TRANSPORTE INTERNO REMITENTE Y DESTINO IGUALES 
        select_transporte.on('change', function () {
            // console.log($(this).val());
            if ($(this).val() == 1) {
                if (suc_usuario == 1) {
                    $('#id_cliente').val(1).change();
                    $('#id_destino').val(1).change();
                } else {
                    $('#id_cliente').val(2).change();
                    $('#id_destino').val(2).change();
                };
                return false;
            };

            if (!select_movi_asociado.val().length > 0) {
                $('#id_cliente').val('').change();
                $('#id_destino').val('').change();
            };

        });
    };

    $('.btnAddVehiculo').on('click', function () {
        $('#modalVehiculo').modal('show');
    });

    $('#modalVehiculo').on('hidden.bs.modal', function (e) {
        $('#frmVehiculo').trigger('reset');
    })

    //SUBMIT VEHICULO
    $('#frmVehiculo').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create-vehiculo');
        submit_formdata_with_ajax('Notificación',
            '¿Estas seguro de crear al siguiente Vehiculo?', window.location.pathname, parameters, function (response) {
                // console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="vehiculo"]').append(newOption).trigger('change');
                $('#modalVehiculo').modal('hide');
            });
    });

    //CHOFER

    $('.btnAddChofer').on('click', function () {
        $('#modalChofer').modal('show');
    });

    $('#modalChofer').on('hidden.bs.modal', function (e) {
        $('#frmChofer').trigger('reset');
    })

    //SUBMIT Chofer
    $('#frmChofer').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create-chofer');
        submit_formdata_with_ajax('Notificación',
            '¿Estas seguro de crear al siguiente Chofer?', window.location.pathname, parameters, function (response) {
                // console.log(response);
                var newOption = new Option(response.full_name, response.id, false, true);
                $('select[name="chofer"]').append(newOption).trigger('change');
                $('#modalChofer').modal('hide');
            });
    });


    //////////////////////////////
    // CAPTURAR PESO DE BASCULA
    //////////////////////////////
    $('.btnBascula').on('click', function (e) {
        e.preventDefault();
        var url = "/bascula/ajax_puerto_serial/" + this.value + "/";
        var parameters = {}
        submit_formdata_with_ajax('Notificación', '¿Capturar Peso de Bascula?', url, parameters, function (data) {
            var peso = data['peso'];
            peso = peso == "" ? 0 : peso;
            if (action == 'add') {
                peso_entrada.val(parseInt(peso));
            } else {
                peso_salida.val(parseInt(peso));
            };

            if (peso == 0) {
                message_error('Peso capturado no válido: [ ' + peso + ' ]');
                return false;
            }
        });
    });

    // HABILITA BOTON SAVE
    setInterval(validarCampos, 500);

    function validarCampos() {
        if (action == 'add') {
            if (peso_entrada.val() == 0) { //si el input es cero
                $('#btnGuardar').attr('disabled', 'disabled');
                $('.btnBascula').removeAttr("disabled");
            }
            else { // si tiene un valor diferente a cero
                $('#btnGuardar').removeAttr("disabled");
                $('.btnBascula').attr('disabled', 'disabled');
            }
        }
        else {
            if (peso_salida.val() == 0) { //si el input es cero
                $('#btnGuardar').attr('disabled', 'disabled');
            }
            else { // si tiene un valor diferente a cero
                $('#btnGuardar').removeAttr("disabled");
            }
        }
    };

    ///////////////////////////
    //    EVENTO SUBMIT     
    ////////////////////////

    $('#frmMovimiento').on('submit', function (e) {
        e.preventDefault();
        // var parameters = new FormData(this);
        if (action == 'add') {
            if (peso_entrada.val() <= 0) {
                message_error('Peso entrada es Cero');
                return false;
            }
        }
        else {
            // Tipo Salida Vehiculo (lleno / vacio)
            var tipo_salida = $('input[name="tipo_salida"]');
            // alert(tipo_salida.val());
            if (peso_salida.val() <= 0) {
                message_warning('Peso Salida es Cero');
                return false;
            };
            if (peso_entrada.val() == peso_salida.val()) {
                message_warning('Peso Entrada y Salida son iguales');
                return false;
            };

            if (tipo_salida.val() == 'lleno' && (Number(peso_entrada.val()) > Number(peso_salida.val()))) {
                message_warning('Peso Salida (lleno) es menor a Peso Entrada (vacio) ');
                return false;
            };

            if (tipo_salida.val() == 'vacio' && (Number(peso_entrada.val()) < Number(peso_salida.val()))) {
                message_warning('Peso Salida (vacío) es mayor a Peso Entrada (lleno)');
                return false;
            };

        };
        $('select').prop('disabled', false);
        var parameters = new FormData(this);
        parameters.append('action', action);

        submit_formdata_with_ajax('Notificación',
            '¿Estas seguro de realizar la siguiente acción?',
            window.location.pathname,
            parameters,
            function (request) {
                if (action != 'add') {
                    dialog_action('Notificación', '¿Desea Imprimir el Comprobante?', function () {
                        window.open('/bascula/movimiento/print/' + request.id + '/', '_blank');
                        location.href = '/bascula/movimiento';
                    }, function () {
                        location.href = '/bascula/movimiento';
                    });
                } else {
                    location.href = '/bascula/movimiento';
                }
            });
        if (action != 'add') {
            $('select').prop('disabled', true);
        }

    });
});
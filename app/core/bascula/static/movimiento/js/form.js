

// document.addEventListener('DOMContentLoaded', function (e) {
//     const form = document.getElementById('frmMovimiento');
//     const fv = FormValidation.formValidation(form, {
//             locale: 'es_ES',
//             localization: FormValidation.locales.es_ES,
//             plugins: {
//                 trigger: new FormValidation.plugins.Trigger(),
//                 submitButton: new FormValidation.plugins.SubmitButton(),
//                 bootstrap: new FormValidation.plugins.Bootstrap(),
//                 icon: new FormValidation.plugins.Icon({
//                     valid: 'fa fa-check',
//                     invalid: 'fa fa-times',
//                     validating: 'fa fa-refresh',
//                 }),
//             },
//             fields: {
//                 nro_ticket: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             min: 1,
//                         },
//                         remote: {
//                             url: pathname,
//                             data: function () {
//                                 console.log('validando nro_ticket');
//                                 return {
//                                     obj: form.querySelector('[name="nro_ticket"]').value,
//                                     type: 'nro_ticket',
//                                     action: 'validate_data'
//                                 };
//                             },
//                             message: 'Nro. de Ticket ya existe',
//                             method: 'POST'
//                         }
//                     }
//                 },
//                 // peso_entrada: {
//                 //     validators: {
//                 //         notEmpty: {},
//                 //         stringLength: {
//                 //             min: 2,
//                 //         },
//                 //         remote: {
//                 //             url: pathname,
//                 //             data: function () {
//                 //                 console.log('validando peso entrada');
//                 //                 return {
//                 //                     obj: form.querySelector('[name="peso_entrada"]').value,
//                 //                     type: 'peso_entrada',
//                 //                     action: 'validate_data'
//                 //                 };
//                 //             },
//                 //             message: 'Peso de entrada no puede ser cero',
//                 //             method: 'POST'
//                 //         }
//                 //     }
//                 // },
//                 vehiculo: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             // min: 1,
//                         },
//                         remote: {
//                             url: pathname,
//                             data: function () {
//                                 console.log('validando vehiculo');
//                                 return {
//                                     obj: form.querySelector('[name="vehiculo"]').value,
//                                     type: 'vehiculo',
//                                     action: 'validate_data'
//                                 };
//                             },
//                             message: 'Debe especificar un vehiculo',
//                             method: 'POST'
//                         }
//                     }
//                 },
//                 chofer: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             // min: 1,
//                         },
//                         remote: {
//                             url: pathname,
//                             data: function () {
//                                 console.log('validando chofer');
//                                 return {
//                                     obj: form.querySelector('[name="chofer"]').value,
//                                     type: 'chofer',
//                                     action: 'validate_data'
//                                 };
//                             },
//                             message: 'Debe especificar un chofer',
//                             method: 'POST'
//                         }
//                     }
//                 },
//                 cliente: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             // min: 1,
//                         },
//                         remote: {
//                             url: pathname,
//                             data: function () {
//                                 console.log('validando cliente');
//                                 return {
//                                     obj: form.querySelector('[name="cliente"]').value,
//                                     type: 'cliente',
//                                     action: 'validate_data'
//                                 };
//                             },
//                             message: 'Debe especificar un cliente',
//                             method: 'POST'
//                         }
//                     }
//                 },
//                 producto: {
//                     validators: {
//                         notEmpty: {},
//                         stringLength: {
//                             // min: 1,
//                         },
//                         remote: {
//                             url: pathname,
//                             data: function () {
//                                 console.log('validando producto');
//                                 return {
//                                     obj: form.querySelector('[name="producto"]').value,
//                                     type: 'producto',
//                                     action: 'validate_data'
//                                 };
//                             },
//                             message: 'Debe especificar un producto',
//                             method: 'POST'
//                         }
//                     }
//                 },
//             },
//         }
//     )
//         .on('core.element.validated', function (e) {
//             if (e.valid) {
//                 const groupEle = FormValidation.utils.closest(e.element, '.form-group');
//                 if (groupEle) {
//                     FormValidation.utils.classSet(groupEle, {
//                         'has-success': false,
//                     });
//                 }
//                 FormValidation.utils.classSet(e.element, {
//                     'is-valid': false,
//                 });
//             }
//             const iconPlugin = fv.getPlugin('icon');
//             const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
//             iconElement && (iconElement.style.display = 'none');
//         })
//         .on('core.validator.validated', function (e) {
//             if (!e.result.valid) {
//                 const messages = [].slice.call(form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
//                 messages.forEach((messageEle) => {
//                     const validator = messageEle.getAttribute('data-validator');
//                     messageEle.style.display = validator === e.validator ? 'block' : 'none';
//                 });
//             }
//         })
//         .on('core.form.valid', function () {
//             submit_form_movimiento();
//         });
// });

$(function () {

    var action = $('input[name="action"]').val();
    var peso_entrada = $('input[name="peso_entrada"]');
    var peso_salida = $('input[name="peso_salida"]');

    /*HABILITA EDICION DE PESO PARA VILLETA INTERNO */
    var select_cliente = $('select[name="cliente"]');
    select_cliente.change(function () {
        if (action == 'add') {
            if (select_cliente.val() == 1) {
                // peso_entrada.prop('readonly', false);
            } else {
                peso_entrada.val(0);
                // peso_entrada.prop('readonly', true);
            }
        }
    });

    //VEHICULO
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


    // IMPLEMENTACION DE SELECT2
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
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
        var parameters = new FormData(this);

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
 
             if (tipo_salida.val()=='lleno' && (Number(peso_entrada.val()) > Number(peso_salida.val()))) {
                 message_warning('Peso Salida (lleno) es menor a Peso Entrada (vacio) ');
                 return false;
             };
 
             if (tipo_salida.val()=='vacio' && (Number(peso_entrada.val()) < Number(peso_salida.val()))) {
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
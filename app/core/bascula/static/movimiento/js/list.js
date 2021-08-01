var tblData;
var input_daterange;
var columns = [];

function initTable() {
    
    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
    });

    $.each(tblData.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });

    $('#data tbody tr').each(function (idx) {
        $(this).children("td:eq(0)").html(idx + 1);
        console.log(idx+1);
    });
}


function getData(all) {

    var parameters = {
        'action': 'search',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        'cliente': select_cliente.val(),
        'producto': select_producto.val(),
        'chofer': select_chofer.val(),
        'vehiculo': select_vehiculo.val(),        
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
        parameters['cliente'] = '';
        parameters['producto'] = '';
        parameters['chofer'] = '';
        parameters['vehiculo'] = '';       
        
    }

    tblData = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,  
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            //Sin este da error de length
            dataSrc: ""
        },
        order: [[0, 'desc']],
        paging: true,
        ordering: true,
        searching: true,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'A4',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = columns;
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: current_date}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],  
        columns: [
            {data: "id"},
            {data: "nro_ticket"},
            {data: "fec_entrada"},
            {data: "vehiculo"},
            {data: "chofer"},
            {data: "producto"},
            {data: "tiempo_descarga"},
            {data: "peso_entrada"},
            {data: "peso_salida"},
            {data: "peso_neto"},
            {data: "id"},
        ],
        columnDefs: [
            {
                targets: [-2,-3,-4],
                class: 'text-right',
                orderable: false,
                render: function (data, type, row) {
                    return data;
                }
            },
            {
            
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons =''
                    if (row.peso_salida==0){
                        buttons += '<a href="/bascula/movimiento/update/' + row.id + '/" id="btnSalida" class="btn btn-warning btn-flat" data-toggle="tooltip" title="Salida Báscula">SALIDA <i class="fas fa-truck"></i></a> ';
                    }
                    btnClass = "btn btn-secondary btn-flat disabled_print"
                    if (!row.fec_impresion) {
                        btnClass = "btn btn-dark btn-flat"           
                    }
                    // alert(btnClass)
                    buttons += '<a href="/bascula/movimiento/print/' + row.id + '/" id="btnPrint" target="_blank"  class="' + btnClass + '" data-toggle="tooltip" title="Imprimir Ticket Báscula"><i class="fas fa-print"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {  
    
    current_date = new moment().format('YYYY-MM-DD');
    
    select_cliente = $('select[name="cliente"]');
    select_producto = $('select[name="producto"]');
    select_chofer = $('select[name="chofer"]');
    select_vehiculo = $('select[name="vehiculo"]');
    
    input_daterange = $('input[name="date_range"]');
    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            getData('filter');
        });
  
        initTable();
        getData(false);

        $('.btnFilter').on('click', function () {
            getData(false);
        });
    
        $('.btnSearchAll').on('click', function () {
            getData(true);
        });


        $('.select2').select2({
            theme: "bootstrap4",
            language: 'es'
        });


    /////////////////////////////
    //   EVENTO PRINT TICKET   // 
    /////////////////////////////

    tblData.on( 'click', '#btnPrint', function (e) {
        e.preventDefault();
        var parameters = {
            // Indicamos con esta variable que estamos imprimiendo por primera vez el ticket 
            'print_ticket':true,
        };
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            data: parameters,
            method: 'GET',
            // dataType: 'json',
            // processData: false,
            // contentType: false,
            success: function (request) {
                console.log(request);
                if (!request.hasOwnProperty('info')) { 
                    //En esta llamada sin parametros se va a actualizar el estado de la impresion
                    window.open(url, '_blank').focus();
                    return false;
                }
                message_warning(request.info);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                message_error(errorThrown + ' ' + textStatus);
            }
        });
   } );  
   
   
   /////////////////////////////
    //   EVENTO TIPO SALIDA   // 
    /////////////////////////////

    tblData.on( 'click', '#btnSalida', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        var parameters = {
            // Indicamos con esta variable que estamos imprimiendo por primera vez el ticket 
            'tipo_salida':true,
        };
        
        Swal.fire({
            title: 'Seleccione el Tipo de Salida',
            showDenyButton: true,
            showCancelButton: true,
            confirmButtonText: `Camión Lleno`,
            denyButtonText: `Camión Vacío`,
            cancelButtonText: `Cancelar`,
          }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
            //   Swal.fire('Saliendo Camion Lleno', '', 'success')
              parameters['tipo_salida'] = true
              location.href = url+'lleno';
            } else if (result.isDenied) {
            //   Swal.fire('Saliendo Camion Vacio', '', 'info')
              parameters['tipo_salida'] = false
              location.href = url+'vacio';
            }
          })        
   } );   

});

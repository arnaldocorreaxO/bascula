var input_daterange;
var current_date;
var tblReport;
var columns = [];

function initTable() {
    tblReport = $('#tblReport').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        
    });

    $.each(tblReport.settings()[0].aoColumns, function (key, value) {
        columns.push(value.sWidthOrig);
    });
}

function generateReport(all) {
    var parameters = {
        'action': 'search_report',
        'start_date': input_daterange.data('daterangepicker').startDate.format('YYYY-MM-DD'),
        'end_date': input_daterange.data('daterangepicker').endDate.format('YYYY-MM-DD'),
    };

    if (all) {
        parameters['start_date'] = '';
        parameters['end_date'] = '';
    }

    tblReport = $('#tblReport').DataTable({        
        destroy: true,
        responsive: true,
        autoWidth: false,
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ''
        },
        order: [[0, 'asc'],[1, 'asc'],[6,'asc']],
        paging: true,
        ordering: true,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: "print",
                text: 'Print <i class="fas fa-print"></i>',
                autoPrint: false,
                className: 'btn btn-success btn-flat btn-xs'
            },
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
                pageSize: 'LEGAL',
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
            {data: "barrio_fullname"},
            {data: "manzana_fullname"},
            {data: "ci"},
            {data: "nombre"},
            {data: "apellido"},
            {data: "edad"},
            {data: "nro_casa"},
        ],
        columnDefs: [
            // {
            //     targets: [-4],
            //     class: 'text-center',
            //     render: function (data, type, row) {
            //         return data;
            //     }
            // },
            // {
            //     targets: [-1],
            //     class: 'text-center',
            //     render: function (data, type, row) {
            //         return data;
            //         // return '$' + parseFloat(data).toFixed(2);
            //     }
            // }
        ],
        rowCallback: function (row, data, index) {

        },
        initComplete: function (settings, json) {

        },

        rowGroup: {
            // startRender: null,
            endRender: function ( rows, group ) {
            return '<b>'+group +'</b> ('+rows.count()+')';
            },
            dataSrc: ["barrio_fullname","manzana_fullname"]
        },
        columnDefs: [ {
            targets: [ 0, 1 ],
            visible: false
        } ]
    });
}


$(function () {

    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');

    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            },
        });

    $('.drp-buttons').hide();

    initTable();

    generateReport(false);

    $('.btnSearchReport').on('click', function () {
        generateReport(false);
    });

    $('.btnSearchAll').on('click', function () {
        generateReport(true);
    });
});
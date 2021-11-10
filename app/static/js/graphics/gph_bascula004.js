function get_graph_4(currentYear,currentDate) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'get_graph_4'
        },
        dataType: 'json',
    }).done(function (request) {
        if (!request.hasOwnProperty('error')) {
            Highcharts.chart('graph_4', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: '</i><span style="font-size:20px; font-weight: bold;">Movimiento Clinker Año ' + currentYear + ' Actualizado: ' + currentDate + '</span>'
                },
                subtitle: {
                    text: ''
                },
                exporting: {
                    enabled: true
                },
                xAxis: {
                    categories: request.categories,
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'TOTALES'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y:.2f} TON</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.1,
                        borderWidth: 0,  
                        /**/
                        // stacking: 'normal', 
                        dataLabels: {
                            enabled: true
                        }                         
                    },
                    // series: {
                    //     dataLabels: {
                    //         enabled: true,
                    //         format: '<b>{point.y:.2f}',
                    //         style: {
                    //             fontSize: 20 + 'px'
                    //         }
                    //     }
                    // }
                },
                series: request.series
            });
         
            return false;
        }
        message_error(request.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {

    });
}
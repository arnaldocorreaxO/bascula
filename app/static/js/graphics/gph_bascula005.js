function get_graph_5(currentDate) {
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'get_graph_5'
        },
        dataType: 'json',
    }).done(function (request) {
        if (!request.hasOwnProperty('error')) {
            console.log(request.series);
            Highcharts.chart('graph_5', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: '</i><span style="font-size:20px; font-weight: bold;">Cantidad de Vehículos por Productos - ' + currentDate + '</span>'
                },
                subtitle: {
                    text: ''
                },
                exporting: {
                    enabled: true
                },
                xAxis: request.xAxis,
                yAxis: {
                    min: 0,
                    title: {
                        text: 'CANTIDAD DE VEHICULOS'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: { 
                        pointPadding: 0.2,
                        borderWidth: 0,
                        /**/
                        // stacking: 'normal',
                        dataLabels: {
                            enabled: true
                        }
                    },
                    series: {
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.y}',
                            style: {
                                fontSize: 20 + 'px'
                            }
                        }
                    }
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
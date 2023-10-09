
var input_daterange;
var input_timerange_in;
var input_timerange_out;
var input_timerange_in_out;
var input_time_in;
var input_time_out;
// INIT LOAD
$(function () {  
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');
    input_time_in =  $('input[name="time_in"]');
    input_time_out =  $('input[name="time_out"]');
    
    
    // RANGO DE FECHAS
    input_daterange
        .daterangepicker({
            language: 'auto',
            startDate: new Date(),
            locale: {
                format: 'YYYY-MM-DD',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {

        });
  
    // DESDE HORA ENTRADA
    input_time_in
        .daterangepicker({
            singleDatePicker:true,
            timePicker: true,
            timePicker24Hour: true,
            timePickerIncrement: 1,
            timePickerSeconds: true,
            locale: {
                format: 'HH:mm:ss'
            }
        }).on('show.daterangepicker', function (ev, picker) {
            picker.container.find(".calendar-table").hide();
        });
    // HASTA HORA SALIDA
    input_time_out
        .daterangepicker({
            singleDatePicker:true,
            timePicker: true,
            timePicker24Hour: true,
            timePickerIncrement: 1,
            timePickerSeconds: true,
            locale: {
                format: 'HH:mm:ss'
            }
        }).on('show.daterangepicker', function (ev, picker) {
            picker.container.find(".calendar-table").hide();
        });
    
    input_time_out.val('23:59:59')

    // #SUCURSAL POR DEFECTO 
    var sucursal_id = $('input[name="suc_usuario"]').val();   
    var select_sucursal = $('select[name="sucursal"]'); 
    select_sucursal.val(sucursal_id).change();
    // getData('all');
});
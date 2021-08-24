
var input_daterange;


// INIT LOAD
$(function () {  
    current_date = new moment().format('YYYY-MM-DD');
    input_daterange = $('input[name="date_range"]');    
    select_asociacion = $('select[name="asociacion"]');   

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

    // // BTN DEFAULT 
    // input_term.keypress(function(e){
    //     if(e.keyCode==13)
    //     $('.btnFilter').click();
    //   });


    // // Agregamos una linea vacia a los select
    
    // select_asociacion.append($("<option>", {
    //     value: '',
    //     text: '---------'
    //   })); 

    //  select_asociacion.val("").change();

});

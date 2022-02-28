var input_fecha;
var anho;
var usu_denom_corta;
var fec_hora_actual;
var mes_actual;
var anho_actual;


function load() {
    args = []
    //INPUT NO VISIBLES 
    usu_suc_denom_corta = $('input[name="usu_suc_denom_corta"]').val();
    fec_hora_actual = $('input[name="fecha_hora_actual"]').val();    
    mes_actual = $('input[name="mes_actual"]').val();
    anho_actual = $('input[name="anho_actual"]').val();

    // SUCURSAL
    suc_seleccion = $('select[name="sucursal"]').val();    
    suc_seleccion_texto = $('select[name="sucursal"] option:selected').text();    

    //NOMBRE DEL MES
    fec_seleccion = $('input[name="fecha"]').val();
    mes_seleccion = fec_seleccion.substring(3,5)
    mes_seleccion = obtenerNombreMes(mes_seleccion);
    mes_seleccion = mes_seleccion.charAt(0).toUpperCase() + mes_seleccion.slice(1) 

    // ANHO
    anho_seleccion = fec_seleccion.substring(6)       
    
    // console.log(fecha_seleccion)
    // console.log(mes_seleccion)
    // console.log(anho_seleccion)

    args.push(suc_seleccion_texto); //[0]
    args.push(fec_hora_actual);
    args.push(fec_seleccion);
    args.push(mes_seleccion);
    args.push(anho_seleccion); 
    args.push(suc_seleccion); 
    
    // console.log(anho_actual);

    get_graph_1_1(args);
    get_graph_1_2(args);
    get_graph_2_1(args);
    get_graph_2_2(args);
    get_graph_3(args);
    get_graph_4(args);
    get_graph_5(args);
    
};


$(function () {

    input_fecha = $('input[name="fecha"]');
    input_fecha
        .daterangepicker({
            language: 'auto',
            singleDatePicker: true,
            startDate: new Date(),
            locale: {
                format: 'DD/MM/YYYY',
            }
        })
        .on('apply.daterangepicker', function (ev, picker) {
            load();
        });


    /*ESTABLECER LA SUCURSAL ACTUAL EN EL DASHBOARD */
    // anho_actual = $('input[name="anho_actual"]').val(); 
    input_sucursal = $('input[name="usu_sucursal"]');
    select_sucursal = $('select[name="sucursal"]');

    /*AL CAMBIAR LA SUCURSAL*/
    select_sucursal.on('change', function () {
        load();
    });

    /*AMBOS METODOS FUNCIONA */
    // sucursal.val(sucursal_actual).trigger("change"); //Cambia valor y dispara el evento
    select_sucursal.val(input_sucursal.val()).change(); //Cambia valor y dispara el evento


    


  
});
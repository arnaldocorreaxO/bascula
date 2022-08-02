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

    // PRODUCTO
    sel_producto = $('select[name="producto"]').val();    
    sel_producto_texto = $('select[name="producto"] option:selected').text();    

    // SUCURSAL
    sel_sucursal = $('select[name="sucursal"]').val();    
    sel_sucursal_texto = $('select[name="sucursal"] option:selected').text();    

    //NOMBRE DEL MES
    sel_fecha = $('input[name="fecha"]').val();
    sel_mes = sel_fecha.substring(3,5)
    sel_mes = obtenerNombreMes(sel_mes);
    sel_mes = sel_mes.charAt(0).toUpperCase() + sel_mes.slice(1) 

    // ANHO
    anho_seleccion = sel_fecha.substring(6)       
    
    // console.log(fecha_seleccion)
    // console.log(sel_mes)
    // console.log(anho_seleccion)

    args.push(sel_sucursal_texto); //[0]
    args.push(fec_hora_actual);
    args.push(sel_fecha);
    args.push(sel_mes);
    args.push(anho_seleccion); 
    args.push(sel_sucursal);     
    args.push(sel_producto_texto); 
    args.push(sel_producto); 
    
    // console.log(anho_actual);

    get_graph_1_1(args);
    get_graph_1_2(args);
    get_graph_2_1(args);
    get_graph_2_2(args);
    get_graph_3(args);
    get_graph_4(args);
    get_graph_5(args);
    get_list(args);
    
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
    select_producto = $('select[name="producto"]');

    /*AL CAMBIAR LA SUCURSAL*/
    select_sucursal.on('change', function () {
        load();
    });
    /*AL CAMBIAR EL PRODUCTO*/
    select_producto.on('change', function () {
        load();
    });

    /*AMBOS METODOS FUNCIONA */
    // sucursal.val(sucursal_actual).trigger("change"); //Cambia valor y dispara el evento
    select_sucursal.val(input_sucursal.val()).change(); //Cambia valor y dispara el evento

});
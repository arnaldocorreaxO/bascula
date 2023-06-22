
//Validar Navegador Chrome
function isChrome(){
    if(/chrom(e|ium)/.test(navigator.userAgent.toLowerCase())){
    //   alert("estas en chrome");
      return true;
    }else{
        $('body').html('Esta web solo puede ser utilizada con el navegador <a href="https://www.google.com/chrome/">Google Chrome</a>');  
    }
   };

// Bloquear inspeccionar elemento
// Block inspect element 
function blockie() {
    // document.addEventListener("contextmenu", (e) => {
    //     e.preventDefault();
    // });
    window.addEventListener("keydown", (e) => {
        // e.preventDefault();
        // console.log(e);
        let handled = false;
        if (e.code == "F12") {
            // Handle the event with KeyboardEvent.key
            handled = true;
        }
        if (e.ctrlKey==true & e.shiftKey ==true & e.code == "KeyI") {
            // Handle the event with KeyboardEvent.key
            handled = true;
        }
        if (e.ctrlKey==true & e.code == "KeyU") {
            // Handle the event with KeyboardEvent.key
            handled = true;
        }
        if (handled) {
            // Suppress "double action" if event handled
            e.preventDefault();
        }
    },
        true
    )

}



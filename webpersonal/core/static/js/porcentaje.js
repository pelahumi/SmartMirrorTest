const progress = document.getElementById('progress');
let percentaje = document.getElementById('percentaje');
let contador = 0;
let cantidad = 630;
let resta = cantidad / 100 

let tiempo = setInterval(() => {
    contador += 1;
    let value = Math.ceil(cantidad -= resta);
    percentaje.textContent = `${contador}%`;
    progress.style.strokeDashoffset = value;

    if (contador === 100) {
        clearInterval(tiempo);
    }
}, 80);
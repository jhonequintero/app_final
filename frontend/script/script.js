

// Función para abrir la ventana emergente
function abrirPopup(id) {
    const popup = document.getElementById(id);
    if (popup) {
        popup.style.display = "block";
    }
}

// Función para cerrar la ventana emergente
function cerrarPopup(id) {
    const popup = document.getElementById(id);
    if (popup) {
        popup.style.display = "none";
    }
}

// Función para cambiar entre la vista de trabajador y admin
function cambiarVista(tipo) {
    const vistaTrabajador = document.getElementById('vistaTrabajador');
    const vistaAdmin = document.getElementById('vistaAdmin');

    if (tipo === 'admin') {
        vistaTrabajador.style.display = 'none';
        vistaAdmin.style.display = 'block';
    } else {
        vistaAdmin.style.display = 'none';
        vistaTrabajador.style.display = 'block';
    }
}




document.addEventListener('DOMContentLoaded', () => {
    const formularios = document.querySelectorAll('form');

    formularios.forEach(formulario => {
        formulario.addEventListener('submit', async (e) => {
            e.preventDefault(); // Evita que se recargue la página

            const tipo = formulario.querySelector('input[name="tipo"]').value;
            const correo = formulario.querySelector('input[name="correo"]');
            const contrasena = formulario.querySelector('input[name="contrasena"]');

            const datos = {
                tipo: tipo,
                correo: correo.value,
                contrasena: contrasena.value
            };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(datos)
                });

                const resultado = await response.json();

                // Mostrar mensaje como alert
                alert(resultado.mensaje);

                // Vaciar campos
                correo.value = '';
                contrasena.value = '';

                if (resultado.success) {
                    // Redirigir según el campo 'redireccion' de la respuesta
                    if (resultado.redireccion) {
                        window.location.href = resultado.redireccion;
                    }
                }

            } catch (error) {
                console.error('Error al enviar el formulario:', error);
                alert("Error al conectar con el servidor.");
            }
        });
    });
});









// style particulas 
particlesJS("particles-js", {
    particles: {
        number: {
            // value: 700,
            value: 80,
            density: {
                enable: true,
                value_area: 800
            }
        },
        color: {
            value: "#ffffff"
        },
        shape: {
            type: "circle"
        },
        opacity: {
            value: 0.5,
            random: false
        },
        size: {
            value: 3,
            random: true
        },
        line_linked: {
            enable: true,         // Las partículas se conectan entre sí
            distance: 150,
            color: "#ffffff",
            opacity: 0.4,
            width: 1
        },
        move: {
            enable: true,
            speed: 1.5,
            direction: "none",
            out_mode: "out"
        }
    },
    interactivity: {
        detect_on: "canvas",
        events: {
            onhover: {
                enable: true,
                mode: "grab" // Este modo hace que el cursor conecte partículas como si las tocara
            },
            onclick: {
                enable: false
            }
        },
        modes: {
            grab: {
                distance: 180, // Distancia a la que el cursor "agarra" partículas
                line_linked: {
                    opacity: 1 // Qué tan fuerte se ve la línea del cursor a la partícula
                }
            }
        }
    },
    retina_detect: true
});




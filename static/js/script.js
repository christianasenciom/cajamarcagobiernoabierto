document.addEventListener('DOMContentLoaded', function() {
    const banner = document.querySelector('.banner-container');

    // Lógica para cambiar algo cuando el mouse pasa por encima
    banner.addEventListener('mouseover', function() {
        // Aquí podrías agregar interactividad avanzada si la necesitas
    });

    banner.addEventListener('mouseout', function() {
        // Aquí podrías agregar interactividad avanzada si la necesitas
    });
});

function showModal() {
    document.getElementById('modal').style.display = 'flex';
}

function hideModal() {
    document.getElementById('modal').style.display = 'none';
}
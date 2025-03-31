document.addEventListener('DOMContentLoaded', function() {
    // Manejar clicks en los enlaces del sidebar
    document.querySelectorAll('.sidebar-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Actualizar clase activa
            document.querySelectorAll('.nav-item').forEach(item => {
                item.classList.remove('active');
            });
            this.parentElement.classList.add('active');
            
            // Cargar contenido dinámicamente
            fetch(this.href)
                .then(response => response.text())
                .then(html => {
                    // Extraer solo el contenido del bloque
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newContent = doc.querySelector('#content-container').innerHTML;
                    
                    // Actualizar el contenido principal
                    document.getElementById('main-content').innerHTML = newContent;
                    
                    // Actualizar el título de la página
                    const newTitle = doc.querySelector('title').textContent;
                    document.title = newTitle;
                    
                    // Cambiar la URL sin recargar
                    history.pushState(null, newTitle, this.href);
                })
                .catch(err => console.error('Error loading page:', err));
        });
    });
    
    // Manejar el botón de retroceso/avance del navegador
    window.addEventListener('popstate', function() {
        fetch(window.location.pathname)
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('#content-container').innerHTML;
                document.getElementById('main-content').innerHTML = newContent;
                document.title = doc.querySelector('title').textContent;
                
                // Actualizar el elemento activo en el sidebar
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                const currentPath = window.location.pathname;
                document.querySelectorAll('.sidebar-link').forEach(link => {
                    if (link.getAttribute('href') === currentPath) {
                        link.parentElement.classList.add('active');
                    }
                });
            });
    });
});
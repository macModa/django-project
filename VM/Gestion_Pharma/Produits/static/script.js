document.querySelector(".jsFilter").addEventListener("click", function () {
  document.querySelector(".filter-menu").classList.toggle("active");
});

document.querySelector(".grid").addEventListener("click", function () {
  document.querySelector(".list").classList.remove("active");
  document.querySelector(".grid").classList.add("active");
  document.querySelector(".products-area-wrapper").classList.add("gridView");
  document
    .querySelector(".products-area-wrapper")
    .classList.remove("tableView");
});

document.querySelector(".list").addEventListener("click", function () {
  document.querySelector(".list").classList.add("active");
  document.querySelector(".grid").classList.remove("active");
  document.querySelector(".products-area-wrapper").classList.remove("gridView");
  document.querySelector(".products-area-wrapper").classList.add("tableView");
});

var modeSwitch = document.querySelector('.mode-switch');
modeSwitch.addEventListener('click', function () {                      document.documentElement.classList.toggle('light');
 modeSwitch.classList.toggle('active');
});

// Delete button AJAX logic for product rows
if (document.querySelectorAll('.delete_button').length) {
  document.querySelectorAll('.delete_button').forEach(function(button) {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      var produitId = button.getAttribute('data-id');
      if (confirm("Êtes-vous sûr de vouloir supprimer ce produit ?")) {
        fetch('/produits/suprimer/' + produitId + '/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json',
          },
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            button.closest('.products-row').style.transition = 'opacity 0.3s';
            button.closest('.products-row').style.opacity = 0;
            setTimeout(function() {
              button.closest('.products-row').remove();
            }, 300);
            alert(data.message);
          } else {
            alert('Erreur: ' + data.message);
          }
        })
        .catch(error => {
          alert('Erreur technique: ' + error);
        });
      }
    });
  });
}



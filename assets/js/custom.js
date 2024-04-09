(function($) {
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("menu");
  var close = document.getElementById("menu-close");

  toggle.addEventListener("click", function(e) {
    if (menu.classList.contains("open")) {
      menu.classList.remove("open");
    } else {
      menu.classList.add("open");
    }
  });

  close.addEventListener("click", function(e) {
    menu.classList.remove("open");
  });

  // Close menu after click on smaller screens
  $(window).on("resize", function() {
    if ($(window).width() < 846) {
      $(".main-menu a").on("click", function() {
        menu.classList.remove("open");
      });
    }
  });

  $(".owl-carousel").owlCarousel({
    items: 4,
    lazyLoad: true,
    loop: true,
    dots: true,
    margin: 30,
    responsiveClass: true,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 1
      },
      1000: {
        items: 1
      }
    }
  });

  $(".hover").mouseleave(function() {
    $(this).removeClass("hover");
  });

  $(".isotope-wrapper").each(function() {
    var $isotope = $(".isotope-box", this);
    var $filterCheckboxes = $('input[type="radio"]', this);

    var filter = function() {
      var type = $filterCheckboxes.filter(":checked").data("type") || "*";
      if (type !== "*") {
        type = '[data-type="' + type + '"]';
      }
      $isotope.isotope({ filter: type });
    };

    $isotope.isotope({
      itemSelector: ".isotope-item",
      layoutMode: "masonry"
    });

    $(this).on("change", filter);
    filter();
  });

  lightbox.option({
    resizeDuration: 200,
    wrapAround: true
  });
})(jQuery);



window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  var topButton = document.getElementById("topBtn");
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      topButton.style.display = "block";
  } else {
      topButton.style.display = "none";
  }
}

function topFunction() {
  var scrollAnimation = setInterval(function(){
     document.body.scrollTop -= 50;
     document.documentElement.scrollTop -= 50;

     if(document.body.scrollTop === 0 && document.documentElement.scrollTop === 0){
         clearInterval(scrollAnimation); 
     }
  }, 10);
}


// var isNight = true;
// function switchNightDay() {
//   var bodyElt = document.getElementById('page-wraper'); 
//   var iconElt = document.getElementById('icon');
//   if (isNight) {
//       bodyElt.style.setProperty('background-image', 'url("/assets/images/page-bg.jpg")');
//       iconElt.className  = 'fa fa-sun-o';
//       isNight = false;
//   } else {
//       bodyElt.style.setProperty('background-image', 'url("/assets/images/page-bg2.jpg")');
//       iconElt.className = "fa fa-moon-o";
//       isNight = true;
//   }
// }

// function toggleNav() {
//     var element = document.getElementById("navOverlay");
//     element.style.display = (element.style.display == 'none') ? 'block' : 'none';
// }

// <button onclick="switchNightDay();" id="NigthDayBtn">
// <span id="icon" class="button fa fa-moon-o"></span>
// </button>


$(document).ready(function() {
  function resizeIframe() {
      var containerHeight = $('#iframeContainer').height();
      $('#googleSheet').height(containerHeight);
  }

  // Appeler resizeIframe au chargement de la page
  resizeIframe();

  // Appeler resizeIframe à chaque redimensionnement de la fenêtre
  $(window).resize(function() {
      resizeIframe();
  });
});
$(document).ready(function () {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    $(".heart").addClass(heart_blast_js);
  });
  $(function () {
    $(".heart").on("click", function () {
        if (is_authenticated == "true") $(this).toggleClass("heart-blast");
    });
  });

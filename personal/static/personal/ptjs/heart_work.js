  $(function () {
    $(".love").on("click", function () {
        if (is_authenticated) $(this).toggleClass("loved");
      });
  });

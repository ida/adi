(function($) {
  $(document).ready(function() {
    var interval_ms = 7277
    var url = window.location.href
    reload_interval = setInterval(function () {
      window.location.reload()
    }, interval_ms);

    $('body').prepend('<a href=#"'+ url + '" class="stop" style="position:fixed;top:0;right:0;z-index:27;">stop</div>')
    $($('body > .stop:first-child')[0]).click(function(eve) {
      eve.preventDefault()
      clearInterval(reload_interval)
      $(this).remove()
    });

  }); //docready
})(jQuery);

(function($) { $(document).ready(function() {
  //$("<div>++resource++adi.info.resources/main.js loaded</div>").insertBefore("#visual-portal-wrapper")
  if($('.portalMessage').length > 0) {
    $('.portalMessage').each(function() {
      $(this).html('<div class="closeMsg">x</div>' + $(this).html())
      $('.closeMsg').css('float','right')
      $('.closeMsg').click(function() {
        $(this).parent().remove()
      });
      $(this).animate({opacity: 0}, 7000, function() {
        $(this).remove()
      });
    });
  }

}); })(jQuery);

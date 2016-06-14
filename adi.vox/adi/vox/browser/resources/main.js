(function($) { $(document).ready(function() {
// Abuse #portal-column-one for showing the history of an argument
// when viewing it:
if($('.template-document_view.portaltype-pro').length > 0
  || $('.template-document_view.portaltype-contra').length > 0) {
  var history_url = document.location.href + 
    '/@@contenthistorypopup?ajax_load=' +
    Date.now()
  $('#portal-column-one').load(history_url + ' #content',
    function () {
    $('#portal-column-one h2').remove()
    }
  );
}
}); })(jQuery);

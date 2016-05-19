// Defines which ele is to be focused by default, when loading a page,
// depending on the given context (landingpage/editmode/etc):
document.addEventListener("DOMContentLoaded", function(event) { 
  // Editmode archetypes:
  if(document.getElementsByClassName('template-atct_edit').length > 0) {
    document.getElementById('title').focus()
  }
});
/* Keeping for reference: Use jq and bind dollar-sign to it:
(function($) {
    $(document).ready(function() {
    }); //docready
})(jQuery);
*/

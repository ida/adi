function listenLoadLinks(loaderParent) {
  // Expects a div containing a link with class 'loadLink',
  // and a next sibling with class 'linkLoader',
  // loads the destination's #content-element into 'linkLoader'.
  $(loaderParent).find('.loadLink').each(function() {
    $(this).click(function(eve) {
      eve.preventDefault()
      var link = $(eve.target)
      var loader = $($(link).find('~ .linkLoader')[0])
      var href = link.attr('href')
      // #content-core is loaded already ...
      if(loader.find('> #content-core').length > 0) {
        // ... hide, respectively show it:
        if( 
            $(loader.find('> #content-core')[0]).css('display') != 'none') {
              $(loader.find('> #content-core')[0]).css({'display':'none'});
              // Switch arrow-symbol of load-link from up to down:
              link.html('&darr;')
        }
        else {
          $(loader.find('> #content-core')[0]).css({'display':'block'});
              // Switch arrow-symbol of load-link from down to up:
              link.html('&uarr;')
        }
      }
      // #content-core is not loaded, yet ...
      else {
        // ... load it:
        loader.load(
          href + ' #content-core',
          // After loading, re-apply listeners to new loaded links:
          function() {
            loaderParent = $(loader.find('.children')[0])
            listenLoadLinks(loaderParent)
            // And swith arrow-down to up:
            link.html('&uarr;')
          }
        );
      }
    });
  });
}
function manipulateAuthorTemplate() {
  if($('.template-author').length > 0) { // context is author-template
      $('#content').html('')             // let content-area dissapear first
      var userId = window.location.pathname.split('/')  // prep var
      var siteId = userId[1]                            // get var
      userId = userId[userId.length-1]                  // get var
      // Load results-area of search-template with userid passed
      // into content-area:
      $('#content').load(
        portal_url + '/search?getResponsiblePerson=' + 
        userId + '&sort_on=created&sort_order=reverse #search-results',
        // Afterwards prepend a heading:
        function() {
          $('#content').prepend('<h2>Steps ' + userId + ' is responsible for:')
        }
      ); // load
  } // is author-template
}
(function($) { $(document).ready(function() {
  manipulateAuthorTemplate()
  if($('.template-adi_tickets_main_view').length > 0
    && $('#content .children').length > 0) {
      var loaderParent = $('#content .children')[0]
      listenLoadLinks(loaderParent)
  }
/* DEV:
$($('.portletHeader')[0]).click(function(eve) {
  eve.preventDefault()
  $('#portal-column-one').remove()
});
*/
// autoload:
function autoLoad() {
$('.loadLink').each(function() {
  if($(this).find('#content-core').length < 1) {
    $(this).click()
  }
});
}
}); })(jQuery);

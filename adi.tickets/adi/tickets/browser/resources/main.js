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
      console.log('// schon loaded')
        // ... hide, respectively show it:
        if( $(loader.find('> #content-core')[0]).hasClass('loaded') &&
            $(loader.find('> #content-core')[0]).css('height') === undefined ||
            $(loader.find('> #content-core')[0]).css('height') == '0px') {
              $(loader.find('> #content-core')[0]).css({'height':'auto'});
        }
        else {
          $(loader.find('> #content-core')[0]).css({'height':'0', 'overflow':'hidden'});
        }
      }
      // #content-core is not loaded, yet ...
      else {
      console.log('// #content is not loaded, yet...')
        // ... load it:
        loader.load(
          href + ' #content-core',
          // After loading, re-apply listeners to new loaded links:
          function() {
            loaderParent = $(loader.find('ol')[0])
            listenLoadLinks(loaderParent)
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
    && $('#content ol').length > 0) {
      var loaderParent = $('#content ol')[0]
      listenLoadLinks(loaderParent)
  }
}); })(jQuery);

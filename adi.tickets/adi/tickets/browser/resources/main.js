var max_loads = 10
function loadStep(link, loader) {
  if(max_loads > 0) {
    // Asumes children aren't loaded, yet.
    loader.load(
      $(link).attr('href') + ' #content-core',
      // After loading ...
      function() {
        loaderParent = $(loader.find('.children')[0])
        // ... re-apply listeners to new loaded links:
        listenLoadLinks(loaderParent)
        // DEV: AUTOLOAD:
        //setTimeout(function(){loaderParent.find('.loadLink').click()},1027)
        loaderParent.find('.loadLink').click()
      }
    );
  max_loads -= 1
  }
}
function listenLoadLinks(loaderParent) {
  // Looks for children of loaderParent with class 'loadLink',
  // and a next sibling with class 'linkLoader',
  // loads the destination's '#content'-element into 'linkLoader'.
  $(loaderParent).find('.loadLink').each(function() {
    $(this).click(function(eve) {

      eve.preventDefault()

      var link = $(eve.target)
      var loader = $($(link).find('~ .linkLoader')[0])

      // #content-core is loaded already ...
      if(loader.find('> #content-core').length > 0) {
        // ... it's visible, hide it:
        if($(loader.find('> #content-core')[0]).css('display') != 'none') {
          $(loader.find('> #content-core')[0]).css({'display':'none'});
          link.html('&darr;') // arrow-down
        }
        // ... it's invisible, show it:
        else {
          $(loader.find('> #content-core')[0]).css({'display':'block'});
              link.html('&uarr;') // arrow-up
        }
      }
      // #content-core is not loaded, yet ...
      else {
        // ... load it:
        loadStep(link, loader)
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
  $('.loadLink').click() // ini
}); })(jQuery);

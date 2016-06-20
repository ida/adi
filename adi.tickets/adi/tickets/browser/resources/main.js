function loadStep(link, loader, max_autoload_depth) {
    // Assumes children aren't loaded, yet.
    loader.load(
      $(link).attr('href') + ' #content-core',
      // After loading ...
      function() {
        link.html('&uarr;') // arrow-up
        //  ... disable author-link in children, for quicker tabbing:
        $('.children .creator').each(function() {
        $(this).html($(this).text()) 
        });
        // ... re-apply listeners to new loaded links:
        loaderParent = $(loader.find('.children')[0])
        max_autoload_depth = listenLoadLinks(loaderParent, max_autoload_depth)
        // DEV: AUTOLOAD:
        if(max_autoload_depth > 0) {
          //setTimeout(function(){
            loaderParent.find('.loadLink').click()
          //}, 1027);
        }
      }
    );
  max_autoload_depth -= 1
  return max_autoload_depth
}
function listenLoadLinks(loaderParent, max_autoload_depth) {
  // Looks for children of loaderParent with class 'loadLink',
  // and a next sibling with class 'linkLoader',
  // loads the destination's '#content'-element into 'linkLoader'.
  $(loaderParent).find('.loadLink').each(function() {
    $(this).click(function(eve) {

      eve.preventDefault()

      var link = $(eve.target)
      var loader = $($(link).parent().find('.linkLoader')[0])

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
        max_autoload_depth = loadStep(link, loader, max_autoload_depth)
      }
    });
  });
  return max_autoload_depth
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
function main(max_autoload_depth=0) {
  if($('.template-adi_tickets_main_view').length > 0
    && $('#content .children').length > 0) {
      var loaderParent = $('#content .children')[0]
      listenLoadLinks(loaderParent, max_autoload_depth)
  }
}
(function($) { $(document).ready(function() {
  main()
  //main(27)
  //$('.loadLink').click() // ini autoload
  //manipulateAuthorTemplate()
}); })(jQuery);

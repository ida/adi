function clickArrowUpScrollItemHeadToTop(eve) {
  var link = $(eve.target)
  var href = eve.target.getAttribute('href')
  window.location = href
}
function loadStep(link, loader, max_autoload_depth) {
    // Assumes children aren't loaded, yet.
    loader.load(
      $(link).attr('href') + ' #content-core',
      // After loading ...
      function() {
        link.html('&uarr;') // arrow-up
        //  ... transform author-link in children to 
        //  plain text, for quicker tabbing:
        $('.children .creator').each(function() {
          $(this).html($(this).text()) 
        });
        //  ... remove edit-buttons-links in children 
        //  of the tabflow, for quicker tabbing:
        $('.children .buttons a').each(function() {
          $(this).css('border','1px solid red')
          $(this).attr('tabindex', '-1')
        });
        // ... re-apply listeners to new loaded links:
        loaderParent = $(loader.find('.children')[0])
        max_autoload_depth = listenLoadLinks(loaderParent, max_autoload_depth)
        // Load next children if max_autoload_depth is not exceeded:
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
              clickArrowUpScrollItemHeadToTop(eve)
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
function manipulateTopicTabularView() { 
  var context_condition = $('.portaltype-stepbystep')
  if(context_condition.length > 0) { // TODO: pass current date
    var query = '/@@search?advanced_search=False&sort_on=&SearchableText='
              + '&portal_type%3Alist=Stepbystep&expires.query%3Arecord%3Alist'
              + '%3Adate=2016-06-24&expires.range%3Arecord=max'
    // Mind and keep the space before the '#' !
    var url = window.location.href + query + ' #search-results'
    // Load:
    $('#due-end-date-passed').load(url, function() {
        // Has not ele with txt 'No results found'
        var no_results_found_ele = $(this).find('strong')
      // After load:
console.log(no_results_found_ele.length)
      if(no_results_found_ele.length > 0) {
        no_results_found_ele.remove()
        $(this).find('.discreet').remove() // author, mod-date, item-path
      }
      else {
        $(this).prepend('<div class="header warning">Attention! These steps have passed the due end-time already:</div>')
      }
    });
  }
}
function manipulateAuthorTemplate() { // TODO: context is app
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
  if($('.template-adi_stepbysteps_main_view').length > 0
    && $('#content .children').length > 0) {
      var loaderParent = $('#content .children')[0]
      listenLoadLinks(loaderParent, max_autoload_depth)
  }
  document.body.onkeypress = function(eve) {
    if(eve.keyCode == 20) {
      eve.preventDefault()
      $(eve.target).click()
    }
  }
}
(function($) { $(document).ready(function() {
  manipulateTopicTabularView() // prototype
  manipulateAuthorTemplate() // prototype
  var max_autoload_depth = 0
  main(max_autoload_depth)
//  $('.loadLink').click() // (auto-)load 1st children
}); })(jQuery);

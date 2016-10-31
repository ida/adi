function loadLink(link, loadLinkClass) {
  var href = link.attr('href')
  var anchorId = ''
  var loadContainer = null
  var loadedEle = null
  if(href.indexOf('#') != -1) {
    href = href.split('#')
    anchorId = href[1]
    href = href[0]
  }
// If we have a link with class showChildren; prepend to parent,
// if link we have a link with class loadText; insert after step-title:
if( link.hasClass('showText') ) {
  // Create wrapper to load dest into:
  link.parent().append('<div class="loadWrapper"></div>')
  // Grab the newly created wrapper:
  loadContainer = link.find('~ div.loadWrapper')
}
else {
  loadContainer = $('<div class="loadWrapper"></div>')
                  .insertAfter( link.parent() )
}
  // Load destination into wrapper:
  loadContainer.load(href + ' #' + anchorId, function() {
    // Fetch loaded content:
    loadedEle = loadContainer.find('#' + anchorId)
    // Now the wrapper has become superfluous, remove it:
    loadedEle.unwrap()
    // Apply click-listener to the new loaded links:
    onLoadLinkClick(loadedEle, loadLinkClass, anchorId)
    // Switch button for show/hide children-button:
    toggleChildrenButtons(link)
  });
}
function onLoadLinkClick(container, loadLinkClass) {
  // On click, check if content is already loaded,
  // if so, switch its visibility, if not, load content intially.
  container.find('.' + loadLinkClass).click(function(eve) {
    eve.preventDefault()
    var link = $(eve.target)
    var anchorId = link.attr('href').split('#')[1]
    var content = $(link.parent().parent().find('#' + anchorId)[0]) // only 1st
    // Content has not been loaded yet, load it:
    if(content.length < 1) {
      loadLink(link, loadLinkClass, anchorId)
    }
    // Otherwise only toggle visibility:
    else {
      content.toggle()
      toggleChildrenButtons(link)
    }
  });
}
function toggleChildrenButtons(link) {
// TODO improve: Do not merely switch class-name,
// but really check, if content is visible or not,
// because beleaving is good, yet proving is better.
  if(link.hasClass('showChildren')) {
    link.removeClass('showChildren'); link.addClass('hideChildren')
  }
  else if(link.hasClass('hideChildren')) {
    link.removeClass('hideChildren'); link.addClass('showChildren')
  }
  else if(link.hasClass('showText')) {
    link.removeClass('showText'); link.addClass('hideText')
  }
  else if(link.hasClass('hideText')) {
    link.removeClass('hideText'); link.addClass('showText')
  }
}
function onSpacebarPress(container) {
  container.keypress(function(eve) { // a key is pressed
    if(eve.keyCode == '0') { // it's the spacebar
      eve.target.click() // simulate click on focused/active-ele
    }
  });
}
function alertOverdues(container) {
// http://www.stackoverflow.com/questions/24744466/how-to-search-content-using-a-date-range-on-plone
  var href = 'http://localhost:8080/Plone/@@search?portal_type:list=Stepbystep&expires.query:date:list:record=2017/01/02%2000%3A00%3A00%20GMT%2B0&expires.range:record=max'
  var anchorId = 'search-results'
  // Or, load results of pre-populated collection (see '../../setuphandlers.py'),
  // that'll give us atble-view qith the xpiraton-date shown:
  href = 'http://localhost:8080/Plone/0/overviews/overdue'
  anchorId = 'content-core'

  // Provide ele to load content into, prepend it to container-children:
  var loadEle = $('<div></div>').insertBefore($(container.find('> *')[0]))
  loadEle.load(href + ' #' + anchorId, function() { // load into ele
    loadEle.find('a').attr('tabindex', '-1') // inhibit links in ele of tabbing
  });
}
(function($) { $(document).ready(function() {
  var container  = $(document.body)
  var loadLinkClass = 'loadLink'
  onLoadLinkClick(container, loadLinkClass) // apply listener
  onSpacebarPress(container)
  alertOverdues(container)
}); })(jQuery);

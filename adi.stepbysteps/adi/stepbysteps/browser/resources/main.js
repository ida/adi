function loadLink(link, loadLinkClass) {
  var href = link.attr('href')
  var destId = ''
  if(href.indexOf('#') != -1) {
    href = href.split('#')
    destId = href[1]
    href = href[0]
  }
  // Create wrapper to load dest into:
  link.parent().append('<div class="loadWrapper"></div>')
  // Grap the newly created wrapper:
  var loadContainer = link.find('~ div.loadWrapper')
  // Load:
  loadContainer.load(href + ' #' + destId, function() {
    // Fetch loaded content:
    var loadedEle = loadContainer.find('#' + destId)
    // Now the wrapper has become superfluous, remove it:
    loadedEle.unwrap()
    // Apply this listener to the new loaded links:
    loadLinkClick(loadedEle, loadLinkClass, destId)
    // Show first children of new loaded content:
    toggleChildren(link)
  });
}
function loadLinkClick(container, loadLinkClass) {
  // On click, check if content is already loaded,
  // if so, switch its visibility, if not, load content intially.
  container.find('.' + loadLinkClass).click(function(eve) {
    eve.preventDefault()
    var link = $(eve.target)
    var destId = link.attr('href').split('#')[1]
    var content = link.find('~ #' + destId)
    // Content has not been loaded yet, load it:
    if(content.length < 1) {
      loadLink(link, loadLinkClass, destId)
    }
    // Otherwise only toggle visibility:
    else {
      content.toggle()
      toggleChildren(link)
    }
  });
}
function toggleChildren(link) {
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
(function($) { $(document).ready(function() {
  var container  = $(document.body)
  var loadLinkClass = 'loadLink'
  loadLinkClick(container, loadLinkClass) // apply listener
}); })(jQuery);

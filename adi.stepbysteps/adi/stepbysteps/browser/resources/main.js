function loadLink(link, loadLinkClass, loadDestId) {
  // Get dest-url and append ele-id to load:
  var href = link.attr('href') + ' #' + loadDestId
  // Create wrapper to load dest into:
  link.parent().append('<div class="loadWrapper"></div>')
  // Grap the newly created wrapper:
  var loadContainer = link.find('~ div.loadWrapper')
  // Load:
  loadContainer.load(href, function(doAfter) {
    // Fetch loaded content:
    var loadedEle = loadContainer.find('#' + loadDestId)
    // Now the wrapper has become superfluous, remove it:
    loadedEle.unwrap()
    // Apply this listener to the new loaded links:
    loadLinkClick(loadedEle, loadLinkClass, loadDestId)
    // Show first children of new loaded content:
    toggleChildren(link)
  });
}
function loadLinkClick(container, loadLinkClass, loadDestId) {
  // On click, check if content is already loaded,
  // if so, switch visibility, if not, load content.
  container.find('.' + loadLinkClass).click(function(eve) {
    eve.preventDefault()
    var link = $(eve.target)
    var content = link.find('~ #' + loadDestId)
    // Content has not been loaded yet, load it:
    if(content.length < 1) {
      loadLink(link, loadLinkClass, loadDestId)
    }
    else {
      content.toggle()
      toggleChildren(link)
    }
  });
}
function toggleTextClick() {
  $('.showText').click(function() {
    $(this).addClass('hideText').removeClass('showText').text('-')
    toggleTextClick() // re-apply this listener
  });
  $('.hideText').click(function() {
    $(this).removeClass('hideText').addClass('showText').text('+')
    toggleTextClick() // re-apply this listener
  });
}
function toggleChildren(link) {
  if(link.hasClass('showChildren')) {
    link.removeClass('showChildren'); link.addClass('hideChildren')
  }
  else if(
    link.hasClass('hideChildren')) {
    link.removeClass('hideChildren'); link.addClass('showChildren')
  }
}
(function($) { $(document).ready(function() {
  var container  = $(document.body)
  var loadLinkClass = 'loadLink'
  var loadDestId = 'content-core'
  toggleTextClick() // apply listener
  loadLinkClick(container, loadLinkClass, loadDestId) // apply listener
}); })(jQuery);

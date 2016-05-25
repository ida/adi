(function($) { $(document).ready(function() {
  // Look for eles with class loader,
  // look for its id, use as target-link,
  // load target-link's #content-core into ele.
  $('.loader').each(function(i, loader) {
    $(loader).load(loader.id + ' #content')
  });
}); })(jQuery);

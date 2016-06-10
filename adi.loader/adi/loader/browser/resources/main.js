(function($) { $(document).ready(function() {
  // Look for eles with class 'loader',
  // gets url to load of its data-src-attribute,
  // defaults to load div#content of url only, unless
  // otherwise specified as an optional paramater, e.g.:
  // <div class="loader" data-src="../folder-id/file-id#content-core" />
  // Or without, falling back to #content:
  // <div class="loader" data-src="../folder-id/file-id" />
  // .look for its id, use as target-link,
  // if id contains a space, last word is id to load
  // otherwise take '#content'.
  $('.loader').each(function(i, loader) {
    var load_url = loader.getAttribute('data-src')
    var load_id = 'content'
    if(load_url.split('#').length > 1) {
      load_id = load_url.split('#')[1]
      load_url = load_url.split('#')[0]
    }
    $(loader).load(load_url + ' #' + load_id)
  });
}); })(jQuery);

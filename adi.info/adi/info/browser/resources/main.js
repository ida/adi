var info_mss_css = ''


function handlePortalMsgs(container, msgsClass) {
  var msgs = $('.' + msgsClass)
  var scnds = 6
  // For each found msg:
  msgs.each(function() {
    // Add close- and stick-button to msg:
    $(this).html('<div class="msgCountdown">' + scnds + '</div><div class="msgStick vanish">stick</div><div class="msgClose">close</div>' + $(this).html())
  });
  // If user clicks stick-button:
  $('.msgStick').click(function(eve) {
    // Remove class vanish:
    $(eve.target).removeClass('vanish')
  });
  // If user clicks close-button:
  $('.msgClose').click(function(eve) {
    // Remove msg:
    $(eve.target).parent().remove()
  });
  // Countdown:
  $('.msgCountdown').each(function() {
    var o = scnds
    var msg = $(this)
    for(var i=-1;i<scnds;i++) {
      setTimeout(function() {
        msg.html(String(o))
        o -=1
      }, i*1000);
    }
  });
  // Wait 5 seconds, so user has time to click stick-button:
  setTimeout(function() {
    // If user didn't click stick-button and vanish-classes are still present:
    $('.vanish').each(function() {
      // Let msg vanish (fade-out) and remove leftovers, like good scouts do:
      $(this).parent().animate( {opacity:0}, 2777, function() { $(this).remove() } )
    });
  }, 4213);
}
// On page load:
(function($) { $(document).ready(function() {
  var container = $(document.body)
  var msgsClass = 'portalMessage'
  handlePortalMsgs(container, msgsClass)
}); })(jQuery);

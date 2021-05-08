 /*
  * Message Plugin
  * 
  * Author : dreamcog
  * Website: dreamcog.com
  * 
  */
!function ($) {

    $.dreamAlert =  function (options) {
        var settings = {
            'base_path' :   '../source/',
            'type'      :   'success',
            'message'   :   'Operation completed',
            'summary'   :   '',
            'icon'      :   '',
            'position'  :   'center',
            'message_id':   1,
            'duration'  :   3000,
            'id'        :   0
        }
        $.extend(settings, options);
        
        dreamalert = {
            'init'  :   function() {
                if ($('#dmalert').length == 0) {
                    $('body').append("<div id='dmalert'><div id='dma_right'></div><div id='dma_center'></div></div>");
                }
                this.show(settings.message);
            },
            'set'   :   function(options) {
                $.extend(settings, options);
            },
            'close' :   function() {
                $('.dream_alert').fadeOut();
            },
            'get_html'  :   function(message) {
                return  '<div id="dreamAlert'+$.dreamAlert.message_id+'" class="dream_alert dream_'+settings.position+' clearfix"><div class="alert-icon alert-icon-'+settings.type+' alert-icon-'+settings.position+'"></div><span>'+message+'</span></div>'; 
            },
            'show'   :   function(message) {
                $.dreamAlert.message_id += 1;
                var message_id = $.dreamAlert.message_id;
                var alert_html = this.get_html(message);
                if (settings.position == 'center') {
                    $('#dma_center').append(alert_html);
                    var w = - $('#dreamAlert'+message_id).width() / 2;
                    var h = - $('#dreamAlert'+message_id).height() / 2;
                    $('#dreamAlert'+message_id).css('margin-left',w).css('margin-top',h);
                }else {
                    $('#dma_right').prepend(alert_html);
                }

                if (settings.type != 'loading') {
                    console.log('fadeout');
                    setTimeout("$('#dreamAlert"+message_id+"').fadeOut('normal',function() {$('#dreamAlert"+message_id+"').remove();});",settings.duration);
                }else {
                    return message_id
                }

            }

        }
        dreamalert.init();
    }
    
    $.dreamAlert.message_id = 1;
    $.dreamAlert.close = function(options) {
        $('.dream_alert').fadeOut();
    }

}(window.jQuery);
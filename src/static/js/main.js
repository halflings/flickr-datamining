/* Misc */
var markdown = new Showdown.converter();

var preprocessText = function(msg) {
    return msg.replace(/(\r\n|\n|\r)/gm, '<br>').replace(/ /g, '&nbsp;');
}


/* Handlebars */
loadTemplate = function(template_id) {
    var source = $(template_id).html();
    return Handlebars.compile(source);
}

Handlebars.registerHelper('breaklines', function(text) {
    text = Handlebars.Utils.escapeExpression(text);
    text = preprocessText(text);
    return new Handlebars.SafeString(text);
});

Handlebars.registerHelper('fixedDecimal', function(number) {
  return number.toFixed(4);
});


/* API related */
var apiCall = function(path, method, data, callback) {
	$.ajax({
	  url: path,
	  type: method,
	  async: true,
	  dataType: "json",
	  data: JSON.stringify(data),
	  contentType: 'application/json;charset=UTF-8',
	  success: callback
	});
};

/* Notification zone */
notification = {
    show: function(cls, msg) {
        msg = preprocessText(msg);
        $('#notification-bar').attr('class', cls).stop().html(msg).fadeIn(300).delay(2000).fadeOut(500);
    },
    error: function(msg) {
        this.show('error', msg);
    },
    warning: function(msg) {
        this.show('warning', msg);
    },
    info: function(msg) {
        this.show('info', msg);
    },
    success: function(msg) {
        this.show('success', msg);
    }
}

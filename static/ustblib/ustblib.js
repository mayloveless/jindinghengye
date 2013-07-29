;(function(window){
	$(document).ready(function(){
		if(!$('#info')[0]){
			return;
		};
		var ison  = $.trim($('#info').text().split('ISBN:')[1]);
		var uid = $.trim($('.nbg').attr('title').split('uid:')[1].split(',')[0])
		if($('#ustblib')[0]){
			$('#ustblib').remove();
		}
		var i = '<iframe id="ustblib" style="width:630px;height:280px;" frameborder="0" scrolling="no" src="http://wangaibing.sinaapp.com/ustblib?ison='+ison+'&uid='+uid+'"></iframe>';
		$('.subjectwrap').after(i);
	});
})(window);
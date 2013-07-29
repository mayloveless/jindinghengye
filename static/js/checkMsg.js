$(document).ready(function(){

	var status = location.href.split('status=')[1];
	if(status){
		if(status === '1'){
			$('#status').text('已读留言');
		}else{
			$('#status').text('未读留言');
		}
	}

	$('.msgList').bind('click',function(){
		var mid = $($(this).children()[0]).text();

		$.post('/admin/read',{mid:mid},function(res){
			alert('此留言标记已读');
			location.href = location.href;
		});
	});	

	$('#markAll').bind('click',function(){
		var midArr = [];
		$('.msgList').each(function(){
			var mid = $($(this).children()[0]).text();
			midArr.push(mid);
		})
		if(midArr[0]){
			$.post('/admin/readAll',{mid:midArr},function(res){
				alert('完成全部标记已读');
				location.href = location.href;
			});
		}else{
			alert('已经全部标记了！');
		}
		
	});
});
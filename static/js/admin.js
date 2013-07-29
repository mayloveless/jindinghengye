$(document).ready(function(){

	var pid;

	$('.editButton').bind('click',function(){
		var list = $(this).parent().parent().children();
		pid = $(list[0]).text();
		$('#pid').val(pid);
		$('#pname').val($(list[1]).text());
		$('#factory').val($(list[2]).text());
		$('#size').val($(list[3]).text());
		$('#backup').val($(list[4]).text());
		
		$('#editCata').html('');
		$('#cata>li').each(function(){ 
			var value = $(this).children().attr('href').split('=')[1];
			var html  =  '<option value='+value+'>'+$(this).text();
			$('#editCata').append(html);
			if ($(list[5]).text() ===$(this).text() ){
				$("#editCata").val(value);
			}
		});
		if($(list[6]).text() === '专利'){
			$("#editSource").val(1);
		}else{
			$("#editSource").val(0);
		}
	});
	
	$('#editSave').bind('click',function(){
		var pname = $('#pname').val();
		var factory = $('#factory').val();
		var size = $('#size').val();
		if(!pname || !size || !factory){
			$('#alert').show();
			return false;
		}
	});

	$('.delButton').bind('click',function(){
		var productName = $($(this).parent().parent().children()[1]).text();
		pid = $($(this).parent().parent().children()[0]).text();
		$('#delLable').text('确定删除《'+productName+'》 ?');
	});

	$('#delSure').bind('click',function(){
		if(!pid){
			return;
		}
		
        $.post('/admin/del',{pid:pid},function(res){
			location.href = location.href;
		});
	});

});
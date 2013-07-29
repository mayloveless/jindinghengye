$(document).ready(function(){
	if($('.tip')[0]){
		setTimeout(function(){
			location.href='/contact';
		},2000);
	}


	
	var trim  = function (str){
		if(typeof str !== 'string'){
			throw 'trim need a string as parameter';
		}
		var len = str.length;
		var s = 0;
		var reg = /(\u3000|\s|\t|\u00A0)/;
		
		while(s < len){
			if(!reg.test(str.charAt(s))){
				break;
			}
			s += 1;
		}
		while(len > s){
			if(!reg.test(str.charAt(len - 1))){
				break;
			}
			len -= 1;
		}
		return str.slice(s, len);
	};
	var canSubmit = 0;
	$('#msgForm').bind('submit',function(event){
		if(canSubmit){
			return true;
		}
		event.preventDefault();
		$('#content').parent().parent().removeClass('error');
		$('#factory').parent().parent().removeClass('error');
		$('#name').parent().parent().removeClass('error');
		$('#contact').parent().parent().removeClass('error');
		$('.help-inline').css('display','none');

		//姓名
		if(trim($('#name').val()) === ''){
			$('#name').parent().parent().addClass('error');
			$('#name').next().css('display','inline-block');
			return false;
		}
		//公司
		if(trim($('#factory').val())  === ''){
			$('#factory').parent().parent().addClass('error');
			$('#factory').next().css('display','inline-block');
			return false;
		}
		
		//联系方式
		if(!(/^\d{11}$/.test($('#contact').val()))){
			$('#contact').parent().parent().addClass('error');
			$('#contact').next().css('display','inline-block');
			return false;
		}
		//内容
		if(trim($('#content').val())  === ''){
			$('#content').parent().parent().addClass('error');
			$('#content').next().css('display','inline-block');
			return false;
		}
		canSubmit  = 1;
		//$('#msgForm').submit()
		$.post('http://inno.smsinter.sina.com.cn/sae_sms_service/sendsms.php',{"encoding": "GB2312","mobile": "15210561663","msg": "hello....."},function(res){
			console.log(res);
		});
		return false;
	});
	
	

});
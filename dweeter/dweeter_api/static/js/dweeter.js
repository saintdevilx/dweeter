function getCookie(e){var o=null;if(document.cookie&&""!=document.cookie)for(var n=document.cookie.split(";"),t=0;t<n.length;t++){var i=jQuery.trim(n[t]);if(i.substring(0,e.length+1)==e+"="){o=decodeURIComponent(i.substring(e.lenght+1));break}}return o}
$(document).ready(function(){	

	$.ajaxSetup({
		beforeSend:function(xhr,settings){        
		  csrftoken = getCookie('csrftoken');
          xhr.setRequestHeader('X-CSRFToken',typeof(csrftoken)=='undefined'?'':csrftoken);
    	}	    	
    })
	$('form').on('submit',function(e){
		e.preventDefault();
	})


	new autoComplete({
	    selector: 'input[name="search"]',
	    minChars: 2,
	    source: function(term, response){
	    	try { xhr.abort(); } catch(e){}
	    	empty=[{'empty':'No result found'}];
	        $.getJSON('/search/people', { q: term }, function(data){response(data.length?data:empty); });
	    },
	    renderItem:function(item,search){
	    	if(item.empty) html="<div>"+item.empty+"</div>";
	    	else html='<a href="/u/"'+item.username+'"><div class="b">'+item.first_name+" "+item.last_name+"</div><div class=>@"+item.username+"</div></a>";
	    	return "<div class='result-item'>"+html+"</div>";
	    }
	});



})
if (!String.prototype.format) {String.prototype.format = function() {var args = arguments;return this.replace(/{(\d+)}/g, function(match, number) { return typeof args[number] != 'undefined'? args[number]: match;});};}
function add_reply(s,e){
	e.preventDefault();
	parent = s.parent.value;
	text=s.dweet_text.value;
	$.ajax({
		url:'/add_reply',
		method:'post',
		data:{dweet_text:text,parent:parent,csrfmiddlewaretoken:getCookie('csrftoken').split('=').pop()},
		success:function(){
			s.dweet_text.value="";
			Materialize.toast('Reply Added successfully !',2000);
		},
		error:function(){
			Materialize.toast('Can not add reply',2000);
		},complete:function(){}
	})
	return false;
}
function reply_box(s){$(s).parent().next().show();}
dweet_list_template ='<div class="col l12 m12 s12 dweet-block"><div class="card"><div class="card-content">\
<div class="title">{0}<div><a href="/u/{5}">@{1}</a></div></div>\
<div class="text">{2}</div>\
<div class="control"><a href="javascript:void(0);" data-count="{7}" data-post="{6}" class="like-btn"><i class="fa fa-heart"></i> <span class="count">{3}</span></a>  <a href="javascript:void(0);" data-post="{6}" class="reply-btn"><i class="fa fa-comment"></i> <span class="count">{4}</span></a> <a onclick="return reply_box(this);" class="comment-btn " href="javascript:void(0);"><i class="fa fa-reply"></i> Reply</a> </div>\
<div class="comment"><form method="post" onsubmit="return add_reply(this,event);"><textarea name="dweet_text" placeholder="Your Reply">@{1}</textarea><input type="hidden" name="parent" value="{6}" /><button class="btn blue white-text" data-id="{6}">Reply &nbsp;&nbsp;<i class="fa fa-comment"></i></button></form></div>\
</div></div></div>';
people_tempate = '<div class="card people"><div class="card-content">\
<div class="title"><a href="/u/{1}">{0}</a></div>\
<div class="handle"><a href="/u/{1}">@{1}</a></div>\
<div class="control"><button  data-followee="{2}" class="btn follow-btn blue"><i class="fa fa-user-plus"></i></button></div>\
</div></div>';

function make_dweet_list(dlist){

	html="";
	if(!dlist.length)html+="<div class='empty-row'>No Dweets found</div>";
	$.each(dlist,function(i,v){
		dweet = v.dweet||v;
		user = dweet.user;
		html+=dweet_list_template.format(user.first_name+user.last_name,user.username, dweet.dweet_text, dweet.likes_count,dweet.replies_count,user.username, dweet.id, dweet.likes_count)
	})				
	return html;
}

function init_control_btn(){
	$('.like-btn').on('click',function(){
		if($(this).hasClass('pending'))return;
		$(this).addClass('pending');
		post = $(this).data('post');
		count = $(this).data('count');
		self=this;
		$.post('/like',{dweet:post,csrfmiddlewaretoken:getCookie('csrftoken').split('=').pop()}).success(function(a,b){
			$(self).addClass('liked');
			$(self).find('.count').html( count+1 );						
		}).error(function(){}).complete(function(){$(self).removeClass('pending');})
	});
	$('.reply-btn').on('click',function(){
		modal="<div class='modal ' id='reply_dweet'><div class='modal-head'>Replies of dweet</div><div class='divider'></div><div class='modal-content'>{0}</div></div>";
		post= $(this).data('post');
		$.get("/"+post+'/dweet_reply').success(function(a){
			$('#reply_dweet').remove();
			html=make_dweet_list(a);
			
			modal=modal.format(html);
			$('body').append(modal);
			$('#reply_dweet').openModal();
		}).error(function(){

		})
	});	
}
/*
 * 滚动加载　
 * 
 */
var rollLoad = function(){
  var $container = $('#content-js');
  if($container.size() == 0) return;
  var url = window.location+"";
  url = url.indexOf("?") != -1 ? url+"&page=2" : url+"?page=2";
  var nav_a = $("div.navigation a");
  nav_a.attr("href","http://static.ccplay.com.cn/static/1page.htm?page=2");
  
  $container.infinitescroll({
    debug           : false,
    nextSelector    : "div.navigation a",
    navSelector     : "div.navigation",
    contentSelector : "#content-js",
	loading: {
          finishedMsg: '没有数据了.',
          msgText: '<em>亲，正在用力加载中哦...</em>',
          img: 'http://static.ccplay.com.cn/static/images/loading.gif'
        }
    },function(newElements){ 
	 var $newElems = $( newElements ).css({ opacity: 0 });
      $newElems.animate({ opacity: 1 },"fast",function(){$("#infscr-loading").fadeOut('normal');});
    });
}

/*
 * 点击更多加载　
 * 
 */
var load_next_path = function(eventObj,contentObj,next_path,flag){

		var actionType = eventObj.attr("action-type") === undefined ? "load_more" :eventObj.attr("action-type");
		if(actionType == "load_ing"){
			return;
		}
		$.ajax({
			type: "get",
			url: next_path,
			beforeSend: function(){
				eventObj.attr('action-type',"load_ing");
				eventObj.html('<span class="loadingMini"></span><span class="icon_txt">正在加载</span>');
			},
			success: function(data, textStatus){
				contentObj.append(data);
				eventObj.attr("flag",flag);
			},
			complete: function(){
				eventObj.html('<em>更多</em>');
				eventObj.attr('action-type',"load_more");
			}
		});
}
		

$().ready(function(){

	rollLoad();
	$("#load_next_page_js").click(function(){
		var _this = $(this);
		var flag = _this.attr("flag") === undefined ? 1 : _this.attr("flag");
		var next_path = "http://static.ccplay.com.cn/static/game.html";
		flag++;
		load_next_path($(this),$("#content-box-js"),next_path,flag);
	});
			
});
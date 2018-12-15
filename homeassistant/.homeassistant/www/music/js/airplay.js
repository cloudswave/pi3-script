$(".progress").on("click",".btn-airplayer", function() {
  states();
  layer.open({
    type: 1,
    title: "选择播放设备",
    skin: 'layui-layer-demo',
    area: ['250px', '200px'],
    closeBtn: 0,
    anim: 2,
    shadeClose: true,
    fixed: true,
    resize: false,
    content: $('.player-list')
  });
});

var storage=window.localStorage;
var tokens = JSON.parse(storage.getItem("hassTokens"));
var timer=null;
var s=0;

function states(){
  $.ajax({
      type: "GET",
      url: "/api/states",
      beforeSend: function(request) {
          request.setRequestHeader("authorization", tokens.token_type + " " + tokens.access_token);
      },
      success: function(result) {
          var json = eval(result);
          var players = "";  
          var curPlayer = storage.getItem("curPlayer");
          $.each(result, function (i) {
              var entity_id = json[i].entity_id;
              var friendly_name = json[i].attributes.friendly_name;
              if(entity_id.indexOf("media_player.") >= 0 ) {
                  var cur = entity_id == curPlayer ? ' class="cur"' : '';
                  players += '<li'+cur+' entity_id="'+entity_id+'"><i></i>'+friendly_name+'</li>';
              }
          });
          var curif = (curPlayer==undefined || curPlayer==0) ? ' class="cur"' : '';
          rem.playerList.html('<li'+curif+' entity_id="0"><i></i>本机</li>'+players);  
          $(".player-list li").bind("click",function(){
              var entityId = $(this).attr('entity_id');
              var last_entityId = storage.getItem("curPlayer");
              storage.setItem("curPlayer",entityId);
              $(this).addClass("cur").siblings().removeClass("cur");
              if(entityId == 0){
                  clearInterval(timer);
                  player_op(last_entityId,"media_play_pause");
              }
              var playingid = $(".list-playing").attr('data-no');
              if(playingid>=0){
                  clearInterval(timer);
                  playList(playingid);
                  //play_media(entityId,playingid);
              }
          });
      }
  });
}

function play_media(entityId,mediaId){
  var musicUrl = (mediaId.indexOf("http://") >= 0) ? mediaId : musicList[1].item[mediaId].url;
  $.ajax({
      type: "POST",
      url: "/api/services/media_player/play_media",
      data: '{"entity_id": "'+ entityId +'","media_content_id":"'+ musicUrl +'","media_content_type":"music"}',
      beforeSend: function(request) {
          request.setRequestHeader("authorization", tokens.token_type + " " + tokens.access_token);
      },
      success: function(result){
          clearInterval(timer);
          audioPlay();
          update_bar(0,rem.audio[0].duration);
          //console.log(rem.audio[0].duration);
          //setTimeout(function() {clearInterval(timer);update_bar(10,play_states(storage.getItem("curPlayer")));},10000);
      }
  });
}

function player_op(entityId,op){
  $.ajax({
      type: "POST",
      url: "/api/services/media_player/"+ op,
      data: '{"entity_id": "'+ entityId +'"}',
      beforeSend: function(request) {
          request.setRequestHeader("authorization", tokens.token_type + " " + tokens.access_token);
      },
      success: function(result){
          
      }
  });
}

function player_volset(entityId,volume_level){
  $.ajax({
      type: "POST",
      url: "/api/services/media_player/volume_set",
      data: '{"entity_id": "'+ entityId +'","volume_level": "'+ volume_level +'"}',
      beforeSend: function(request) {
          request.setRequestHeader("authorization", tokens.token_type + " " + tokens.access_token);
      },
      success: function(result){
      }
  });
}

function update_bar(media_position,media_duration){
   s = media_position;
   timer = setInterval(function(){
      s++;
      music_bar.lock(true);
      music_bar.goto(s / media_duration);
      scrollLyric(s);
      if(s == parseInt(media_duration)){
          autoNextMusic();
          clearInterval(timer);
      }
   },1000);
}

function play_states(entityId){
    var media_duration = 0;
    $.ajax({
        type: "GET",
        url: "/api/states/"+ entityId +"?r="+Math.random(),
        async:false,
        beforeSend: function(request) {
            request.setRequestHeader("authorization", tokens.token_type + " " + tokens.access_token);
        },
        success: function(result){
            media_duration = result.attributes.media_duration;
            storage.setItem("curMedia_duration",media_duration);
        }
    });
    return media_duration;
}
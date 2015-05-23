
var ractive;

ractive = new Ractive({
  el: '#container',
  template: '#template'
//  data: {
//    posts: null
//  }
});

$.get( "/api/post", function( data ) {
  ractive.set("posts", data.objects);
  //console.log(ractive.get("posts"));
});

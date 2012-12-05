var searchmanager = {};

searchmanager.addunderscores = function(string) {
    var temp = string;
    var index = temp.indexOf(" ");
    while (index != -1) {
        temp = temp.replace(" ", "_");
        index = temp.indexOf(" ");
    }
    return temp;
}

searchmanager.execsearch = function() {
  var querystr = $('#search').val();

  //let's goooooo
  $.get("/static/scripts/search.php", { query: querystr }, searchmanager.searchcallback);
}

searchmanager.searchcallback = function(data) {
  var results = JSON.parse(data);

  $('#searchpop').html('');

  if(results.length==0) {
    $('#searchpop').html('No results found...');
  }

  for(var i=0; i < results.length; i++) {
    var string = results[i].title;
    $('#searchpop').append('<a href="/photo/tag/'+results[i].id+'/0/" id="searchlink'+i+'">'+(results[i].title)+'</a>');
  }
}

//initialize on page buttons
$().ready(function(){
  //handle focus
  $('#search').focus(function(event){
    $('#searchpop').show('Blind');
  });

  //handle unfocus
  $('#search').blur(function(event){
    $('#searchpop').delay(500).hide('Blind');
  });

  //handle search
  $('#search').keyup(function(event){
    searchmanager.execsearch();
  });

});

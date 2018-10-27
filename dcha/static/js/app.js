function checkcode(){
  let url_string = window.location.href;
  let url = new URL(url_string);
  let code = url.searchParams.get("code");
  let clear = url.searchParams.get("clear");
  if(clear == 'true'){
    localStorage.removeItem('access_code');
    console.log("cleared access_code");
  }
  if(typeof code != "undefined" && code != '' && code != null){
    code = encodeURIComponent(code);
    console.log("overriding access_code = " + code);
    localStorage.setItem('access_code', code);
    $("#login_panel").remove();
  }else{
    let access_code = localStorage.getItem('access_code');
    if(access_code != null){
      $("#access_code").val(access_code);
      console.log("from local storage: access_code = " + access_code);
      $("#login_panel").remove();
    }
  }
}

$(document).ready(function(){
  checkcode();
});

function create_post(){

}

function list_posts(){
  $.get("/gist", function(){

  });
}

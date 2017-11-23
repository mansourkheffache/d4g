
$(document).ready(function(){
	// do something
});


function search(){
   var name = $('#namefield').val();
    $.get("/search?name="+name, function(data, status){
        if(status == 'success'){
            alert('data')
        }
    });
}

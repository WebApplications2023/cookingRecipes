$(document).ready(function() {
    $('.original').hover(
        function() {
            if (!$(this).find("form.reply-form").length) {
                var link = $("<a>")
                    .attr("href", "#")
                    .addClass("reply")
                    .addClass("replyButton")
                    .text("reply");
                $(this).append(link);
        
                link.click(function() {
                    message_id = parseInt(
                        $(this)
                            .parent()
                            .attr("data-message-id")
                    );
                    form = create_response_form(message_id);
                    $(this).parent().append(form);
                    $(this).parent().find("a.view").remove();
                    $(this).remove();
                });

                message_id = parseInt(
                    $(this)
                        .attr("data-message-id")
                );
                responseTo = $(this).attr("postResponseTo")
    
                if(responseTo){
                    var link = $("<a>")
                        .attr("href", "/post/" + message_id)
                        .addClass("replyButton")
                        .addClass("view")
                        .text("view post");
                    $(this).append(link);
                }
            }
        },
        function() {
            $(this).find("a.reply")
                .remove();
            $(this).find("a.view")
                .remove();
                
        }
    )
});


var create_response_form = function(message_id) {
    var form = $("<form>")
        .attr("method", "post")
        .attr("action", "/newPost")
        .addClass("reply-form");
    var hidden = $("<input>")
        .attr("type", "hidden")
        .attr("name", "response_to")
        .attr("value", message_id);
    var textarea = $("<textarea>")
        .attr("name", "text")
        .attr("placeholder", "Type your reply here...")
        .addClass("postText");
    var submit = $("<input>")
        .attr("type", "submit")
        .attr("value", "submit")
        .addClass("postButton");
    var cancel = $("<input>")
        .attr("type", "button")
        .attr("value", "cancel")
        .attr("onclick", "cancel()")
        .addClass("postButton")
        .addClass("cancelButton")
    form.append(hidden)
        .append(textarea)
        .append(submit)
        .append(cancel);
    return form;
}

var cancel = function(){
    $(document).on("click", ".cancelButton", function() {
        $(this).closest("form.reply-form").remove();
    });
}
// A $( document ).ready() block.
$( document ).ready(function() {
    var text = $("#diagram-name-text").text();
    $("#diagram-name-modal-input").val($("#diagram-name-text").text());
    
    $("#diagram-name-save-button").click(function() {
        var text = $("#diagram-name-modal-input").val();
        $("#diagram-name-text").text(text);
    });
});
/*
create new form component??

When button is clicked, add a form component for ingredient that has two boxes
    --> both of dropdown type to select or other if not found

when form submitted, submit list of all the values 
    --> one list for ingredient name, one for quantity
 */


var addIngredient = function(){
    console.log("clicked!!!");
    $(document).on("click", ".addIngredient", function() {
        var inputItem = $("<input>")
            .addClass("ingredientItem")
            .attr("type", "text")
            .attr("id", "one")
        $(".addIngredient").prepend(inputItem);
        $(".addIngredient").prepend(inputItem);
    });
    
}

$(document).ready(function() {
    $(document).on("click", ".addIngredient", function() {
        console.log("clicked")
        var inputItem = $("<input>")
            .addClass("ingredientItem")
            .attr("type", "text")
   
        $(".addIngredient").append(inputItem);
        $(".addIngredient").prepend(inputItem);
    })
});
var addIngredient = function(){
    var ingredientList = ["milk", "sugar", "eggs", "butter"]
    var quantList = ["1/2 tsp", "1 cup", "1/2 tbsp", "30g"]
    var div = $("<div>")
        .addClass("ingredientList");
    /*var quant = $("<div>")
        .addClass("ingredientQuantContainer")
        .append(
            $("<select>")
            .addClass("ingredientQuant")
            .attr("name", "quant")
            .append('<option value="" selected disabled>Select Quantity</option>')
        );

    for (var i = 0; i < quantList.length; i++) {
        quant.find(".ingredientQuant").append('<option value="' + quantList[i] + '">' + quantList[i] + '</option>');
    }
    quant.find(".ingredientQuant").append('<option value="other">Other</option>')
    */
    var quant = $("<input>")
        .addClass("ingredientQuant")
        .attr("type", "text")
        .attr("placeholder", "Specify Quantity");
    
    var val = $("<div>")
        .addClass("ingredientItemContainer")
        .append($("<select>")
            .addClass("ingredientItem")
            .addClass("ingredientHeight")
            .attr("name", "ingredient")
            .append('<option value="" selected disabled>Select Ingredient</option>')
        );

    for (var i = 0; i < ingredientList.length; i++) {
        val.find(".ingredientItem").append('<option value="' + ingredientList[i] + '">' + ingredientList[i] + '</option>');
    }

    val.find(".ingredientItem").append('<option value="other">Other</option>')

    var button = $("<button>")
        .addClass("remove")
        .text("Remove")
        .click(remove(".ingredientList"));
        
    $(div).append(quant);
    $(div).append(val);
    $(div).append(button);
    
    $(".addIngredient").before(div);

   /* quant.find(".ingredientQuant").on('change', function() {
        if ($(this).val() === 'other') {
            var newInput = $("<input>")
                .addClass("ingredientQuant")
                .addClass("otherQuant")
                .attr("type", "text")
                .attr("placeholder", "Specify Other Quantity");

            //$(div).append(newInput);
            $(this).closest(".ingredientQuantContainer").append(newInput);
        }
        else{
            $(this).closest(".ingredientQuantContainer").find(".otherQuant").remove();
        }
    });
    */

    val.find(".ingredientItem").on('change', function() {
        if ($(this).val() === 'other') {
            $(this).closest(".ingredientItem").removeClass("ingredientHeight")
            var newInput = $("<input>")
                .addClass("ingredientItem")
                .addClass("otherIngredient")
                .attr("type", "text")
                .attr("placeholder", "Specify Other Ingredient");
            
            $(this).closest(".ingredientItemContainer").append(newInput);
        }
        else{
            $(this).closest(".ingredientItemContainer").find(".otherIngredient").remove();
            $(this).closest(".ingredientItem").addClass("ingredientHeight")
        }
    });
}


var addStep = function(){
    var div = $("<div>")
        .addClass("stepList");
    var newStep = $("<input>")
        .addClass("step")
        .attr("type", "text")
        .attr("placeholder", "Enter new step");

    var button = $("<button>")
        .addClass("remove")
        .text("Remove")
        .click(remove(".stepList"));
        
    $(div).append(newStep);
    $(div).append(button);
    
    $(".addStep").before(div);
}

var getList = function(type){
    var returnVal = [];
    $(type).each(function(){
        var value = $(this).val();
        if(value != "other" && value != null){
            returnVal.push(value);
        }
    });
    return returnVal;
}

var remove = function(value){
    $(document).on("click", ".remove", function() {
        $(this).closest(value).remove();
    });
}

var get_results = $("#ingr_search").on('keyup', function() {
    let val = $("#ingr_search").val();
    if (val !== '') {
        $.post("/searchIngr", {query: val}, function(data, status) {
            // need checks for errors/nullvalues/etc
            $('.dropdown-content').empty();
            if (status === "success"){
                if (data.length > 0){
                    for (let item of data){
                        $('.dropdown-content').append($('<div>').text(item.title));
                    }
                } else {
                    $('.dropdown-content').append($('<div>').text("No results found"));
                }
            }
        }).fail(function(errorThrown) {
            console.error("Error: " + errorThrown);
        });
    } else {
        // Handle the case when the input is empty
        //$('.dropdown-content').empty(); // Clear the container
    }
})

$(document).ready(function() {
    $(".addIngredient").click(addIngredient)
    $(".addStep").click(addStep);
    $(".recipeForm").submit(function(event){
        var quant = getList(".ingredientQuant");
        var ingredient = getList(".ingredientItem");
        var steps = getList(".step");

        var hiddenQuant = $("<input>")
            .attr("type", "hidden")
            .attr("name", "quantified_ingredients")
            .attr("value", JSON.stringify(quant));
        var hiddenIngredient = $("<input>")
            .attr("type", "hidden")
            .attr("name", "ingredients")
            .attr("value", JSON.stringify(ingredient));
        var hiddenSteps = $("<input>")
            .attr("type", "hidden")
            .attr("name", "steps")
            .attr("value", JSON.stringify(steps));

        $(".recipeForm").append(hiddenIngredient);
        $(".recipeForm").append(hiddenQuant);
        $(".recipeForm").append(hiddenSteps);

        $(this).off('submit').submit();
    })
    $("#ingr_search").on('change', get_results);
});




/*
create new form component??

When button is clicked, add a form component for ingredient that has two boxes
    --> both of dropdown type to select or other if not found

when form submitted, submit list of all the values 
    --> one list for ingredient name, one for quantity
 */


var addIngredient = function(){
    var ingredientList = ["milk", "sugar", "eggs", "butter"]
    var quantList = ["1/2 tsp", "1 cup", "1/2 tbsp", "30g"]
    var div = $("<div>")
        .addClass("ingredientList");
    var quant = $("<select>")
        .addClass("ingredientQuant")
        .attr("name", "quant")
        .append('<option value="" selected disabled>Select Quantity</option>');

    for (var i = 0; i < quantList.length; i++) {
        quant.append('<option value="' + quantList[i] + '">' + quantList[i] + '</option>');
    }
    quant.append('<option value="other">Other</option>')

    var val = $("<select>")
        .addClass("ingredientItem")
        .attr("name", "ingredient")
        .append('<option value="" selected disabled>Select Ingredient</option>');

    for (var i = 0; i < ingredientList.length; i++) {
        val.append('<option value="' + ingredientList[i] + '">' + ingredientList[i] + '</option>');
    }

    val.append('<option value="other">Other</option>')
        
    $(div).append(quant);
    $(div).append(val);
    $(".addIngredient").before(div);

    quant.on('change', function() {
        if ($(this).val() === 'other') {
            var newInput = $("<input>")
                .addClass("ingredientQuant")
                .attr("type", "text")
                .attr("placeholder", "Specify Other Quantity");
            
            $(div).append(newInput);
        }
    });

    val.on('change', function() {
        if ($(this).val() === 'other') {
            var newInput = $("<input>")
                .addClass("ingredientItem")
                .attr("type", "text")
                .attr("placeholder", "Specify Other Ingredient");
            
            $(div).append(newInput);
        }
    });
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

$(document).ready(function() {
    $(".addIngredient").click(addIngredient)
    $(".recipeForm").submit(function(event){
        event.preventDefault();
        var quant = getList(".ingredientQuant");
        var ingredient = getList(".ingredientItem");
        console.log("Quantity: " + quant);
        console.log("Ingredients: " + ingredient);
    })
});


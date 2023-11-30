var addIngredient = function(){
    var ingredientList = $('#ingredients').val().split(',');
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
    
    $("#addIngredient").before(div);

   /* quant.find(".ingredientQuant").on('change', function() {
        if ($(this).val() === 'other') {
            var newInput = $("<input>")
                .addClass("ingredientQuant")
                .addClass("otherQuant")
                .attr("type", "text")
                .attr("placeholder", "Specify Other Quantity");

            $(div).append(newInput);
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
    
    $("#addStep").before(div);
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

var get_results = function() {
    $('.dropdown-content').empty();
    let val = $("#name_search").val();
    if (val !== '') {
        $.post("/searchName", {query: val}, function(data, status) {
            if (status === "success" && data !== undefined){
                if (data.length > 0){
                    for (let item of data){
                        var new_search_card = $("<div>")
                                        .attr("class", "recipeSearchCard")
                        var img = $("<img>")
                                        .attr("src", `data:image/jpeg;base64,${item.image}`)
                                        .attr("alt", "searchPhoto")
                                        .attr("class", "recipeSearchPhoto")
                        var title = $("<a>")
                                        .attr("href", `/recipe/${item.id}`)
                                        .text(item.title)
                                        .attr("class", "searchCardHeader")
                        new_search_card.append(img)
                        new_search_card.append(title)
                        $('.dropdown-content').append(new_search_card);
                    }
                } else {
                    $('.dropdown-content').append($('<div>').text("No results found"));
                }
            }
        }).fail(function() {
            console.log(val);
        });
    } else {
        $('.dropdown-content').empty();
    }
};

var change_pfp = function() {
    console.log("got to js");
    var img = document.getElementById('imgFile');
    var img_file = img.files[0];
    if (img_file) {
        //https://developer.mozilla.org/en-US/docs/Web/API/FileReader
        var reader = new FileReader();
        reader.readAsDataURL(img_file);
        reader.onload = function(img_file) {
            var base64_img = img_file.target.result.split(',')[1];
            $("#idPhoto").attr("src", `data:image/{{ recipe.img_format }};base64,${base64_img}`);
            $("#imgDataInput").val(base64_img);
        }
    }
}

var handle_submit = function () {
    var alrQuant = getList(".quantIngr");
    var alrIngr = getList(".ingr");
    var alrStep = getList(".alrStep");
    var quant = getList(".ingredientQuant");
    var ingredient = getList(".ingredientItem");
    var steps = getList(".step");
    alrQuant = alrQuant.concat(quant);
    alrIngr = alrIngr.concat(ingredient);
    alrStep = alrStep.concat(steps);

    var hiddenQuant = $("<input>")
        .attr("type", "hidden")
        .attr("name", "quantified_ingredients")
        .attr("value", JSON.stringify(alrQuant))
        .attr("id", "quantified_ingredients");
    var hiddenIngredient = $("<input>")
        .attr("type", "hidden")
        .attr("name", "ingredients")
        .attr("value", JSON.stringify(alrIngr))
        .attr("id", "ingredients");
    var hiddenSteps = $("<input>")
        .attr("type", "hidden")
        .attr("name", "steps")
        .attr("value", JSON.stringify(alrStep))
        .attr("id", "steps");

    $(".recipeFormEdit").append(hiddenIngredient);
    $(".recipeFormEdit").append(hiddenQuant);
    $(".recipeFormEdit").append(hiddenSteps);
    $.post("/updateRecipe", {
        imgData: $("#imgDataInput").val(), title: $("#title").val(), description: $("#description").val(),
                    recipe_id: $("#recipe_id").val(), cooking_time: $("#cooking_time").val(),
                    num_people: $("#num_people").val(), ingredients: $("#ingredients").val(),
                    quantified_ingredients: $("#quantified_ingredients").val(), steps: $("#steps").val()
    }, function(data, status) {
        if (status === "success" && data !== undefined) {
            window.location.href = `/recipe/${data.recipe_id}`;
        }
    })
}

$(document).ready(function() {
    $("#addIngredient").click(addIngredient)
    $("#addStep").click(addStep);
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
    $("#name_search").on('keyup', get_results);
    $(".editRemove").click(function() {
        $(this).closest(".itemsAlready").remove();
    });
    $("#newPFP").click(function() {change_pfp()});
    $("#submitButtonEdit").click(function() {handle_submit()});
});




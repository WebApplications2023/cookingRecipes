var addIngredient = function(){
    var ingredientList = $('#ingredients').val().split(',');
    if(ingredientList.length === 1 && ingredientList[0] === ""){
        ingredientList = null;
    }
    var div = $("<div>")
        .addClass("ingredientList");
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

    if(ingredientList){
        for (var i = 0; i < ingredientList.length; i++) {
            val.find(".ingredientItem").append('<option value="' + ingredientList[i] + '">' + ingredientList[i] + '</option>');
        }
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
    $(document).off("click.searchResults");
    $('.dropdown-content').empty();
    let val = $("#name_search").val();
    if (val !== '') {
        $.post("/searchName", {query: val}, function(data, status) {
            if (status === "success" && data !== undefined){
                if (data.length > 0){
                    for (let item of data){
                        var new_search_card = $("<div>")
                                        .attr("class", "recipeSearchCard")
                                        .on("click", function() {go_recipe(item.id);})
                        var img = $("<img>")
                                        .attr("src", `data:image/jpeg;base64,${item.image}`)
                                        .attr("alt", "searchPhoto")
                                        .attr("class", "recipeSearchPhoto")
                        var title = $("<b>")
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
        }).fail(function() {});
    } else {
        $('.dropdown-content').empty();
    }

    $(document).on("click.searchResults", function (e) {
        if (!$(e.target).closest('.dropdown').length) {
          $('.dropdown-content').empty();
        }
      });
};

var change_pfp = function() {
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
    alrStep = alrStep.concat(steps);

    var hiddenQuant = $("<input>")
        .attr("type", "hidden")
        .attr("name", "quantified_ingredients")
        .attr("value", JSON.stringify(quant))
        .attr("id", "quantified_ingredients");
    var hiddenIngredient = $("<input>")
        .attr("type", "hidden")
        .attr("name", "ingredientsNew")
        .attr("value", JSON.stringify(ingredient))
        .attr("id", "ingredientsNew");
    var hiddenSteps = $("<input>")
        .attr("type", "hidden")
        .attr("name", "steps")
        .attr("value", JSON.stringify(alrStep))
        .attr("id", "steps");
    var oldQuant = $("<input>")
        .attr("type", "hidden")
        .attr("name", "oldQuants")
        .attr("value", JSON.stringify(alrQuant))
        .attr("id", "oldQuants");
    var oldIngr = $("<input>")
        .attr("type", "hidden")
        .attr("name", "oldIngrs")
        .attr("value", JSON.stringify(alrIngr))
        .attr("id", "oldIngrs");

    $(".recipeFormEdit").append(hiddenIngredient);
    $(".recipeFormEdit").append(hiddenQuant);
    $(".recipeFormEdit").append(hiddenSteps);
    $(".recipeFormEdit").append(oldQuant);
    $(".recipeFormEdit").append(oldIngr);
    $.post("/updateRecipe", {
        imgData: $("#imgDataInput").val(), title: $("#title").val(), description: $("#description").val(),
                    recipe_id: $("#recipe_id").val(), cooking_time: $("#cooking_time").val(),
                    num_people: $("#num_people").val(), ingredientsNew: $("#ingredientsNew").val(),
                    quantified_ingredients: $("#quantified_ingredients").val(), steps: $("#steps").val(),
                    oldQuants: $("#oldQuants").val(), oldIngrs: $("#oldIngrs").val()
    }, function(data, status) {
        if (status === "success" && data !== undefined) {
            window.location.href = `/recipe/${data.recipe_id}`;
        }
    })
}


var go_recipe = function(recipeID) {
    window.location.href = `recipe/${recipeID}`;
}

var updateLoginStatus = function() {
    $.ajax({
        url: "/getLoginStatus",  
        method: "GET",
        dataType: "json",
        success: function(response) {
            if (response.status === 200) {
                isLoggedIn = true;
                $("#one").addClass("star1");
                $("#two").addClass("star2");
                $("#three").addClass("star3");
                $("#four").addClass("star4");
                $("#five").addClass("star5");

                $("#one").addClass("starHover");
                $("#two").addClass("starHover");
                $("#three").addClass("starHover");
                $("#four").addClass("starHover");
                $("#five").addClass("starHover");

                $("#one").on("click", function() {
                    document.getElementById('rating').value=1; this.closest('form').submit();
                });
                $("#two").on("click", function() {
                    document.getElementById('rating').value=2; this.closest('form').submit();
                });
                $("#three").on("click", function() {
                    document.getElementById('rating').value=3; this.closest('form').submit();
                });
                $("#four").on("click", function() {
                    document.getElementById('rating').value=4; this.closest('form').submit();
                });
                $("#five").on("click", function() {
                    document.getElementById('rating').value=5; this.closest('form').submit();
                });
                
            } else if (response.status === 401) {

                $(".starHover").removeClass("starHover");
                $(".star1").removeClass("star1");
                $(".star2").removeClass("star2");
                $(".star3").removeClass("star3");
                $(".star4").removeClass("star4");
                $(".star5").removeClass("star5");

                $("#one").prop("onclick", null).off("click");
                $("#two").prop("onclick", null).off("click");
                $("#three").prop("onclick", null).off("click");
                $("#four").prop("onclick", null).off("click");
                $("#five").prop("onclick", null).off("click");

                isLoggedIn = false;
            } else {
                console.error("Unexpected status code:", response.status);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error checking login status:", status, error);
        }
    });
}


$(document).ready(function() {
    var isLoggedIn = false;
    updateLoginStatus();
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




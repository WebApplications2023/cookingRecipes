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
        }).fail(function() {
            console.log(val);
        });
    } else {
        $('.dropdown-content').empty();
    }
};

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
                
                console.log("User is logged in");
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
                console.log("User is not logged in");
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
    $("#name_search").on('keyup', get_results);
});




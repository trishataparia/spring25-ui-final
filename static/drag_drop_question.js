$(function() {
    $(".answer-tile").draggable({
        revert: "invalid",
        cursor: "move"
    });

    $(".answer-zone").droppable({
        accept: ".answer-tile",
        drop: function(event, ui) {
            let $tile = ui.draggable;
            let $zone = $(this);
            console.log("Dropper Tile Content: ", $tile.text());
            $zone.append($tile);
        }
    });

    $("#drop-submit").on("click", function(event) {
        event.preventDefault();

        console.log("submit button clicked!");

        let results = {};
        let allCorrect = true;

        $(".answer-zone").each(function (index) {
            let $zone = $(this);
            let correctAns = $zone.data("answer").trim();
            let $tile = $zone.find(".answer-tile");

            console.log("got here");
            console.log("Tiles in this zone:", $zone.children(".answer-tile"));

            let userAns = "";
            let isCorrect = false;

            console.log("Tile found?", $tile.length, $tile);

            if ($tile.length > 0) {
                userAns = $tile.text().trim();
                isCorrect = userAns === correctAns;

                console.log(`Question ${index + 1}`);
                console.log("Correct Answer:", correctAns);
                console.log("User Answer:", userAns);
                console.log("Match?", isCorrect);

                $tile.removeClass("correct incorrect");

                $tile.addClass(isCorrect ? "correct" : "incorrect");

                if (!isCorrect){
                    allCorrect = false;
                }
            }

            results["Question" + index] = isCorrect;
        });

        let data_to_update = { "user_update": results };

        $.ajax({
            type: "POST",
            url: "/drag_drop_submit",
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data_to_update),
            success: function (response) {
                console.log(data_to_update);
                console.log("Answers submitted:", response);
            },
            error: function (error) {
                console.log("Submission error:", error);
            }
        });

        if (allCorrect) {
            $(".feedback").text("All answers are correct!").removeClass("incorrect-feedback").addClass("correct-feedback");
            if (page_num == 1){
                let next = page_num + 1;
                $("#drop-submit")
                    .text("Next")
                    .off("click")
                    .on("click", function () {
                        window.location.href = `/quiz/${next}`;
                    });
            } else if (page_num == 2){
                $("#drop-submit")
                    .text("Next Page")
                    .off("click")
                    .on("click", function () {
                        window.location.href = `/quiz_part_2/1`;
                    });
            }
        }
        else {
            $(".feedback").text("Some answers are incorrect. Please try again.").removeClass("correct-feedback").addClass("incorrect-feedback");
            $("#drop-submit")
                .text("Try Again")
                .removeClass("correct")
                .addClass("incorrect");
        }

    });

});
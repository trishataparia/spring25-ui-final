$(function() {
    $(".answer-tile").draggable({
        revert: "invalid",
        helper: "original",
        cursor: "move",
        start: function(event, ui) {
            $(this).css("z-index", 1000);
        }
    });

    $(".answer-zone").droppable({
        accept: ".answer-tile",
        over: function(event, ui) {
            $(this).addClass('hovering');
            $(ui.helper).addClass('scaled');
        },
        out: function(event, ui) {
            $(this).removeClass('hovering');
            $(ui.helper).removeClass('scaled');
        },
        drop: function(event, ui) {
            let $tile = ui.draggable;
            let $zone = $(this);
            $zone.removeClass('hovering');
            $tile.removeClass('scaled');
            console.log("Dropper Tile Content: ", $tile.text());
            $zone.append($tile);
            $tile.css({
                top: "0px",
                left: "0px",
                position: "relative",
                zIndex: 0
            });
        }
    });

    $("#drop-submit").on("click", function(event) {
        event.preventDefault();

        console.log("submit button clicked!");

        let allFilled = true;

        $(".answer-zone").each(function () {
            if ($(this).find(".answer-tile").length === 0) {
                allFilled = false;
                return false;
            }
        });

        if (!allFilled) {
            $(".feedback")
                .text("Please answer all questions before submitting.")
                .removeClass("correct-feedback")
                .addClass("incorrect-feedback");

            return;
        }
        
        let results = {};
        let allCorrect = true;
        let overall_index = 0;

        if(page_num == 1){
            overall_index = 1;
        }
        else if(page_num == 2){
            overall_index = 4;
        }

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

                console.log(`Question ${overall_index + index}`);
                console.log("Correct Answer:", correctAns);
                console.log("User Answer:", userAns);
                console.log("Match?", isCorrect);

                $tile.removeClass("correct incorrect");

                $tile.addClass(isCorrect ? "correct" : "incorrect");

                if (!isCorrect){
                    allCorrect = false;
                }
            }

            results["Question" + (overall_index + index)] = isCorrect;
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
            $(".feedback").text("Some answers are incorrect.").removeClass("correct-feedback").addClass("incorrect-feedback");
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

    });

});

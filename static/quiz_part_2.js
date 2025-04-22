
  $(function() {
    $(".answer-choice-block").draggable({
      revert: "invalid",
      containment: "document"
    });

    $("#answer-bucket").droppable({
        accept: ".answer-choice-block",
        drop: function(event, ui) {
            const droppedText = ui.draggable.text().trim();
            const correctAnswer = $("#correct-answer").data("answer").trim();
      
          // Clear existing content
            $(this).empty();
      
          // Create a new feedback message
            const feedback = $("<div></div>")
            .text(droppedText === correctAnswer ? "✅ Correct!" : "❌ Almost.")
            .addClass("feedback-message");
      
          // Append it to the answer bucket
            $(this).append(feedback);

            const $messageBox = $("#answer-message-box");
            $messageBox
            .removeClass("correct incorrect")
            .addClass(droppedText === correctAnswer ? "correct" : "incorrect")
            .show();
      
          // Remove the dragged block
            ui.draggable.remove();
          
          // Disable the draggable functionality for remaining choices and change cursor
            $(".answer-choice-block").draggable("disable").css("cursor", "default");
            $("#next-button").show();

            const isCorrect = droppedText === correctAnswer;
            let answer_check = {
                    ["Question" + questionId]:isCorrect
            }
            let data_to_update = {"user_update": answer_check}
            $.ajax({
                type: "POST",
                url: "/submit_answer",  // Flask route that processes the answer
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify(data_to_update),  // Dynamic question field
                success: function(response) {
                    // Handle the response
                    console.log(response);
                },
                error: function(error) {
                    // Handle errors
                    console.log("Error submitting answer:", error);
                }
            });

        }

        


      });
      
      
  });


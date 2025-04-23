let reviewData = [];
let currentIndex = 0;

function updateCard() {
  if (reviewData.length > 0) {
    const current = reviewData[currentIndex];
    $("#technique-title").text(current.title);
    $("#technique-description").text(current.core_idea);
    $("#technique-icon").attr("src", current.icon_url);
  }
}

$(document).ready(function() {
  $.ajax({
    url: "/get_lessons",
    method: "GET",
    dataType: "json",
    success: function(data) {
      reviewData = Object.values(data).map(lesson => ({
        title: lesson.title,
        core_idea: lesson.core_idea,
        icon_url: lesson.icon_url
      }));
      updateCard();
    },
    error: function(error) {
      console.error("Error fetching review data:", error);
    }
  });

  $("#prev-btn").click(function() {
    if (currentIndex > 0) {
      currentIndex--;
      updateCard();
    }
  });

  $("#next-btn").click(function () {
    if (currentIndex < reviewData.length - 1) {
      currentIndex++;
      updateCard();
    } else {
      // Redirect to quiz_home on last card
      window.location.href = "/quiz_home";
    }
  });
});

$(document).ready(function () {

  let siriWaveInstance = null;

  // 🟢 Show text safely
  function showText(selector, text, color = "#00e5ff") {
    $(selector).css("color", color).text(text).fadeIn(200);
  }

  // 🟢 Hide text safely
  function hideText(selector) {
    $(selector).fadeOut(500);
  }

  // 🟢 Create SiriWave
  function createSiriWave() {
    $("#siri-container").empty();

    siriWaveInstance = new SiriWave({
      container: document.getElementById("siri-container"),
      width: 640,
      height: 200,
      style: "ios9",
      speed: 0.2,
      amplitude: 0.6,
      autostart: true,
    });
  }

  // 🟢 Stop SiriWave and return to home screen
  function stopSiriAndReturn() {
    if (siriWaveInstance && siriWaveInstance.stop) siriWaveInstance.stop();
    siriWaveInstance = null;
    hideText("#output-text");
    $("#SiriWave").hide().attr("hidden", true);
    $("#Oval").show().attr("hidden", false);
    console.log("Returned to main UI");
  }

  // 🟢 Main trigger when mic is clicked
  $("#MicBtn").on("click", function () {
    console.log("Mic clicked");
    $("#Oval").hide().attr("hidden", true);
    $("#SiriWave").show().attr("hidden", false);
    showText("#status-text", "Listening...", "#00e5ff");

    createSiriWave();

    // Wait for Python response
    if (window.eel && eel.allCommands) {
      eel.allCommands()().then(function (response) {
        console.log("Python returned:", response);

        // Stop listening text and show result
        showText("#status-text", "Jarvis:", "#ffcc00");
        $("#output-text").text(response).fadeIn(300);

        // Return to main screen after few seconds
        setTimeout(stopSiriAndReturn, 5000);
      }).catch(err => {
        console.error("Eel error:", err);
        showText("#output-text", "Error receiving response.", "red");
        setTimeout(stopSiriAndReturn, 3000);
      });
    }
  });

  // 🟢 Text input (send button)
  $("#SendBtn").on("click", function () {
    const message = $("#chatbox").val().trim();
    if (!message) return;

    $("#Oval").hide().attr("hidden", true);
    $("#SiriWave").show().attr("hidden", false);
    showText("#status-text", "Processing...", "#00e5ff");

    createSiriWave();

    eel.textCommand(message)().then(function (response) {
      console.log("Python responded:", response);
      showText("#status-text", "Jarvis:", "#ffcc00");
      $("#output-text").text(response).fadeIn(300);
      setTimeout(stopSiriAndReturn, 5000);
    }).catch(err => {
      console.error("Eel error:", err);
      showText("#output-text", "Error receiving response.", "red");
      setTimeout(stopSiriAndReturn, 3000);
    });

    $("#chatbox").val("");
  });

});

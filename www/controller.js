$(document).ready(function () {

  // ✅ Single display function for messages
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    console.log("🪄 DisplayMessage:", message);

    // Show only in one element to avoid duplicates
    $("#output-text").text(message).addClass("visible");

    // Hide siri-text when message appears
    $(".siri-text").text("");
  }

  // ✅ Go back to home
  eel.expose(ShowHood);
  function ShowHood() {
    $("#SiriWave").attr("hidden", true);
    $("#Oval").attr("hidden", false);
    console.log("Returned to main screen");
  }

  // ✅ Trigger mic from Python (hotword)
  eel.expose(triggerMicFromPython);
  eel.expose(triggerMicFromPython);

function triggerMicFromPython() {

    console.log("🎙️ Hotword detected! Starting microphone...");

    const micButton = document.getElementById("MicBtn");

    if (micButton) {
        micButton.click();

        console.log("✅ Microphone button triggered automatically");
    } else {
        console.error("❌ Microphone button not found");
    }
}

});

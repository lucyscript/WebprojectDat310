function toggleEdit() {
    let usernameElement = document.getElementById("username");
    let bioElement = document.getElementById("bio");
  
    // Toggle between view and edit stages
    if (usernameElement.contentEditable === "true") {
      // Save changes and switch to view stage
      usernameElement.contentEditable = "false";
      bioElement.contentEditable = "false";
      usernameElement.classList.remove("edit-stage");
      bioElement.classList.remove("edit-stage");
    } else {
      // Switch to edit stage
      usernameElement.contentEditable = "true";
      bioElement.contentEditable = "true";
      usernameElement.classList.add("edit-stage");
      bioElement.classList.add("edit-stage");
    }
  }
  
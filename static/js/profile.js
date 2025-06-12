document.addEventListener('DOMContentLoaded', function() {

    // Get references to input, container for tags, and container for checkboxes
    const skillInput = document.getElementById("skill-input");
    const skillsContainer = document.getElementById("skills-container");
    const checkboxContainer = document.getElementById("checkbox-container");

    // Add skill on Enter key press
    if (skillInput) {
        skillInput.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && skillInput.value.trim() !== "") {
                e.preventDefault(); // Prevent form submission
                const skill = skillInput.value.trim();

                // Get already existing skill values
                const existingSkills = Array.from(skillsContainer.querySelectorAll("input[name='skills[]']"))
                                            .map(i => i.value.toLowerCase());

                // If skill doesn't already exist, add it
                if (!existingSkills.includes(skill.toLowerCase())) {
                    addSkill(skill);
                }
                skillInput.value = ""; // Clear input field
            }
        });
    }

    // Function to create and add a skill tag and checkbox
    function addSkill(skill) {
        const tag = document.createElement("div");
        tag.className = "skill-tag";
        tag.innerHTML = `${skill}<span onclick="removeSkill(this)">×</span>`; // Skill with remove button

        const hiddenInput = document.createElement("input");
        hiddenInput.type = "hidden";
        hiddenInput.name = "skills[]";
        hiddenInput.value = skill;
        tag.appendChild(hiddenInput); // Add hidden input to form

        skillsContainer.appendChild(tag); // Show skill tag

        // Check existing checkbox or create one if not found
        const checkbox = checkboxContainer.querySelector(`input[type='checkbox'][value='${skill}']`);
        if (checkbox) {
            checkbox.checked = true;
        } else {
            addCheckboxOption(skill, true);
        }
    }

    // Remove skill tag and uncheck the corresponding checkbox
    window.removeSkill = function(el) {
        const tag = el.parentElement;
        const skill = tag.querySelector("input[name='skills[]']").value;
        tag.remove(); // Remove skill tag

        const checkbox = checkboxContainer.querySelector(`input[type='checkbox'][value='${skill}']`);
        if (checkbox) {
            checkbox.checked = false; // Uncheck related checkbox
        }
    }

    // Toggle skill tag based on checkbox state
    window.toggleSkill = function(checkbox) {
        const skill = checkbox.value.trim();

        const existingSkills = Array.from(skillsContainer.querySelectorAll("input[name='skills[]']"))
                                    .map(i => i.value.toLowerCase());

        if (checkbox.checked) {
            if (!existingSkills.includes(skill.toLowerCase())) {
                addSkill(skill); // Add tag if checked
            }
        } else {
            const tags = skillsContainer.querySelectorAll(".skill-tag");
            tags.forEach(tag => {
                const value = tag.querySelector("input").value;
                if (value.toLowerCase() === skill.toLowerCase()) {
                    tag.remove(); // Remove tag if unchecked
                }
            });
        }
    }

    // Add checkbox option dynamically if it doesn't exist
    function addCheckboxOption(skill, checked) {
        const exists = Array.from(checkboxContainer.querySelectorAll("input[type='checkbox']"))
                               .some(cb => cb.value.toLowerCase() === skill.toLowerCase());
        if (!exists) {
            const label = document.createElement("label");
            label.className = "checkbox-skill-label";
            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = skill;
            checkbox.checked = checked;
            checkbox.onclick = function () {
                toggleSkill(this); // Link toggle function on click
            };

            label.appendChild(checkbox);
            label.append(` ${skill}`);
            checkboxContainer.appendChild(label); // Add to container
        }
    }

    // Handle logout trigger via hidden form submission
    const logoutLink = document.querySelector('.logout-trigger');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default action
            document.getElementById('logoutForm').submit(); // Submit logout form
        });
    }
});

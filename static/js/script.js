function confirmDelete() {

    return confirm("Are you sure you want to delete this student?");

}


function showWelcomeMessage() {

    const message = document.getElementById("welcome-message");

    if (message) {
        message.textContent = "Welcome! You are using the Student Management System.";
    }

}


document.addEventListener("DOMContentLoaded", function () {

    showWelcomeMessage();

});


function validateStudentForm() {

    const name = document.getElementById("name").value.trim();
    const department = document.getElementById("department").value.trim();
    const email = document.getElementById("email").value.trim();

    if (name === "") {
        alert("Name is required.");
        return false;
    }

    if (department === "") {
        alert("Department is required.");
        return false;
    }

    if (email === "") {
        alert("Email is required.");
        return false;
    }

    return true;

}


const addStudentForm = document.getElementById("add-student-form");
const editStudentForm = document.getElementById("edit-student-form");


if (addStudentForm) {

    addStudentForm.addEventListener("submit", function (event) {

        // const name = document.getElementById("name").value;
        // const department = document.getElementById("department").value;
        // const email = document.getElementById("email").value;

        // console.log("Name:", name);
        // console.log("Department:", department);
        // console.log("Email:", email);

        if (!validateStudentForm()) {
            event.preventDefault();
        }

    });

}


if (editStudentForm) {

    editStudentForm.addEventListener("submit", function (event) {

        if (!validateStudentForm()) {
            event.preventDefault();
        }

    });

}


const searchInput = document.getElementById("search-input");
const searchFeedback = document.getElementById("search-feedback");

if (searchInput) {

    searchInput.addEventListener("input", function () {

        const searchValue = searchInput.value.trim();

        if (searchValue === "") {
            searchFeedback.textContent = "";
        } else {
            searchFeedback.textContent = "Searching for: " + searchValue;
        }

    });

}

// function testFetchStudents() {

//     fetch("/students")
//         .then(function (response) {

//             console.log("Status:", response.status);
//             console.log("OK:", response.ok);

//             return response.text();

//         })
//         .then(function (data) {

//             console.log("Response received from Flask:");
//             console.log(data);

//         })
//         .catch(function (error) {

//             console.log("Fetch error:", error);

//         });

// }
// testFetchStudents();
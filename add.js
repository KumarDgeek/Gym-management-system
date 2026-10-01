let members = [];

const memberForm = document.getElementById("memberForm");
const memberTable = document.getElementById("memberTable");
const message = document.getElementById("message");


// Add Member
memberForm.addEventListener("submit", function(event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const phone = document.getElementById("phone").value;
    const gender = document.getElementById("gender").value;
    const plan = document.getElementById("plan").value;

    // Phone validation
    if (phone.length !== 10 || isNaN(phone)) {
        message.innerText = "❌ Enter a valid 10-digit phone number";
        message.style.color = "red";
        return;
    }

    const member = {
        id: Date.now(),
        name: name,
        age: age,
        phone: phone,
        gender: gender,
        plan: plan
    };

    members.push(member);

    // Save data in browser
    localStorage.setItem(
        "gymMembers",
        JSON.stringify(members)
    );

    message.innerText = "✅ Member added successfully!";
    message.style.color = "green";

    memberForm.reset();

    displayMembers();
});


// Display Members
function displayMembers() {

    memberTable.innerHTML = "";

    members.forEach(function(member, index) {

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${member.name}</td>
            <td>${member.age}</td>
            <td>${member.phone}</td>
            <td>${member.gender}</td>
            <td>${member.plan}</td>

            <td>
                <button
                    class="delete-btn"
                    onclick="deleteMember(${member.id})">
                    Delete
                </button>
            </td>
        `;

        memberTable.appendChild(row);
    });
}


// Delete Member
function deleteMember(id) {

    members = members.filter(function(member) {
        return member.id !== id;
    });

    localStorage.setItem(
        "gymMembers",
        JSON.stringify(members)
    );

    displayMembers();

    message.innerText = "🗑️ Member deleted successfully!";
    message.style.color = "red";
}


// Load saved members
function loadMembers() {

    const savedMembers =
        localStorage.getItem("gymMembers");

    if (savedMembers) {
        members = JSON.parse(savedMembers);
    }

    displayMembers();
}


// Start
loadMembers();
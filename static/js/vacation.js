function addComment(vacationId) {
  console.log("hii from add comments");
  const content = document.getElementById("comment-content").value;
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`/vacation/${vacationId}/comment/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `content=${encodeURIComponent(content)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      const commentsContainer = document.getElementById("comments-container");
      const commentElement = document.createElement("div");
      commentElement.className = "comment card";
      commentElement.innerHTML = `
            <p>${data.content}</p>
            <p>By: ${data.user}</p>
            <p>Posted: ${data.created_at}</p>
            <button onclick="upvoteComment(${data.id})" class="button">
                Upvote (<span id="upvotes-${data.id}">${data.upvotes}</span>)
            </button>
        `;
      commentsContainer.insertBefore(
        commentElement,
        commentsContainer.firstChild
      );
      document.getElementById("comment-content").value = "";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function upvoteComment(commentId) {
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  fetch(`/comment/${commentId}/upvote/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "X-Requested-With": "XMLHttpRequest",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const upvotesElement = document.getElementById(`upvotes-${commentId}`);
      upvotesElement.textContent = data.upvotes;
    });
}

function performsearch() {
  let debounceTimeout;

  const searchInput = document.getElementById("search-input");
  //   console.log(`You searched for: ${searchInput}`);
  searchInput.addEventListener("input", (e) => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      searchVacations(e.target.value);
    }, 1000);
  });
}

function searchVacations(query) {
  console.log("hii there form searchVacations");
  fetch(`/search/?q=${encodeURIComponent(query)}`)
    .then((response) => response.json())
    .then((data) => {
      const resultsContainer = document.getElementById("search-results");
      resultsContainer.innerHTML = "";

      data.results.forEach((vacation) => {
        const card = document.createElement("div");
        card.className = "vacation-card card";
        card.innerHTML = `
                    <img src="${vacation.image_url}" alt="${vacation.title}" class="vacation-image">
                    <div class="vacation-content">
                        <h3>${vacation.title}</h3>
                        <p>${vacation.description}</p>
                        <p>Category: ${vacation.category}</p>
                        <a href="/vacation/${vacation.id}" class="button">View Details</a>
                    </div>
                `;
        resultsContainer.appendChild(card);
      });

      if (data.results.length === 0) {
        resultsContainer.innerHTML =
          '<p class="no-results">No vacations found</p>';
      }
    });
}

const themeToggle = document.getElementById("themeToggle");
const body = document.body;

// Load saved theme preference
const savedTheme = localStorage.getItem("theme")  || 'light';
body.setAttribute("data-theme", savedTheme);
updateThemeToggleText();

themeToggle.addEventListener("click", () => {
    console.log("theme button is tapped");
  const currentTheme = body.getAttribute("data-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";

  body.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  updateThemeToggleText();
});

function updateThemeToggleText() {
  const currentTheme = body.getAttribute("data-theme");
  themeToggle.textContent =
    currentTheme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode";
}

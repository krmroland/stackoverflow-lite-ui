const sidebarLinks = document.querySelectorAll("#Sidebar .sidebar-link");

const questionFilters = document.querySelectorAll(
    "#Questions .question-filter"
);

let { pathname } = window.location;

sidebarLinks.forEach(
    link => (pathname === link.pathname ? link.classList.add("active") : null)
);

const activateQuestionFilterLink = () => {
    const { hash } = window.location;
    questionFilters.forEach(link => {
        link.hash === hash
            ? link.classList.add("active")
            : link.classList.remove("active");
    });
};

activateQuestionFilterLink();

//listen for when the url hash changes
window.addEventListener("hashchange", activateQuestionFilterLink);

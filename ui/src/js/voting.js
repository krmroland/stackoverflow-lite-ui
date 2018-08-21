const handleClick = e => {
    const button = e.currentTarget;

    button.classList.toggle("active");

    const closestButton =
        button.previousElementSibling || button.nextElementSibling;

    closestButton && closestButton.classList.remove("active");
};
document
    .querySelectorAll(".js-vote-button")
    .forEach(button => button.addEventListener("click", handleClick));

const autoSize = field => {
    // reset height
    field.style.height = "inherit";

    const computed = window.getComputedStyle(field);

    const height =
        parseFloat(computed.getPropertyValue("border-top-width"), 10) +
        parseFloat(computed.getPropertyValue("padding-top"), 10) +
        field.scrollHeight +
        parseFloat(computed.getPropertyValue("padding-bottom"), 10) +
        parseFloat(computed.getPropertyValue("border-bottom-width"), 10);

    field.style.height = height + "px";
};

document.querySelectorAll("textarea").forEach(field => {
    //activate initially
    autoSize(field);
    field.addEventListener("input", e => autoSize(e.currentTarget));
});

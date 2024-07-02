const content = document.querySelector("#content");
const nav = document.querySelector("header");

content.style.minHeight = `calc(100% - ${nav.getBoundingClientRect().height}px)`;

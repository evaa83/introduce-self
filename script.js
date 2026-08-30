const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".primary-nav");

menuButton?.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
  menuButton.querySelector(".sr-only").textContent = isOpen ? "關閉選單" : "開啟選單";
});

nav?.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    nav.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
    menuButton.querySelector(".sr-only").textContent = "開啟選單";
  }
});

const revealElements = document.querySelectorAll(".reveal");
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (reducedMotion || !("IntersectionObserver" in window)) {
  revealElements.forEach((element) => element.classList.add("visible"));
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px" },
  );

  revealElements.forEach((element) => observer.observe(element));
}

const simplified = document.documentElement.lang === "zh-Hans";
const menuOpenLabel = simplified ? "开启选单" : "開啟選單";
const menuCloseLabel = simplified ? "关闭选单" : "關閉選單";

const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector(".primary-nav");

menuButton?.addEventListener("click", () => {
  const isOpen = nav.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
  menuButton.querySelector(".sr-only").textContent = isOpen ? menuCloseLabel : menuOpenLabel;
});

nav?.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    nav.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
    menuButton.querySelector(".sr-only").textContent = menuOpenLabel;
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

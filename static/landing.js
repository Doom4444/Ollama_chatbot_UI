/* Ticker animation - horizontal scroll */
const ticker = document.querySelector(".ticker");
if (ticker) {
  const spans = ticker.querySelectorAll("span");
  const totalWidth = Array.from(spans).reduce((acc, s) => acc + s.offsetWidth + 16, 0);
  let offset = 0;
  setInterval(() => {
    offset -= 1;
    ticker.style.transform = `translateX(${offset}px)`;
    if (Math.abs(offset) >= totalWidth) {
      offset = 0;
    }
  }, 30);
}

/* Login button - scroll to chat section */
const loginBox = document.querySelector(".login-box");
const loginBtn = loginBox?.querySelector(".login-btn");
const emailInput = loginBox?.querySelector("input[type='text']");
const passwordInput = loginBox?.querySelector("input[type='password']");
if (loginBtn) {
  loginBtn.addEventListener("click", () => {
    const email = emailInput?.value?.trim() || "";
    const password = passwordInput?.value?.trim() || "";
    if (email === "" || password === "") {
      alert("Please enter email and password");
      return;
    }
    if (!email.includes("@")) {
      alert("Please enter a valid email");
      return;
    }
    alert("Welcome to X Investment");
    document.querySelector("#chat")?.scrollIntoView({ behavior: "smooth" });
  });
}

/* Navbar scroll effect */
const navbar = document.querySelector(".navbar");
const navLinks = document.querySelectorAll(".nav-links a");
if (navbar) {
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.style.background = "rgba(2, 12, 27, 0.98)";
    } else {
      navbar.style.background = "rgba(2, 12, 27, 0.9)";
    }
  });
}

/* Smooth scroll for nav links */
navLinks?.forEach((link) => {
  link.addEventListener("click", (e) => {
    const href = link.getAttribute("href");
    if (href?.startsWith("#")) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    }
  });
});

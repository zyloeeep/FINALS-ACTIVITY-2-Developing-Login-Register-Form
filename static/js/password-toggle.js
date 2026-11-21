document.querySelectorAll("[data-toggle-password]").forEach((button) => {
  const input = document.getElementById(button.dataset.togglePassword);
  const icon = button.querySelector("img");

  button.addEventListener("click", () => {
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    icon.src = show ? button.dataset.iconVisible : button.dataset.iconHidden;
    button.setAttribute("aria-label", show ? "Hide password" : "Show password");
  });
});
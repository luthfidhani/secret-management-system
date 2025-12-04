function authApp() {
  return {
    masterPassword: "",
    confirmPassword: "",
    showPassword: false,
    loading: false,
    error: "",
    showSetup: false,
    strengthColors: {
      1: "bg-red-500",
      2: "bg-yellow-500",
      3: "bg-vault-400",
      4: "bg-vault-500",
    },

    get passwordStrength() {
      const pwd = this.masterPassword;
      if (!pwd) return 0;

      let strength = 0;
      if (pwd.length >= 8) strength++;
      if (pwd.length >= 12) strength++;
      if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) strength++;
      if (/[0-9]/.test(pwd) && /[^A-Za-z0-9]/.test(pwd)) strength++;

      return strength;
    },

    get strengthText() {
      const texts = ["", "Weak", "Fair", "Good", "Strong"];
      return texts[this.passwordStrength] || "";
    },

    async login() {
      this.error = "";
      this.loading = true;

      try {
        const response = await fetch("/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({
            master_password: this.masterPassword,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          window.location.href = "/dashboard";
        } else {
          this.error = data.error || "Login failed";
        }
      } catch (err) {
        this.error = "Network error. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    async setup() {
      this.error = "";

      if (this.masterPassword !== this.confirmPassword) {
        this.error = "Passwords do not match";
        return;
      }

      if (this.masterPassword.length < 8) {
        this.error = "Password must be at least 8 characters";
        return;
      }

      this.loading = true;

      try {
        const response = await fetch("/api/setup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify({
            master_password: this.masterPassword,
            confirm_password: this.confirmPassword,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          window.location.href = "/dashboard";
        } else {
          this.error = data.error || "Setup failed";
        }
      } catch (err) {
        this.error = "Network error. Please try again.";
      } finally {
        this.loading = false;
      }
    },
  };
}

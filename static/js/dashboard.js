function dashboardApp() {
  return {
    entries: [],
    loading: true,
    filter: "all",
    searchQuery: "",
    mobileMenuOpen: false,
    modalOpen: false,
    modalMode: "create",
    formData: {},
    showPassword: false,
    saving: false,
    error: "",
    toast: { show: false, message: "", type: "success" },

    entryTypes: [
      {
        type: "login",
        label: "Logins",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path></svg>',
        color: "text-vault-400",
        bgColor: "bg-vault-500/20",
      },
      {
        type: "note",
        label: "Notes",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>',
        color: "text-yellow-400",
        bgColor: "bg-yellow-500/20",
      },
      {
        type: "credit_card",
        label: "Credit Cards",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>',
        color: "text-purple-400",
        bgColor: "bg-purple-500/20",
      },
      {
        type: "identity",
        label: "Identities",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2"></path></svg>',
        color: "text-blue-400",
        bgColor: "bg-blue-500/20",
      },
      {
        type: "api_credential",
        label: "API Credentials",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path></svg>',
        color: "text-orange-400",
        bgColor: "bg-orange-500/20",
      },
      {
        type: "database",
        label: "Databases",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>',
        color: "text-cyan-400",
        bgColor: "bg-cyan-500/20",
      },
      {
        type: "server",
        label: "Servers",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path></svg>',
        color: "text-red-400",
        bgColor: "bg-red-500/20",
      },
      {
        type: "software_license",
        label: "Software Licenses",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path></svg>',
        color: "text-pink-400",
        bgColor: "bg-pink-500/20",
      },
      {
        type: "ssh_key",
        label: "SSH Keys",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"></path></svg>',
        color: "text-emerald-400",
        bgColor: "bg-emerald-500/20",
      },
      {
        type: "wifi",
        label: "WiFi Networks",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"></path></svg>',
        color: "text-indigo-400",
        bgColor: "bg-indigo-500/20",
      },
      {
        type: "bank_account",
        label: "Bank Accounts",
        icon: '<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>',
        color: "text-teal-400",
        bgColor: "bg-teal-500/20",
      },
    ],

    getEntryType(type) {
      return this.entryTypes.find((t) => t.type === type);
    },

    getEntrySubtitle(entry) {
      switch (entry.type) {
        case "login":
          return entry.username || "";
        case "note":
          return entry.preview || "";
        case "credit_card":
          return entry.cardholder_name || "";
        case "identity":
          return entry.full_name || "";
        case "api_credential":
          return entry.permissions || "";
        case "database":
          return entry.database_type || "";
        case "server":
          return entry.hostname || entry.ip_address || "";
        case "software_license":
          return entry.product || "";
        case "ssh_key":
          return entry.username || "";
        case "wifi":
          return entry.ssid || "";
        case "bank_account":
          return entry.bank_name || "";
        default:
          return "";
      }
    },

    getEntryMeta(entry) {
      switch (entry.type) {
        case "login":
          return entry.url || "";
        case "note":
          return "";
        case "credit_card":
          return entry.card_last4 ? "•••• " + entry.card_last4 : "";
        case "identity":
          return entry.email || "";
        case "api_credential":
          return entry.expiration_date || "";
        case "database":
          return entry.host || "";
        case "server":
          return entry.os || "";
        case "software_license":
          return entry.expiry_date || "";
        case "ssh_key":
          return entry.host || "";
        case "wifi":
          return entry.security_type || "";
        case "bank_account":
          return entry.account_last4 ? "•••• " + entry.account_last4 : "";
        default:
          return "";
      }
    },

    get filteredEntries() {
      let filtered = this.entries;
      if (this.filter !== "all") {
        filtered = filtered.filter((e) => e.type === this.filter);
      }
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter((e) => {
          const searchFields = [
            e.title,
            e.username,
            e.url,
            e.full_name,
            e.email,
            e.ssid,
            e.host,
            e.hostname,
            e.ip_address,
            e.bank_name,
            e.product,
            e.cardholder_name,
            e.database_type,
          ];
          return searchFields.some((f) => f && f.toLowerCase().includes(query));
        });
      }
      return filtered;
    },

    async init() {
      await this.loadEntries();
    },

    async loadEntries() {
      this.loading = true;
      try {
        const response = await fetch("/api/entries", {
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });

        if (response.status === 401) {
          window.location.href = "/";
          return;
        }

        const data = await response.json();
        this.entries = data.entries || [];
      } catch (err) {
        this.showToast("Failed to load entries", "error");
      } finally {
        this.loading = false;
      }
    },

    openModal(type) {
      this.modalMode = "create";
      this.formData = {
        type: type,
        title: "",
        notes: "",
        // Login
        url: "",
        username: "",
        password: "",
        // Credit Card
        cardholder_name: "",
        card_number: "",
        expiration_date: "",
        security_code: "",
        pin: "",
        // Identity
        prefix_title: "",
        full_name: "",
        email: "",
        phone: "",
        birth_date: "",
        gender: "",
        organization: "",
        address: "",
        postal_code: "",
        city: "",
        state: "",
        country: "",
        ssn: "",
        passport_number: "",
        license_number: "",
        website: "",
        x_handle: "",
        linkedin: "",
        reddit: "",
        facebook: "",
        yahoo: "",
        instagram: "",
        company: "",
        job_title: "",
        work_website: "",
        work_phone: "",
        work_email: "",
        // API Credential
        api_key: "",
        api_secret: "",
        permissions: "",
        // Database
        host: "",
        port: "",
        database_type: "",
        database_name: "",
        // Server
        ip_address: "",
        hostname: "",
        os: "",
        // Software License
        license_key: "",
        product: "",
        expiry_date: "",
        owner: "",
        // SSH Key
        public_key: "",
        private_key: "",
        passphrase: "",
        // WiFi
        ssid: "",
        security_type: "",
        // Bank Account
        bank_name: "",
        account_number: "",
        routing_number: "",
        account_type: "",
        iban: "",
        swift_bic: "",
        holder_name: "",
      };
      this.showPassword = false;
      this.error = "";
      this.modalOpen = true;
    },

    async viewEntry(id) {
      try {
        const response = await fetch(`/api/entries/${id}`, {
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });

        if (response.status === 401) {
          window.location.href = "/";
          return;
        }

        const data = await response.json();
        this.formData = { ...data.entry };
        this.modalMode = "view";
        this.showPassword = false;
        this.error = "";
        this.modalOpen = true;
      } catch (err) {
        this.showToast("Failed to load entry", "error");
      }
    },

    closeModal() {
      this.modalOpen = false;
      this.formData = {};
      this.error = "";
    },

    async saveEntry() {
      if (!this.formData.title.trim()) {
        this.error = "Title is required";
        return;
      }

      this.saving = true;
      this.error = "";

      try {
        const isEdit = this.modalMode === "edit";
        const url = isEdit
          ? `/api/entries/${this.formData.id}`
          : "/api/entries";
        const method = isEdit ? "PUT" : "POST";

        const response = await fetch(url, {
          method: method,
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
          body: JSON.stringify(this.formData),
        });

        if (response.status === 401) {
          window.location.href = "/";
          return;
        }

        const data = await response.json();

        if (response.ok) {
          this.showToast(
            isEdit ? "Entry updated!" : "Entry created!",
            "success"
          );
          this.closeModal();
          await this.loadEntries();
        } else {
          this.error = data.error || "Failed to save";
        }
      } catch (err) {
        this.error = "Network error. Please try again.";
      } finally {
        this.saving = false;
      }
    },

    async confirmDelete() {
      if (
        !confirm(
          "Are you sure you want to delete this entry? This cannot be undone."
        )
      ) {
        return;
      }

      try {
        const response = await fetch(`/api/entries/${this.formData.id}`, {
          method: "DELETE",
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });

        if (response.status === 401) {
          window.location.href = "/";
          return;
        }

        if (response.ok) {
          this.showToast("Entry deleted!", "success");
          this.closeModal();
          await this.loadEntries();
        } else {
          const data = await response.json();
          this.showToast(data.error || "Failed to delete", "error");
        }
      } catch (err) {
        this.showToast("Network error", "error");
      }
    },

    async logout() {
      try {
        await fetch("/api/logout", {
          method: "POST",
          headers: { "X-Requested-With": "XMLHttpRequest" },
        });
      } catch (err) {
        // Ignore errors
      }
      window.location.href = "/";
    },

    generatePassword() {
      const charset =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?";
      let password = "";
      const array = new Uint32Array(20);
      crypto.getRandomValues(array);
      for (let i = 0; i < 20; i++) {
        password += charset[array[i] % charset.length];
      }
      this.formData.password = password;
      this.showPassword = true;
    },

    async copyToClipboard(text) {
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        this.showToast("Copied to clipboard!", "success");
      } catch (err) {
        this.showToast("Failed to copy", "error");
      }
    },

    showToast(message, type = "success") {
      this.toast = { show: true, message, type };
      setTimeout(() => {
        this.toast.show = false;
      }, 3000);
    },
  };
}

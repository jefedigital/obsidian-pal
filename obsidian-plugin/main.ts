import { App, Plugin, PluginSettingTab, Setting, Notice, TFile, ItemView, WorkspaceLeaf } from 'obsidian';

interface YourPalPluginSettings {
    backendUrl: string;
}

const DEFAULT_SETTINGS: YourPalPluginSettings = {
    backendUrl: 'http://localhost:8000'
}

const VIEW_TYPE_SEARCH = "yourpal-search-view";

export default class YourPalPlugin extends Plugin {
    settings: YourPalPluginSettings;
    searchView: SearchView;

    async onload() {
        await this.loadSettings();
        await this.checkBackendVersion();

        this.registerView(
            VIEW_TYPE_SEARCH,
            (leaf) => (this.searchView = new SearchView(leaf, this))
        );

        this.addRibbonIcon('search', 'YourPal Search', () => {
            this.activateView();
        });

        this.addCommand({
            id: 'open-yourpal-search',
            name: 'Open YourPal Search',
            callback: () => {
                this.activateView();
            },
        });

        this.addSettingTab(new YourPalSettingTab(this.app, this));
    }

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }

    async activateView() {
        const { workspace } = this.app;

        let leaf: WorkspaceLeaf | null = null;
        const leaves = workspace.getLeavesOfType(VIEW_TYPE_SEARCH);

        if (leaves.length > 0) {
            // A leaf with our view already exists, use that
            leaf = leaves[0];
        } else {
            // Our view doesn't exist, create a new leaf in the right sidebar
            leaf = workspace.getRightLeaf(false);
            if (leaf) {
                await leaf.setViewState({ type: VIEW_TYPE_SEARCH, active: true });
            }
        }

        // Reveal the leaf in the right sidebar
        if (leaf) {
            workspace.revealLeaf(leaf);
        }
    }

    async sendHelloWorldRequest() {
        try {
            const response = await fetch(`${this.settings.backendUrl}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'hello_world',
                    content: ''
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return response.json();
        } catch (error) {
            console.error('Error:', error);
            if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
                throw new Error('Unable to connect to the backend. Please check your internet connection and backend URL.');
            }
            throw error;
        }
    }

    async sendIndexVaultRequest() {
        try {
            const vault = this.app.vault;
            const vaultName = vault.getName();
            const files = vault.getMarkdownFiles();
            const fileContents: { [key: string]: string } = {};

            // Create a notice to show progress
            const notice = new Notice('Indexing vault...', 0);

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const content = await vault.cachedRead(file);
                fileContents[file.path] = content;
                
                // Update progress
                const progress = Math.round((i + 1) / files.length * 100);
                notice.setMessage(`Indexing file ${i + 1} of ${files.length} (${progress}%)`);
            }

            const response = await fetch(`${this.settings.backendUrl}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'index_vault',
                    content: [vaultName, fileContents]
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            notice.hide();
            return response.json();
        } catch (error) {
            console.error('Error:', error);
            if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
                throw new Error('Unable to connect to the backend. Please check your internet connection and backend URL.');
            }
            throw error;
        }
    }

    async sendSearchVaultRequest(query: string) {
        try {
            const vault = this.app.vault;
            const vaultName = vault.getName();

            const response = await fetch(`${this.settings.backendUrl}/process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'search_vault',
                    content: [vaultName, query]
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return response.json();
        } catch (error) {
            console.error('Error:', error);
            if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
                throw new Error('Unable to connect to the backend. Please check your internet connection and backend URL.');
            }
            throw error;
        }
    }

    async checkBackendVersion() {
        try {
            const response = await fetch(`${this.settings.backendUrl}/version`);
            const version = await response.text();
            if (version !== this.manifest.version) {
                new Notice(`Warning: Plugin version (${this.manifest.version}) does not match backend version (${version})`);
            }
        } catch (error) {
            console.error('Failed to check backend version:', error);
        }
    }
}

class SearchView extends ItemView {
    plugin: YourPalPlugin;
    searchInput: HTMLInputElement;
    searchResults: HTMLElement;

    constructor(leaf: WorkspaceLeaf, plugin: YourPalPlugin) {
        super(leaf);
        this.plugin = plugin;
    }

    getViewType() {
        return VIEW_TYPE_SEARCH;
    }

    getDisplayText() {
        return "YourPal Search";
    }

    async onOpen() {
        const container = this.containerEl.children[1];
        container.empty();

        // Create a container for the top section
        const topSection = container.createEl("div", { cls: "yourpal-top-section" });

        // Add the Index Vault button
        const indexButton = topSection.createEl("button", { text: "Index Vault" });
        indexButton.addEventListener("click", async () => {
            try {
                const response = await this.plugin.sendIndexVaultRequest();
                new Notice(response.result);
            } catch (error) {
                console.error('Error:', error);
                new Notice(`Error: ${error.message}`);
            }
        });

        // Add some space between the button and the search input
        topSection.createEl("br");
        topSection.createEl("br");

        // Add the search input
        this.searchInput = topSection.createEl("input", {
            type: "text",
            placeholder: "Enter your search query"
        });

        // Create a container for search results
        this.searchResults = container.createEl("div", { cls: "yourpal-search-results" });

        // Add event listener for search
        this.searchInput.addEventListener("keydown", async (event) => {
            if (event.key === "Enter") {
                const query = this.searchInput.value;
                if (query) {
                    try {
                        const response = await this.plugin.sendSearchVaultRequest(query);
                        this.displaySearchResults(response.result);
                    } catch (error) {
                        console.error('Error:', error);
                        new Notice(`Error: ${error.message}`);
                    }
                }
            }
        });

        // Add some basic styling
        this.addStyle();
    }

    displaySearchResults(results: Array<{file: string, score: number}>) {
        this.searchResults.empty();
        const ul = this.searchResults.createEl("ul");
        for (const result of results) {
            const li = ul.createEl("li");
            const a = li.createEl("a", { text: result.file, href: "#" });
            a.addEventListener("click", (event) => {
                event.preventDefault();
                this.openFile(result.file);
            });
            li.createEl("span", { text: ` (${result.score.toFixed(2)})` });
        }
    }

    async openFile(filePath: string) {
        const file = this.app.vault.getAbstractFileByPath(filePath);
        if (file instanceof TFile) {
            await this.app.workspace.getLeaf().openFile(file);
        } else {
            new Notice(`File not found: ${filePath}`);
        }
    }

    addStyle() {
        const style = document.createElement('style');
        style.textContent = `
            .yourpal-top-section {
                margin-bottom: 20px;
            }
            .yourpal-top-section button {
                margin-bottom: 10px;
            }
            .yourpal-top-section input {
                width: 100%;
            }
            .yourpal-search-results ul {
                padding-left: 20px;
            }
            .yourpal-search-results li {
                margin-bottom: 5px;
            }
        `;
        document.head.append(style);
    }
}

class YourPalSettingTab extends PluginSettingTab {
    plugin: YourPalPlugin;

    constructor(app: App, plugin: YourPalPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const {containerEl} = this;

        containerEl.empty();

        new Setting(containerEl)
            .setName('Backend URL')
            .setDesc('Enter the URL of your YourPal backend')
            .addText(text => text
                .setPlaceholder('Enter URL')
                .setValue(this.plugin.settings.backendUrl)
                .onChange(async (value) => {
                    this.plugin.settings.backendUrl = value;
                    await this.plugin.saveSettings();
                }));

        new Setting(containerEl)
            .setName('Test Connection')
            .setDesc('Test the connection to your backend')
            .addButton(button => button
                .setButtonText('Test')
                .onClick(async () => {
                    try {
                        await this.plugin.sendHelloWorldRequest();
                        new Notice('Connection successful!');
                    } catch (error) {
                        new Notice(`Connection failed: ${error.message}`);
                    }
                }));
    }
}
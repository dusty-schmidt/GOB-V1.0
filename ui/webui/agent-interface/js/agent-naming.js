/**
 * Agent Naming Service - Client-side module for managing dynamic agent names
 * 
 * This module handles:
 * - Fetching current agent identity from the API
 * - Updating UI elements with current agent names
 * - Scheduling automatic updates at midnight
 * - Caching names for performance
 */

class AgentNamingService {
    constructor() {
        this.currentIdentity = null;
        this.lastUpdated = null;
        this.updateTimer = null;
        this.cacheDuration = 5 * 60 * 1000; // 5 minutes cache
        this.listeners = []; // Event listeners for name changes
        
        // Initialize the service
        this.initialize();
    }
    
    async initialize() {
        console.log('[AgentNaming] Initializing agent naming service...');
        
        try {
            // Fetch current identity
            await this.updateIdentity();
            
            // Set up periodic updates
            this.scheduleNextUpdate();
            
            // Listen for visibility changes to refresh when page becomes visible
            document.addEventListener('visibilitychange', () => {
                if (!document.hidden && this.shouldRefresh()) {
                    this.updateIdentity();
                }
            });
            
            console.log('[AgentNaming] Agent naming service initialized successfully');
        } catch (error) {
            console.error('[AgentNaming] Failed to initialize agent naming service:', error);
            // Fall back to default name
            this.setFallbackIdentity();
        }
    }
    
    async updateIdentity() {
        try {
            console.log('[AgentNaming] Fetching current agent identity...');
            
            const response = await fetch('/api_agent_identity', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'success' && data.agent_identity) {
                const oldIdentity = this.currentIdentity;
                this.currentIdentity = data.agent_identity;
                this.lastUpdated = new Date();
                
                // Update UI elements
                this.updateUI();
                
                // Notify listeners if identity changed
                if (oldIdentity && oldIdentity.acronym !== this.currentIdentity.acronym) {
                    this.notifyListeners(this.currentIdentity, oldIdentity);
                }
                
                console.log(`[AgentNaming] Identity updated: ${this.currentIdentity.acronym} (${this.currentIdentity.full_name})`);
            } else {
                throw new Error(data.message || 'Invalid response from API');
            }
        } catch (error) {
            console.error('[AgentNaming] Failed to update identity:', error);
            
            // If we don't have any identity yet, use fallback
            if (!this.currentIdentity) {
                this.setFallbackIdentity();
            }
        }
    }
    
    setFallbackIdentity() {
        console.log('[AgentNaming] Using fallback identity');
        this.currentIdentity = {
            acronym: 'GOB',
            full_name: 'General Operations Bot',
            type: 'main',
            date: new Date().toISOString().split('T')[0]
        };
        this.lastUpdated = new Date();
        this.updateUI();
    }
    
    updateUI() {
        if (!this.currentIdentity) return;
        
        const { acronym, full_name } = this.currentIdentity;
        
        // Update page title
        document.title = acronym;
        
        // Update version info
        const versionElement = document.getElementById('gobversion');
        if (versionElement) {
            const versionText = versionElement.textContent;
            const newVersionText = versionText.replace(/^[A-Z]{3,4}/, acronym);
            versionElement.textContent = newVersionText;
        }
        
        // Update any elements with the agent-name class
        const nameElements = document.querySelectorAll('.agent-name, [data-agent-name]');
        nameElements.forEach(element => {
            if (element.hasAttribute('data-agent-name')) {
                const nameType = element.getAttribute('data-agent-name');
                if (nameType === 'acronym') {
                    element.textContent = acronym;
                } else if (nameType === 'full') {
                    element.textContent = full_name;
                }
            } else {
                element.textContent = acronym;
            }
        });
        
        // Update any title attributes or tooltips
        const titleElements = document.querySelectorAll('[data-agent-title]');
        titleElements.forEach(element => {
            element.setAttribute('title', full_name);
        });
        
        // Dispatch custom event for other scripts to listen to
        const event = new CustomEvent('agentNameUpdated', {
            detail: { identity: this.currentIdentity }
        });
        document.dispatchEvent(event);
    }
    
    scheduleNextUpdate() {
        // Clear existing timer
        if (this.updateTimer) {
            clearTimeout(this.updateTimer);
        }
        
        // Calculate time until next midnight
        const now = new Date();
        const tomorrow = new Date(now);
        tomorrow.setDate(tomorrow.getDate() + 1);
        tomorrow.setHours(0, 0, 1, 0); // 1 second past midnight
        
        const timeUntilMidnight = tomorrow.getTime() - now.getTime();
        
        console.log(`[AgentNaming] Next update scheduled in ${Math.round(timeUntilMidnight / 1000 / 60)} minutes`);
        
        this.updateTimer = setTimeout(() => {
            console.log('[AgentNaming] Midnight update triggered');
            this.updateIdentity().then(() => {
                // Schedule next update
                this.scheduleNextUpdate();
            });
        }, timeUntilMidnight);
    }
    
    shouldRefresh() {
        if (!this.lastUpdated) return true;
        
        const now = new Date();
        const timeSinceUpdate = now.getTime() - this.lastUpdated.getTime();
        
        // Refresh if cache expired or if it's a new day
        return timeSinceUpdate > this.cacheDuration || 
               now.toDateString() !== this.lastUpdated.toDateString();
    }
    
    // Public API methods
    getCurrentIdentity() {
        return this.currentIdentity;
    }
    
    getCurrentAcronym() {
        return this.currentIdentity ? this.currentIdentity.acronym : 'GOB';
    }
    
    getCurrentFullName() {
        return this.currentIdentity ? this.currentIdentity.full_name : 'General Operations Bot';
    }
    
    async forceUpdate() {
        console.log('[AgentNaming] Force update requested');
        await this.updateIdentity();
    }
    
    // Event listener management
    addChangeListener(callback) {
        this.listeners.push(callback);
    }
    
    removeChangeListener(callback) {
        const index = this.listeners.indexOf(callback);
        if (index > -1) {
            this.listeners.splice(index, 1);
        }
    }
    
    notifyListeners(newIdentity, oldIdentity) {
        this.listeners.forEach(callback => {
            try {
                callback(newIdentity, oldIdentity);
            } catch (error) {
                console.error('[AgentNaming] Error in change listener:', error);
            }
        });
    }
    
    destroy() {
        if (this.updateTimer) {
            clearTimeout(this.updateTimer);
            this.updateTimer = null;
        }
        this.listeners = [];
    }
}

// Global instance
let agentNamingService = null;

// Initialize the service when DOM is ready
function initializeAgentNaming() {
    if (agentNamingService) {
        agentNamingService.destroy();
    }
    agentNamingService = new AgentNamingService();
    
    // Expose globally for access from other scripts
    window.agentNaming = agentNamingService;
}

// Initialize when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeAgentNaming);
} else {
    initializeAgentNaming();
}

// Export for module usage
export { AgentNamingService, initializeAgentNaming };

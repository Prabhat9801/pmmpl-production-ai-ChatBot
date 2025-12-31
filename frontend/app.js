/**
 * Frontend JavaScript for AI Data Assistant
 * Handles chat interactions, API calls, and UI updates
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const sidebar = document.getElementById('sidebar');
const toggleSidebarBtn = document.getElementById('toggleSidebarBtn');
const newChatBtn = document.getElementById('newChatBtn');
const sessionList = document.getElementById('sessionList');
const clearAllBtn = document.getElementById('clearAllBtn');
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const statusIndicator = document.getElementById('statusIndicator');

// State
let isProcessing = false;
let currentSessionId = null;
let sessions = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSessionsFromStorage();
    initializeSession();
    checkHealth();
    setupEventListeners();
    autoResizeTextarea();
});

// Event Listeners
function setupEventListeners() {
    // Toggle sidebar
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
    
    // New chat
    newChatBtn.addEventListener('click', () => {
        createNewSession();
    });
    
    // Clear all chats
    clearAllBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all chat history?')) {
            clearAllSessions();
        }
    });
    
    // Send message
    sendBtn.addEventListener('click', sendMessage);
    
    // Enter to send, Shift+Enter for new line
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Enable/disable send button based on input
    userInput.addEventListener('input', () => {
        const hasText = userInput.value.trim().length > 0;
        sendBtn.disabled = !hasText || isProcessing;
        autoResizeTextarea();
    });
}

// Auto-resize textarea
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 200) + 'px';
}

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            statusIndicator.style.background = '#10a37f';
            statusIndicator.title = `System Healthy | Last refresh: ${new Date(data.last_refresh).toLocaleTimeString()}`;
        } else {
            statusIndicator.style.background = '#f59e0b';
            statusIndicator.title = 'System Degraded';
        }
    } catch (error) {
        statusIndicator.style.background = '#ef4444';
        statusIndicator.title = 'System Offline';
        console.error('Health check failed:', error);
    }
}

// Send message
async function sendMessage() {
    const question = userInput.value.trim();
    if (!question || isProcessing) return;
    
    // Add user message to chat
    addMessage(question, 'user');
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    
    // Set processing state
    isProcessing = true;
    
    // Add typing indicator
    const typingId = addTypingIndicator();
    
    try {
        // Get conversation context (last 20 messages)
        const conversationContext = getConversationContext();
        
        // Call API with context
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                question,
                session_id: currentSessionId,
                conversation_history: conversationContext
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add bot response
        addMessage(
            data.answer,
            'bot',
            {
                confidence: data.confidence,
                rowsFound: data.rows_found,
                dataPreview: data.data_preview,
                queryType: data.query_type
            }
        );
        
        // Update health status
        checkHealth();
        
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage(
            `Sorry, I encountered an error: ${error.message}. Please make sure the backend server is running.`,
            'bot',
            { confidence: 0 }
        );
        console.error('Error sending message:', error);
    } finally {
        isProcessing = false;
    }
}

// Get conversation context for API
function getConversationContext() {
    const session = sessions.find(s => s.id === currentSessionId);
    if (!session || !session.messages) return [];
    
    const messages = session.messages;
    const contextMessages = [];
    
    // Get last 5 full messages (reduced from 20 for token optimization)
    const recentMessages = messages.slice(-5);
    
    // If there are more than 5 messages, summarize older ones
    if (messages.length > 5) {
        const olderMessages = messages.slice(0, -5);
        const summary = summarizeMessages(olderMessages);
        contextMessages.push({
            role: 'system',
            content: `Previous conversation summary: ${summary}`
        });
    }
    
    // Add recent messages in full
    recentMessages.forEach(msg => {
        contextMessages.push({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.text
        });
    });
    
    return contextMessages;
}

// Summarize older messages
function summarizeMessages(messages) {
    const userQuestions = messages
        .filter(m => m.type === 'user')
        .map(m => m.text);
    
    if (userQuestions.length === 0) return 'No previous context.';
    
    const topics = userQuestions.slice(0, 5).join('; ');
    return `User previously asked about: ${topics}. Total ${messages.length} earlier messages.`;
}

// Convert markdown tables to HTML tables
function convertMarkdownTables(text) {
    // Match markdown tables (lines with | characters)
    const tableRegex = /((?:^\|.+\|\s*$\n?)+)/gm;
    
    return text.replace(tableRegex, (match) => {
        const lines = match.trim().split('\n');
        if (lines.length < 2) return match;
        
        // Check if second line is a separator (| --- | --- |)
        if (!lines[1].match(/^\|[\s\-:|]+\|$/)) return match;
        
        // Parse header
        const headers = lines[0].split('|').map(h => h.trim()).filter(h => h);
        
        // Parse rows (skip separator line)
        const rows = lines.slice(2).map(line => {
            return line.split('|').map(cell => cell.trim()).filter(cell => cell !== '');
        }).filter(row => row.length > 0);
        
        // Build HTML table
        let html = '<table class="markdown-table">';
        html += '<thead><tr>';
        headers.forEach(h => html += `<th>${h}</th>`);
        html += '</tr></thead>';
        html += '<tbody>';
        rows.forEach(row => {
            html += '<tr>';
            row.forEach(cell => html += `<td>${cell}</td>`);
            html += '</tr>';
        });
        html += '</tbody></table>';
        
        return html;
    });
}

// Add message to chat
function addMessage(text, type, metadata = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${type}-avatar`;
    avatar.textContent = type === 'user' ? 'You' : 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    
    // Format message text with markdown-like formatting
    let formattedText = text;
    
    if (type === 'bot') {
        // Convert markdown tables to HTML tables FIRST (before other processing)
        formattedText = convertMarkdownTables(formattedText);
        
        // Convert markdown headers to HTML (must be done before line breaks)
        formattedText = formattedText.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        formattedText = formattedText.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        formattedText = formattedText.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        
        // Convert **bold** to <strong>
        formattedText = formattedText.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Convert numbered lists (1. 2. 3.)
        formattedText = formattedText.replace(/^(\d+)\.\s+(.+)$/gm, '<oli>$2</oli>');
        
        // Wrap consecutive <oli> items in <ol>
        formattedText = formattedText.replace(/(<oli>.*<\/oli>(\n)?)+/gs, function(match) {
            const items = match.replace(/<\/?oli>/g, '').split('\n').filter(item => item.trim());
            return '<ol>' + items.map(item => `<li>${item}</li>`).join('') + '</ol>';
        });
        
        // Convert bullet points • to styled list items
        formattedText = formattedText.replace(/^[•\-\*]\s+(.+)$/gm, '<li>$1</li>');
        
        // Wrap consecutive <li> items in <ul>
        formattedText = formattedText.replace(/(<li>.*<\/li>(\n)?)+/gs, '<ul>$&</ul>');
        
        // Convert line breaks to <br>
        formattedText = formattedText.replace(/\n/g, '<br>');
        
        // Wrap in paragraph
        messageText.innerHTML = formattedText;
    } else {
        // User messages - simple line break conversion
        formattedText = formattedText.replace(/\n/g, '<br>');
        messageText.innerHTML = `<p>${formattedText}</p>`;
    }
    
    content.appendChild(messageText);
    
    // Add data table if present
    if (metadata.dataPreview && metadata.dataPreview.length > 0) {
        const tableContainer = createDataTable(metadata.dataPreview);
        content.appendChild(tableContainer);
    }
    
    // Add metadata for bot messages
    if (type === 'bot' && metadata.confidence !== undefined) {
        const meta = document.createElement('div');
        meta.className = 'message-meta';
        
        // Confidence badge
        if (metadata.confidence !== null) {
            const confidenceSpan = document.createElement('span');
            confidenceSpan.className = 'confidence-badge';
            
            const confidencePercent = Math.round(metadata.confidence * 100);
            let confidenceClass = 'confidence-low';
            if (confidencePercent >= 70) confidenceClass = 'confidence-high';
            else if (confidencePercent >= 50) confidenceClass = 'confidence-medium';
            
            confidenceSpan.classList.add(confidenceClass);
            confidenceSpan.textContent = `Confidence: ${confidencePercent}%`;
            meta.appendChild(confidenceSpan);
        }
        
        // Rows found
        if (metadata.rowsFound !== null && metadata.rowsFound !== undefined) {
            const rowsSpan = document.createElement('span');
            rowsSpan.textContent = `${metadata.rowsFound} rows found`;
            meta.appendChild(rowsSpan);
        }
        
        content.appendChild(meta);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    
    // Save to session first
    if (currentSessionId && !metadata.skipSave) {
        saveMessageToSession(text, type, metadata);
    }
    
    // Single scroll at the end
    scrollToBottom();
}

// Create data table
function createDataTable(data) {
    const container = document.createElement('div');
    container.className = 'data-table-container';
    
    const table = document.createElement('table');
    table.className = 'data-table';
    
    // Create header
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    const columns = Object.keys(data[0]);
    
    columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
    });
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    // Create body
    const tbody = document.createElement('tbody');
    
    data.forEach(row => {
        const tr = document.createElement('tr');
        columns.forEach(col => {
            const td = document.createElement('td');
            td.textContent = row[col] !== null && row[col] !== undefined ? row[col] : '';
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    });
    
    table.appendChild(tbody);
    container.appendChild(table);
    
    return container;
}

// Add typing indicator
function addTypingIndicator() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot-avatar';
    avatar.textContent = 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const typing = document.createElement('div');
    typing.className = 'typing-indicator';
    typing.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    content.appendChild(typing);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    // Don't scroll here - will scroll when actual message is added
    
    return 'typing-indicator';
}

// Remove typing indicator
function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) {
        indicator.remove();
    }
}

// Scroll to bottom
function scrollToBottom() {
    // Instant scroll without animation to prevent jitter
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Session Management
function loadSessionsFromStorage() {
    const saved = localStorage.getItem('chatSessions');
    if (saved) {
        sessions = JSON.parse(saved);
    }
}

function saveSessionsToStorage() {
    localStorage.setItem('chatSessions', JSON.stringify(sessions));
}

function initializeSession() {
    if (sessions.length === 0) {
        createNewSession();
    } else {
        currentSessionId = sessions[0].id;
        loadSession(currentSessionId);
    }
    renderSessions();
}

function createNewSession() {
    const sessionId = Date.now().toString();
    const newSession = {
        id: sessionId,
        title: 'New Chat',
        messages: [],
        createdAt: new Date().toISOString()
    };
    
    sessions.unshift(newSession);
    currentSessionId = sessionId;
    saveSessionsToStorage();
    renderSessions();
    clearChatDisplay();
}

function loadSession(sessionId) {
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return;
    
    currentSessionId = sessionId;
    clearChatDisplay();
    
    // Render saved messages (skip saving back to session)
    session.messages.forEach(msg => {
        addMessage(msg.text, msg.type, { ...msg.metadata, skipSave: true });
    });
    
    renderSessions();
}

async function deleteSession(sessionId) {
    // Clear cache for this session
    try {
        await fetch(`${API_BASE_URL}/sessions/${sessionId}/cache`, {
            method: 'DELETE'
        });
        console.log(`Cache cleared for session: ${sessionId}`);
    } catch (error) {
        console.error('Error clearing session cache:', error);
    }
    
    sessions = sessions.filter(s => s.id !== sessionId);
    saveSessionsToStorage();
    
    if (currentSessionId === sessionId) {
        if (sessions.length === 0) {
            createNewSession();
        } else {
            loadSession(sessions[0].id);
        }
    } else {
        renderSessions();
    }
}

async function clearAllSessions() {
    // Clear cache for all sessions
    for (const session of sessions) {
        try {
            await fetch(`${API_BASE_URL}/sessions/${session.id}/cache`, {
                method: 'DELETE'
            });
        } catch (error) {
            console.error(`Error clearing cache for session ${session.id}:`, error);
        }
    }
    
    sessions = [];
    saveSessionsToStorage();
    createNewSession();
}

function updateSessionTitle(sessionId, firstMessage) {
    const session = sessions.find(s => s.id === sessionId);
    if (session && session.title === 'New Chat') {
        session.title = firstMessage.substring(0, 30) + (firstMessage.length > 30 ? '...' : '');
        saveSessionsToStorage();
        renderSessions();
    }
}

function saveMessageToSession(text, type, metadata = {}) {
    const session = sessions.find(s => s.id === currentSessionId);
    if (session) {
        session.messages.push({ text, type, metadata });
        
        // Update title with first user message
        if (type === 'user' && session.messages.filter(m => m.type === 'user').length === 1) {
            updateSessionTitle(currentSessionId, text);
            return; // renderSessions() will be called by updateSessionTitle
        }
        
        // Save to localStorage without re-rendering sidebar
        saveSessionsToStorage();
    }
}

function renderSessions() {
    sessionList.innerHTML = '';
    
    sessions.forEach(session => {
        const item = document.createElement('div');
        item.className = 'session-item';
        if (session.id === currentSessionId) {
            item.classList.add('active');
        }
        
        const text = document.createElement('span');
        text.className = 'session-item-text';
        text.textContent = session.title;
        
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'session-item-delete';
        deleteBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
        `;
        
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (confirm('Delete this chat?')) {
                deleteSession(session.id);
            }
        });
        
        item.addEventListener('click', () => {
            if (session.id !== currentSessionId) {
                loadSession(session.id);
            }
        });
        
        item.appendChild(text);
        item.appendChild(deleteBtn);
        sessionList.appendChild(item);
    });
}

function clearChatDisplay() {
    chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-avatar bot-avatar">AI</div>
            <div class="message-content">
                <div class="message-text">
                    <p>Hello! I'm your AI Data Assistant. I can help you query and analyze your Google Sheets data using natural language.</p>
                    <p>Try asking questions like:</p>
                    <ul>
                        <li>"Show me all purchases from last month"</li>
                        <li>"What's the total revenue by product?"</li>
                        <li>"How many orders were placed today?"</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
}

// Periodic health check
setInterval(checkHealth, 30000); // Check every 30 seconds

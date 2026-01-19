/**
 * Frontend JavaScript for AI Data Assistant
 * Handles chat interactions, API calls, and UI updates with Claude-style streaming
 * FIXED: Messages no longer disappear after streaming
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
let isLoadingSession = false;
let currentStreamingMessage = null;

// Initialize - only once
document.addEventListener('DOMContentLoaded', () => {
    console.log('=== DOMContentLoaded fired ===');
    console.log('Window location:', window.location.href);
    loadSessionsFromStorage();
    initializeSession();
    checkHealth();
    setupEventListeners();
    autoResizeTextarea();
});

// Event Listeners
function setupEventListeners() {
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
    
    newChatBtn.addEventListener('click', () => {
        createNewSession();
    });
    
    clearAllBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear all chat history?')) {
            clearAllSessions();
        }
    });
    
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
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

// Send message with Claude-style streaming
async function sendMessage() {
    console.log('=== sendMessage() called ===');
    const question = userInput.value.trim();
    console.log('Question:', question);
    if (!question || isProcessing) {
        console.log('Skipping - empty question or already processing');
        return;
    }
    
    // Add user message to chat AND save to session immediately
    addMessageToUI(question, 'user');
    saveMessageToSession(question, 'user', {});
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    sendBtn.disabled = true;
    
    // Set processing state
    isProcessing = true;
    console.log('Processing started...');
    
    // Show thinking indicator while waiting for response
    showThinkingIndicator();
    
    let streamingMessageId = null;
    
    try {
        // Get conversation context
        const conversationContext = getConversationContext();
        console.log('Calling API...');
        
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
        
        // Debug: Log the response
        console.log('API Response:', data);
        
        // Remove thinking indicator and create streaming message
        removeThinkingIndicator();
        
        // Check if we have a valid answer
        if (!data.answer) {
            console.error('No answer in response:', data);
            addMessageToUI('Sorry, I received an empty response. Please try again.', 'bot', { confidence: 0 });
            saveMessageToSession('Sorry, I received an empty response. Please try again.', 'bot', { confidence: 0 });
            return;
        }
        
        // Create the streaming message
        streamingMessageId = createStreamingMessage();
        
        // Save bot message to session BEFORE streaming starts
        // This ensures it's saved even if something goes wrong
        saveMessageToSession(data.answer, 'bot', {
            confidence: data.confidence,
            rowsFound: data.rows_found,
            dataPreview: data.data_preview,
            queryType: data.query_type
        });
        
        // Stream the response text with Claude-style chunks
        console.log('Starting streaming with messageId:', streamingMessageId);
        await streamTextClaudeStyle(data.answer, streamingMessageId);
        console.log('Streaming completed');
        
        // Add metadata after streaming completes
        console.log('Adding metadata to message...');
        addMetadataToMessage(streamingMessageId, {
            confidence: data.confidence,
            rowsFound: data.rows_found,
            dataPreview: data.data_preview,
            queryType: data.query_type
        });
        console.log('Metadata added');
        
        // NO session reload or re-render here!
        // The message is already displayed and saved
        
        // Update health status
        checkHealth();
        
    } catch (error) {
        console.error('Error in sendMessage:', error);
        removeThinkingIndicator();
        if (streamingMessageId) removeStreamingMessage(streamingMessageId);
        
        const errorMsg = `Sorry, I encountered an error: ${error.message}. Please make sure the backend server is running.`;
        addMessageToUI(errorMsg, 'bot', { confidence: 0 });
        saveMessageToSession(errorMsg, 'bot', { confidence: 0 });
        
        console.error('Error sending message:', error);
    } finally {
        console.log('Finally block - cleaning up');
        isProcessing = false;
        sendBtn.disabled = false;
        currentStreamingMessage = null;
        console.log('Cleanup complete - NO RELOAD');
    }
}

// Show thinking indicator (animated dots)
function showThinkingIndicator() {
    // Remove any existing indicator first
    removeThinkingIndicator();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'thinking-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot-avatar';
    avatar.textContent = 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const thinkingDots = document.createElement('div');
    thinkingDots.className = 'thinking-dots';
    thinkingDots.innerHTML = '<span></span><span></span><span></span>';
    
    content.appendChild(thinkingDots);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    
    smoothScrollToBottom();
}

// Remove thinking indicator
function removeThinkingIndicator() {
    const existing = document.getElementById('thinking-indicator');
    if (existing) {
        existing.remove();
    }
}

// Create empty message for streaming
function createStreamingMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    const messageId = 'stream-' + Date.now();
    messageDiv.id = messageId;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar bot-avatar';
    avatar.textContent = 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text streaming';
    messageText.innerHTML = '';
    
    content.appendChild(messageText);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    
    currentStreamingMessage = {
        id: messageId,
        element: messageDiv,
        textElement: messageText,
        fullText: '',
        isStreaming: true
    };
    
    smoothScrollToBottom();
    
    return messageId;
}

// Stream text in Claude style - word by word with natural pauses (FAST)
async function streamTextClaudeStyle(text, messageId) {
    if (!currentStreamingMessage || currentStreamingMessage.id !== messageId) return;
    
    const messageText = currentStreamingMessage.textElement;
    
    // Split by characters for smoother streaming with markdown support
    const chars = text.split('');
    let displayedText = '';
    let charCount = 0;
    
    for (let i = 0; i < chars.length; i++) {
        if (!currentStreamingMessage || currentStreamingMessage.id !== messageId || !currentStreamingMessage.isStreaming) break;
        
        const char = chars[i];
        displayedText += char;
        charCount++;
        
        // Update more frequently for smoother streaming
        const shouldUpdate = 
            i === chars.length - 1 || // Last character
            char === '\n' || // Always update on newlines (important for markdown)
            char.match(/[.!?]/) || // Sentence endings
            charCount >= 8; // Update every 8 characters
        
        if (shouldUpdate) {
            currentStreamingMessage.fullText = displayedText;
            
            // Format and render with markdown
            const formattedText = formatBotMessage(displayedText);
            messageText.innerHTML = formattedText;
            
            // FORCE scroll during streaming - call it every update
            smoothScrollToBottom();
            
            // Fast delays
            let delay;
            if (char === '\n') {
                delay = 15; // Brief pause at newlines
            } else if (char.match(/[.!?]/)) {
                delay = 20 + Math.random() * 10; // Short pause at sentence end
            } else {
                delay = 3 + Math.random() * 3; // Very fast for characters
            }
            
            await sleep(delay);
            charCount = 0;
        }
    }
    
    // Finalize - remove streaming class
    if (currentStreamingMessage && currentStreamingMessage.id === messageId) {
        currentStreamingMessage.isStreaming = false;
        const finalFormatted = formatBotMessage(displayedText);
        messageText.innerHTML = finalFormatted;
        messageText.classList.remove('streaming');
        
        // Final scroll after streaming completes
        smoothScrollToBottom();
    }
}

// Format bot message with markdown (improved)
function formatBotMessage(text) {
    let formattedText = text;
    
    // Escape HTML to prevent injection
    const tempDiv = document.createElement('div');
    tempDiv.textContent = formattedText;
    formattedText = tempDiv.innerHTML;
    
    // Convert markdown tables to HTML tables
    formattedText = convertMarkdownTables(formattedText);
    
    // Convert code blocks ```
    formattedText = formattedText.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="code-block"><code>$2</code></pre>');
    
    // Convert inline code `code`
    formattedText = formattedText.replace(/`([^`]+)`/g, '<code class="inline-code">$1</code>');
    
    // Convert markdown headers (must be on new line) - order matters: #### before ### before ## before #
    formattedText = formattedText.replace(/^####\s+(.+)$/gm, '<h4 class="md-h4">$1</h4>');
    formattedText = formattedText.replace(/^###\s+(.+)$/gm, '<h3 class="md-h3">$1</h3>');
    formattedText = formattedText.replace(/^##\s+(.+)$/gm, '<h2 class="md-h2">$1</h2>');
    formattedText = formattedText.replace(/^#\s+(.+)$/gm, '<h1 class="md-h1">$1</h1>');
    
    // Auto-detect title patterns (lines that look like titles - short, no punctuation at end, followed by content)
    formattedText = formattedText.replace(/^([A-Z][A-Za-z0-9\s:&\-–—]+(?:vs\.?|vs|and|&)?[A-Za-z0-9\s:&\-–—]*)$/gm, function(match, title) {
        title = title.trim();
        if (title.length > 5 && title.length < 80 && !title.match(/[.!?,;]$/) && title.match(/^[A-Z]/)) {
            if (title.match(/(Overview|Highlights|Details|Comparison|Summary|Breakdown|Analysis|Key|Total|Orders|Pending|Complete|Status|vs\.?|:)/i)) {
                if (title.match(/(Overview|Comparison|Summary|Analysis|vs\.?)/i) && title.length < 50) {
                    return `<h2 class="md-h2 md-title">${title}</h2>`;
                }
                return `<h3 class="md-h3 md-subtitle">${title}</h3>`;
            }
        }
        return match;
    });
    
    // Convert horizontal rules
    formattedText = formattedText.replace(/^---+$/gm, '<hr class="md-hr">');
    
    // Convert blockquotes
    formattedText = formattedText.replace(/^&gt;\s+(.+)$/gm, '<blockquote class="md-blockquote">$1</blockquote>');
    
    // Convert **bold** and *italic* and ***bold italic***
    formattedText = formattedText.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    formattedText = formattedText.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\*(.+?)\*/g, '<em>$1</em>');
    formattedText = formattedText.replace(/__(.+?)__/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/_(.+?)_/g, '<em>$1</em>');
    
    // Convert ~~strikethrough~~
    formattedText = formattedText.replace(/~~(.+?)~~/g, '<del>$1</del>');
    
    // Convert links [text](url)
    formattedText = formattedText.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="md-link">$1</a>');
    
    // Convert numbered lists (1. 2. 3.)
    formattedText = formattedText.replace(/^\d+\.\s+(.+)$/gm, '<oli>$1</oli>');
    formattedText = formattedText.replace(/(<oli>[\s\S]*?<\/oli>\n?)+/g, function(match) {
        const items = match.match(/<oli>([\s\S]*?)<\/oli>/g);
        if (!items) return match;
        const listItems = items.map(item => {
            const content = item.replace(/<\/?oli>/g, '').trim();
            return `<li>${content}</li>`;
        }).join('');
        return `<ol class="md-ol">${listItems}</ol>`;
    });
    
    // Convert bullet points (-, *, •)
    formattedText = formattedText.replace(/^[•\-\*]\s+(.+)$/gm, '<uli>$1</uli>');
    formattedText = formattedText.replace(/(<uli>[\s\S]*?<\/uli>\n?)+/g, function(match) {
        const items = match.match(/<uli>([\s\S]*?)<\/uli>/g);
        if (!items) return match;
        const listItems = items.map(item => {
            const content = item.replace(/<\/?uli>/g, '').trim();
            return `<li>${content}</li>`;
        }).join('');
        return `<ul class="md-ul">${listItems}</ul>`;
    });
    
    // Convert line breaks (double newlines to paragraphs, single to br)
    formattedText = formattedText.replace(/\n\n+/g, '</p><p>');
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    // Clean up empty paragraphs
    formattedText = formattedText.replace(/<p><\/p>/g, '');
    formattedText = formattedText.replace(/<p><br><\/p>/g, '');
    
    // Wrap in paragraph if not already wrapped in block elements
    if (!formattedText.match(/^<(h[1-6]|ul|ol|pre|table|p|blockquote)/)) {
        formattedText = '<p>' + formattedText + '</p>';
    }
    
    return formattedText;
}

// Add metadata to streamed message
function addMetadataToMessage(messageId, metadata) {
    const messageDiv = document.getElementById(messageId);
    if (!messageDiv) return;
    
    const content = messageDiv.querySelector('.message-content');
    if (!content) return;
    
    // Add data table if present
    if (metadata.dataPreview && metadata.dataPreview.length > 0) {
        const tableContainer = createDataTable(metadata.dataPreview);
        content.appendChild(tableContainer);
        
        // Scroll after adding table
        smoothScrollToBottom();
    }
    
    // Add metadata
    if (metadata.confidence !== undefined) {
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
        
        // Scroll after adding metadata
        smoothScrollToBottom();
    }
}

// Remove streaming message (in case of error)
function removeStreamingMessage(messageId) {
    const messageDiv = document.getElementById(messageId);
    if (messageDiv) {
        messageDiv.remove();
    }
    currentStreamingMessage = null;
}

// Sleep utility for streaming delay
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Get conversation context for API
function getConversationContext() {
    const session = sessions.find(s => s.id === currentSessionId);
    if (!session || !session.messages) return [];
    
    const messages = session.messages;
    const contextMessages = [];
    
    // Get last 5 full messages
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
    const tableRegex = /((?:^\|.+\|\s*$\n?)+)/gm;
    
    return text.replace(tableRegex, (match) => {
        const lines = match.trim().split('\n');
        if (lines.length < 2) return match;
        
        if (!lines[1].match(/^\|[\s\-:|]+\|$/)) return match;
        
        const headers = lines[0].split('|').map(h => h.trim()).filter(h => h);
        const rows = lines.slice(2).map(line => {
            return line.split('|').map(cell => cell.trim()).filter(cell => cell !== '');
        }).filter(row => row.length > 0);
        
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

// Add message to UI only (for user messages and loaded sessions)
function addMessageToUI(text, type, metadata = {}) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = `message-avatar ${type}-avatar`;
    avatar.textContent = type === 'user' ? 'You' : 'AI';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    
    let formattedText = text;
    
    if (type === 'bot') {
        formattedText = formatBotMessage(formattedText);
        messageText.innerHTML = formattedText;
    } else {
        // User messages - escape HTML and convert line breaks
        const tempDiv = document.createElement('div');
        tempDiv.textContent = formattedText;
        formattedText = tempDiv.innerHTML;
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
    
    // DON'T save to session here - only display
    // Saving is handled separately in sendMessage
    
    smoothScrollToBottom();
}

// Create data table
function createDataTable(data) {
    const container = document.createElement('div');
    container.className = 'data-table-container';
    
    const table = document.createElement('table');
    table.className = 'data-table';
    
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

// Smooth scroll to bottom
function smoothScrollToBottom() {
    // Always scroll during streaming, otherwise check if user is near bottom
    requestAnimationFrame(() => {
        if (currentStreamingMessage && currentStreamingMessage.isStreaming) {
            // Force scroll during streaming
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else {
            // Normal behavior - only scroll if user is near bottom
            const isNearBottom = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < 150;
            if (isNearBottom) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
    });
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
    console.log('=== loadSession called ===', sessionId);
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return;
    
    isLoadingSession = true;
    
    currentSessionId = sessionId;
    clearChatDisplay();
    
    session.messages.forEach(msg => {
        addMessageToUI(msg.text, msg.type, msg.metadata || {});
    });
    
    isLoadingSession = false;
    
    renderSessions();
}

async function deleteSession(sessionId) {
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
        // DON'T call renderSessions() here - it can cause issues during streaming
        // Just update the session list without reloading
        updateSessionListItem(sessionId);
    }
}

// Update a single session list item without full re-render
function updateSessionListItem(sessionId) {
    const session = sessions.find(s => s.id === sessionId);
    if (!session) return;
    
    // Find the session item in the DOM
    const sessionItems = sessionList.querySelectorAll('.session-item');
    sessionItems.forEach(item => {
        // Check if this is the right session by comparing the text or adding data attributes
        const textSpan = item.querySelector('.session-item-text');
        if (item.classList.contains('active')) {
            textSpan.textContent = session.title;
        }
    });
}

function saveMessageToSession(text, type, metadata = {}) {
    if (!currentSessionId) {
        console.error('No current session ID');
        return;
    }
    
    const session = sessions.find(s => s.id === currentSessionId);
    if (session) {
        session.messages.push({ text, type, metadata });
        
        // Update session title if this is the first user message
        if (type === 'user' && session.messages.filter(m => m.type === 'user').length === 1) {
            updateSessionTitle(currentSessionId, text);
        } else {
            // Just save to storage, DON'T trigger any re-renders
            saveSessionsToStorage();
        }
        
        console.log(`Message saved to session ${currentSessionId}. Total messages: ${session.messages.length}`);
        return session.messages.length - 1; // Return index of saved message
    } else {
        console.error('Session not found:', currentSessionId);
    }
}

function renderSessions() {
    sessionList.innerHTML = '';
    
    sessions.forEach(session => {
        const item = document.createElement('div');
        item.className = 'session-item';
        item.dataset.sessionId = session.id; // Add data attribute for identification
        
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
    console.log('=== clearChatDisplay called ===');
    console.log('Stack trace:', new Error().stack);
    chatMessages.innerHTML = `
        <div class="message bot-message">
            <div class="message-avatar bot-avatar">AI</div>
            <div class="message-content">
                <div class="message-text">
                    <p>Hello! I'm your AI Data Assistant. I can help you query and analyze your Google Sheets data using natural language.</p>
                    <p>Try asking questions like:</p>
                    <ul class="md-ul">
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
setInterval(checkHealth, 30000);